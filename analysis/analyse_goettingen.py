"""



            case 'correct_predictable': return 5
            case 'correct_unpredictable': return 6
            case 'error': return 7


~/data/electrotime/goettingen/run_*

"""
import numpy, pandas, seaborn
import matplotlib.pyplot as plt
import matplotlib
from logging import getLogger, basicConfig, INFO, StreamHandler
from enum import StrEnum
import sys
from tqdm import tqdm
from os.path import expanduser, join
from glob import glob
log = getLogger('electrotime')
log.setLevel(INFO)
matplotlib.use('agg') 

class MODALITY(StrEnum):
    LIGHT = 'light'
    SOUND = 'sound'

LIGHT_COL, SOUND_COL, TRIGGER_COL, TIME_COL = 0, 1, 2, 3
EPOCH_TMIN = -100 ## start of epoch wrt to trigger in samples
EPOCH_TMAX = 400    ## end of epoch wrt to trigger in samples
TRIGGER_MODALITY = {
    5: MODALITY.SOUND,
    6: MODALITY.SOUND,
    7: MODALITY.SOUND,
    15: MODALITY.LIGHT,
    16: MODALITY.LIGHT,
    17: MODALITY.LIGHT,
    18: MODALITY.LIGHT,
}
selected_triggers = set(TRIGGER_MODALITY.keys())
epoch_len = EPOCH_TMAX - EPOCH_TMIN


in_dir = sys.argv[1]
target_dir = expanduser(in_dir)
fpaths = sorted(glob(join(target_dir, '**', 'electrotime*.txt')))
log.info(f'Found {len(fpaths)} data files.')

epochs = []
triggers = []
modalities = []
bad_lines = []

## extract data arrays from files
for fpath in tqdm(fpaths):
    data_lol = []
    with open(fpath) as fhandle:
        lines = fhandle.readlines()
    for line in lines:
        cells = line.strip().strip(',').split(',')
        if len(cells) != 4:
            bad_lines.append(line)
            continue
        data_lol.append([int(c) for c in cells])
    data = numpy.array(data_lol)

    trigger_idx = numpy.where(numpy.diff(data[:, 2]) > 0)[0]+1
    for index in trigger_idx:
        trigger_val = data[index, 2]
        if trigger_val not in selected_triggers:
            ## skipping as we are not interested in this trigger
            continue
        start = index+EPOCH_TMIN
        end = index+EPOCH_TMAX
        if (start < 0) or (end > data.shape[0]):
            ## ignoring this trigger as we cannot observe a full window
            continue
        epoch = data[start:end, :].copy()
        epoch[:, 3] = epoch[:, 3] - data[index, 3]
        epochs.append(epoch)
        triggers.append(trigger_val)
        modalities.append(TRIGGER_MODALITY[trigger_val])

log.info(f'malformed lines: {len(bad_lines)}')
log.info(f'epochs: {len(epochs)}')

## Store data in dataframe
triggers = numpy.array(triggers)   
epochs = numpy.array(epochs)
df = pandas.DataFrame(
    dict(
        epoch=numpy.arange(triggers.size).repeat(epoch_len),
        trigger=triggers.repeat(epoch_len),
        time=epochs[:,:,TIME_COL].ravel(),
        light=epochs[:,:,LIGHT_COL].ravel(),
        sound=epochs[:,:,SOUND_COL].ravel()
    )
)
df['time'] = df.time/1000

### loop over some random epochs
raise ValueError
df = df[df.epoch==2]


#plt.figure()
seaborn.lineplot(df, x='time', y='sound', hue='epoch')
plt.title('sound')
plt.savefig(f'plots/goettingen/lines_sound_trial.png')
plt.close('all')

# seaborn.lineplot(df, x='time', y='light', hue='epoch')
# plt.title('light')
# plt.savefig(f'plots/goettingen/lines_sound_trial.png')
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
plt.savefig(f'plots/goettingen/dist_sound.png')
plt.close('all')