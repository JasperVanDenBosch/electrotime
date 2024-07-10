import numpy, seaborn

fpath = 'data/latrec_2024-07-10T173335.npy'
raw = numpy.load(fpath)


# loop through continous
# detect trigger onsets
# slice 100ms segments
# if more than one epoch ID, discard
# subtract trigger timestamp from sample timestamps

print(f'Epoching..')
