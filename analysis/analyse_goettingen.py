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
BASELINE_SOUND = 512
BASELINE_LIGHT = 7

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

    ## sample indices where trigger column is not 0 and has changed
    trigger_idx = numpy.where(numpy.diff(data[:, TRIGGER_COL]) > 0)[0]+1
    for index in trigger_idx:
        trigger_val = data[index, TRIGGER_COL]
        if trigger_val not in selected_triggers:
            ## skipping as we are not interested in this trigger
            continue
        start = index+EPOCH_TMIN
        end = index+EPOCH_TMAX
        if (start < 0) or (end > data.shape[0]):
            ## ignoring this trigger as we cannot observe a full window
            continue
        epoch = data[start:end, :].copy()
        ## make time relative to trigger onset:
        epoch[:, TIME_COL] = epoch[:, TIME_COL] - data[index, TIME_COL]
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

## Plots of the light/sound intensity in the epoch timeframe
for modality in (MODALITY.LIGHT, MODALITY.SOUND):

    ### loop over some random epochs for each modality
    mod_epochs = df[df.modality==modality].epoch.unique().tolist()
    sample_epochs = sample(mod_epochs, 5)
    for e in sample_epochs:
        ## plot a single epoch to get an idea of what these look like
        df_epoch = df[df.epoch==e]
        trigger = df_epoch.trigger.values[0]
        seaborn.lineplot(df_epoch, x='time', y=modality.name.lower())
        plt.title(f'{modality.name.lower()} trigger: {trigger} epoch: {e:03}')
        plt.savefig(f'plots/goettingen/{modality.name.lower()}_{e:03}.png')
        plt.close('all')

    ## plot epoch lines together
    df_mod = df[df.modality==modality]
    n_epochs = df.epoch.unique().size
    seaborn.lineplot(
        df_mod,
        x='time',
        y=modality.name.lower(),
        units='epoch', estimator=None,
        color='black',
        alpha=0.1,
        linewidth=0.6,
        legend=False,
    )
    plt.title(f'{modality.name.lower()} epochs: {n_epochs}')
    plt.savefig(f'plots/goettingen/{modality.name.lower()}_all.png', dpi=600)
    plt.close('all')

## determine stimulus onset
delays = []
for e in df.epoch.unique():

    df_epoch = df[df.epoch==e]
    for _, row in df_epoch.iterrows():

        if row.modality == MODALITY.SOUND:
            hit = abs(row.sound-BASELINE_SOUND) > DELTA_SOUND
        else:
            hit = (row.light-BASELINE_LIGHT) > DELTA_LIGHT

        if hit:
            delays.append(
                dict(
                    epoch=row.epoch,
                    trigger=row.trigger,
                    modality=row.modality,
                    delay=row.time
                )
            )
            break

## calculate trigger-wise mean and std of delay and store as table
delays_df = pandas.DataFrame(delays)
table = []
for trigger in sorted(delays_df.trigger.unique()):
    trigger_df = delays_df[delays_df.trigger == trigger]
    table.append(
        dict(
            trigger=trigger,
            modality=trigger_df.modality.iloc[0].name,
            count=trigger_df.shape[0],
            mean=trigger_df.delay.mean(),
            std=trigger_df.delay.std()
        )
    )
pandas.DataFrame(table).to_csv(
    'trigger_delays.csv',
    float_format='%.3f',
    index=False
)


# seaborn.histplot(times)
# plt.title('bla')
# plt.savefig(f'plots/goettingen/dist_sound.png')
# plt.close('all')