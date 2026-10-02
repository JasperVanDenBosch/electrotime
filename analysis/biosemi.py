"""
Compare the latency of ElectroTime with 
a Biosemi "photosensor" and audio signal routed to EXG 1.

data: ~/data/electrotime/vs_biosemi
experiment: ./experiment/run.py
raw log notes from lab:

1. 20:56 tones 1s mkIII
2. 21:01 noise 0.2s mkIII (2x runs)
3. disconnect, +2 runs
4. 21:13 noise 0.2s mkII
5. second run at 21:17
6. (reconnect i think, few more runs)

In other words, I started with the mkIII device. 
The first run of 100 stimuli was using 1s tones.
I then ran some runs (4?) with 0.2 white noise stimuli.
After that I setup the mkII instead and recorded a number of runs on that.
I disconnected about every other run, to reset the serial buffer.
On the mkIII, in the GUI I observed some strange numbering for the triggers. 
So we should look at how the triggers arrived, some may have abberant values 
or there may be noise on the trigger channel (e.g. it was on for just one sample).


## electrotime data analysis
see analyse_goettingen.py for an example of how to analyse the electrotime data.

## biosemi data analysis
- read bdf
- drop channels except: trigger, EXG1 (audio) and ??? (photosensor)
- after that the data has a similar shape so we follow the same approach


Store intermediate data or plots in the derivatives folder or here, 
do not make changes to the vs_biosemi root data folder.
"""