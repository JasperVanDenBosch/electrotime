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
import sys
from os.path import expanduser, join
from glob import glob

LIGHT_COL = 0
SOUND_COL = 1
TRIGGER_COL = 2
TIME_COL = 3
EPOCH_WINDOW = (-100, 400) ## samples wrt trigger

SELECTED_TRIGGERS = [7]

in_dir = sys.argv[1]
target_dir = expanduser(in_dir)
fpaths = sorted(glob(join(target_dir, 'latrec*.txt')))

metas = []
epochs = []

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
        start = index-EPOCH_WINDOW[0]
        end = index+EPOCH_WINDOW[1]
        if start < 0 or end > data.shape[0]:
            print(f'dropping epoch..')
        epochs.append(data[start:end, :])


    

## check for triggers staying over samples