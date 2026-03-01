"""

overall timeline plot

220,510,0,251350588,
218,510,0,251359392,
217,510,0,251360084,

triggers: array([ 0,  1,  2,  3,  6,  7, 16, 28, 31])
?            1 (209x)
?            2 (177x)
flanker: 16 (2x)
response (missing): 28  (741x)
                    31 (162x)
startle_unpred: 6 (1x)
startle_error: return 7 (316x)


"""
import numpy, pandas, seaborn
import matplotlib.pyplot as plt
import matplotlib
import sys
from os.path import expanduser, join
from glob import glob
matplotlib.use('agg') 

LIGHT_COL = 0
SOUND_COL = 1
TRIGGER_COL = 2
TIME_COL = 3
EPOCH_WINDOW = (-100, 400) ## samples wrt trigger
SELECTED_TRIGGERS = [7]
epoch_len = EPOCH_WINDOW[1] - EPOCH_WINDOW[0]


in_dir = sys.argv[1]
target_dir = expanduser(in_dir)
fpaths = sorted(glob(join(target_dir, 'latrec*.txt')))

epochs = []
triggers = []

for fpath in fpaths:
    data_lol = []
    with open(fpath) as fhandle:
        lines = fhandle.readlines()
    for line in lines:
        cells = line.strip().strip(',').split(',')
        assert len(cells) == 4
        data_lol.append([int(c) for c in cells])
    data = numpy.array(data_lol)

    trigger_idx = numpy.where(numpy.diff(data[:, 2]) > 0)[0]+1
    for index in trigger_idx:
        start = index+EPOCH_WINDOW[0]
        end = index+EPOCH_WINDOW[1]
        if (start < 0) or (end > data.shape[0]):
            print(f'dropping epoch..')
            continue
        epoch = data[start:end, :].copy()
        epoch[:, 3] = epoch[:, 3] - data[index, 3]
        epochs.append(epoch)
        triggers.append(data[index, 2])

triggers = numpy.array(triggers)   
epochs = numpy.array(epochs)
df = pandas.DataFrame(
    dict(
        epoch=numpy.arange(triggers.size).repeat(epoch_len),
        trigger=triggers.repeat(epoch_len),
        time=epochs[:,:,3].ravel(),
        light=epochs[:,:,0].ravel(),
        sound=epochs[:,:,1].ravel()
    )
)
df['time'] = df.time/1000



df = df[df.isin(SELECTED_TRIGGERS).trigger]
df = df[df.epoch==2]


#plt.figure()
seaborn.lineplot(df, x='time', y='sound', hue='epoch')
plt.title('sound')
plt.savefig(f'plots/lines_sound_trial.png')
plt.close('all')

# seaborn.lineplot(df, x='time', y='light', hue='epoch')
# plt.title('light')
# plt.savefig(f'plots/lines_sound_trial.png')
# plt.close('all')


times_list = []
for e in df.epoch.unique():

    df_epoch = df[df.epoch==e]
    for x, row in df_epoch.iterrows():
        if abs(row.sound-512) > 50:
            times_list.append(row.time)
            break

times = numpy.array(times_list)
print(f'times {times.mean():.2f} {times.std():.2f}  min={times.min():.2f}  max={times.max():.2f}')

seaborn.histplot(times)
plt.title('bla')
plt.savefig(f'plots/dist_sound.png')
plt.close('all')