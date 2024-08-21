"""
# epoch_nr, light, trigger, tval

In [33]: epochs_df[epochs_df.latency_ms<5]
Out[33]:
     trigger  latency_sample  latency_ms
87        89               0         0.0
132      135               0         0.0

"""
import numpy, pandas, seaborn
import matplotlib.pyplot as plt
import sys

fpath = sys.argv[1]
raw = numpy.load(fpath)
EPOCH_LEN = 40  ## length of an epoch in samples -> 100 to see it go off
T_DUR_US = 64
THRESHOLD_PERCENTILE = 80
THRESHOLD_FRACTION = 0.8
OFFSET_US = 0 #20_000 applies for old simulator settings where i delayed the stim by 20ms
TRIGGERS_IGNORE = [1,2] + list(range(24, 31+1)) + list(range(32, 47+1))

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
epochs = numpy.array(epochs, dtype=numpy.int32)

df = pandas.DataFrame(dict(
    epoch=numpy.arange(triggers.size).repeat(EPOCH_LEN),
    trigger=triggers.repeat(EPOCH_LEN),
    time=epochs[:,:,1].ravel()-OFFSET_US,
    light=epochs[:,:,0].ravel()
))
df['time (ms)'] = df.time/1000


## 1. determine threshold

threshold = THRESHOLD_FRACTION * numpy.percentile(
    df.light.values,
    q=THRESHOLD_PERCENTILE,
    method='closest_observation'
)
epochs_dicts = []
for e in df.epoch.unique():
    valid = True
    epoch_df = df[df.epoch==e]
    if epoch_df.trigger.iloc[0] in TRIGGERS_IGNORE:
        print(f'Discarding epoch as trigger ignored')
        valid = False
    samples_over_threshold = epoch_df.light.values >= threshold
    if numpy.any(samples_over_threshold):
        target_s = numpy.where(epoch_df.light.values >= threshold)[0][0]
        latency_ms=epoch_df.iloc[target_s]['time (ms)']
        if target_s < 2:
            print(f'Discarding epoch since threshold reached too soon')
            valid = False
    else:
        print(f'Discarding epoch since threshold never reached')
        target_s = None
        valid = False
        latency_ms = None
    epochs_dicts.append(
        dict(
            epoch=epoch_df.epoch.iloc[0],
            trigger=epoch_df.trigger.iloc[0],
            latency_sample=target_s,
            latency_ms=latency_ms,
            valid=valid
        )
    )

epochs_df = pandas.DataFrame(epochs_dicts)
valid_epoch_numbers = epochs_df[epochs_df.valid == True].epoch.values
df = df[df.isin(valid_epoch_numbers).epoch]
latency = epochs_df[epochs_df.valid == True].latency_ms
summary = f'latency (ms) mean: {latency.mean():.2f} std: {latency.std():.2f} threshold: {threshold:.1f}'

plt.figure()
seaborn.lineplot(df, x='time (ms)', y='light', hue='trigger')
plt.title(summary)
plt.savefig(f'plots/lines.png')
plt.close('all')
