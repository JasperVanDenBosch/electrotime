"""
Parse data files of prototype MkII s/n 002 recorded in Goettingen
"""
import numpy, pandas, seaborn
from random import sample
import matplotlib.pyplot as plt
import matplotlib
from logging import getLogger, INFO
from enum import Enum
import sys
from tqdm import tqdm
from os.path import expanduser, join
from glob import glob
log = getLogger('electrotime')
log.setLevel(INFO)
matplotlib.use('agg') 

class MODALITY(Enum):
    LIGHT = 1
    SOUND = 2

LIGHT_COL, SOUND_COL, TRIGGER_COL, TIME_COL = 0, 1, 2, 3
EPOCH_TMIN = -100 ## start of epoch wrt to trigger in samples
EPOCH_TMAX = 400    ## end of epoch wrt to trigger in samples
## Defines which triggers are associated with which stimulus modality
TRIGGER_MODALITY = {
    5: MODALITY.SOUND,
    6: MODALITY.SOUND,
    7: MODALITY.SOUND,
    15: MODALITY.LIGHT,
    16: MODALITY.LIGHT,
    17: MODALITY.LIGHT,
    18: MODALITY.LIGHT,
}
## Thresholds
DELTA_SOUND = 80
DELTA_LIGHT = 60

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
modalities = numpy.array(modalities)
df = pandas.DataFrame(
    dict(
        epoch=numpy.arange(triggers.size).repeat(epoch_len),
        modality=modalities.repeat(epoch_len),
        trigger=triggers.repeat(epoch_len),
        time=epochs[:,:,TIME_COL].ravel(),
        light=epochs[:,:,LIGHT_COL].ravel(),
        sound=epochs[:,:,SOUND_COL].ravel()
    )
)
df['time'] = df.time/1000


for modality in (MODALITY.LIGHT, MODALITY.SOUND):

    ### loop over some random epochs for each modality
    mod_epochs = df[df.modality==modality].epoch.unique().tolist()
    sample_epochs = sample(mod_epochs, 5)
    for e in sample_epochs:

        ## plot a single epoch to get an idea of what these look like
        df_epoch = df[df.epoch==e]
        trigger = df_epoch.trigger.values[0]
        seaborn.lineplot(df_epoch, x='time', y=modality.name.lower(), hue='epoch')
        plt.title(f'{modality.name.lower()} trigger: {trigger} epoch: {e:03}')
        plt.savefig(f'plots/goettingen/{modality.name.lower()}_{e:03}.png')
        plt.close('all')

    ## plot epoch lines together
    df_mod = df[df.modality==modality]
    n_epochs = df.epoch.unique().size
    seaborn.lineplot(df_mod, x='time', y=modality.name.lower(), hue='epoch')
    plt.title(f'{modality.name.lower()} epochs: {n_epochs}')
    plt.savefig(f'plots/goettingen/{modality.name.lower()}_all.png')
    plt.close('all')

raise ValueError

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