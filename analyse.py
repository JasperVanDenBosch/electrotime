"""
# epoch_nr, light, trigger, tval

"""
import numpy, pandas, seaborn, matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

fpath = 'data/latrec_2024-07-10T173335.npy'
raw = numpy.load(fpath)
EPOCH_LEN = 100 ## length of an epoch in samples
T_DUR_US = 64

t_diff = numpy.diff(raw[:, 3])
approx_dur_secs = (t_diff[t_diff>0].sum() * T_DUR_US) / 1_000_000
print(f'Recording duration approx {round(approx_dur_secs)}s')

epochs = []
triggers = []
prev_trigger = 0
n_straddling = 0
for s in range(raw.shape[0]):

    this_trigger = raw[s, 2]
    if this_trigger != prev_trigger:
        prev_trigger = this_trigger
        if this_trigger != 0:
            epoch = raw[s:s+100, :].astype(numpy.uint32)
            n_clock_cycles = numpy.unique(epoch[:, 0]).size
            if n_clock_cycles > 1:
                print(f'Epoch straddles clock reset, discarding.')
                continue

            t_sample0 = epoch[0, 3]
            epoch[:, 3] = (epoch[:, 3] - t_sample0) * T_DUR_US
            triggers.append(this_trigger)
            epochs.append(epoch[:, [1, 3]])


"""
In [29]: epoch_df.time.values
Out[29]:
array([    0,  1024,  2112,  3136,  4160,  5184,  6208,  7232,  8256,
        9280, 10368, 11264, 12224, 13184, 14144, 15040, 16000, 16960,
       17920, 18816, 19776, 20736, 21888, 23040, 24128, 25280, 26432,
       27584, 28736, 29888, 31040, 32192, 33280, 34432, 35584, 36736,
       37888, 39040, 40192, 41344, 42432, 43584, 44736, 45888, 47040,
       48192, 49344, 50496, 51584, 52736, 53888, 55040, 56192, 57344,
       58496, 59648, 60736, 61888, 63040, 64192, 65344,   960,  2112,
        3264,  4352,  5312,  6272,  7232,  8128,  9088, 10048, 11008,
       11904, 12864, 13824, 14784, 15680, 16640, 17600, 18560, 19456,
       20416, 21376, 22336, 23232, 24192, 25152, 26112, 27008, 27968,
       28928, 29888, 30784, 31744, 32704, 33664, 34560, 35520, 36480,
       37440], dtype=uint16)


"""
        

triggers = numpy.array(triggers)   
epochs = numpy.array(epochs)

df = pandas.DataFrame(dict(
    epoch=numpy.arange(triggers.size).repeat(EPOCH_LEN),
    trigger=triggers.repeat(EPOCH_LEN),
    time=epochs[:,:,1].ravel(),
    light=epochs[:,:,0].ravel()
))
df['time (ms)'] = df.time/1000

#    epoch_df = df[df.epoch == e]
plt.figure()
seaborn.lineplot(df, x='time (ms)', y='light')
#plt.title(f'epoch {e}')
plt.savefig(f'plots/lines.png')
plt.close('all')
