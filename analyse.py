"""
# epoch_nr, light, trigger, tval

"""
import numpy, pandas, seaborn, matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

fpath = 'data/latrec_2024-07-10T173335.npy'
raw = numpy.load(fpath)
EPOCH_LEN = 40  ## length of an epoch in samples -> 100 to see it go off
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
            epoch = raw[s:s+EPOCH_LEN, :].astype(numpy.uint32)
            n_clock_cycles = numpy.unique(epoch[:, 0]).size
            if n_clock_cycles > 1:
                print(f'Epoch straddles clock reset, discarding.')
                continue

            t_sample0 = epoch[0, 3]
            epoch[:, 3] = (epoch[:, 3] - t_sample0) * T_DUR_US
            triggers.append(this_trigger)
            epochs.append(epoch[:, [1, 3]])
        

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
