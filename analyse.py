"""
# epoch_nr, light, trigger, tval

"""
import numpy, seaborn

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
            epoch = raw[s:s+100, :]
            n_clock_cycles = numpy.unique(epoch[:, 0]).size
            if n_clock_cycles > 1:
                #n_straddling += 1
                print(f'Epoch straddles clock reset, discarding.')
                continue

            t_sample0 = epoch[0, 3]
            epoch[:, 3] = (epoch[:, 3] - t_sample0) * T_DUR_US
            triggers.append(this_trigger)
            epochs.append(epoch[:, [1, 3]])
        

triggers = numpy.array(triggers)   
epochs = numpy.array(epochs)


# loop through continous
# detect trigger onsets
# slice 100ms segments
# if more than one epoch ID, discard
# subtract trigger timestamp from sample timestamps

# plot lineplot with timestamp as x axis

print(f'Epoching..')
