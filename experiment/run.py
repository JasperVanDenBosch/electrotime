"""Simple experiment code to test setup in lab setting

Odd triggers present a visual stimulus, even triggers a white noise burst.
"""
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB'] # fail rather than fall back to a slow backend
from psychopy.sound import Sound
from psychopy.monitors import Monitor
from psychopy.event import getKeys
from psychopy.visual import Window
from psychopy.visual.rect import Rect
from psychopy.parallel import ParallelPort as PsychopyParallelPort
import time
import numpy


ADDRESS = '0xE020'
INTER_TRIAL_INTERVAL_SEC = 2
STIM_DUR_SEC = 0.2
SAMPLE_RATE = 48000
port = PsychopyParallelPort(address=ADDRESS)

def send_trigger(val: int):
    port.setData(val) # val: int , address='FIO'


my_monitor = Monitor(
    name='latrec_mon',
    distance=50.0
)
my_monitor.setSizePix([1920, 1080])
my_monitor.setWidth(60.0)
my_monitor.saveMon()
win = Window(
    size=[1920, 1080],
    monitor=my_monitor,
    color='black',
    fullscr=True,
    units='pix'
)
win.mouseVisible = False 

stimulus = Rect(
    win=win,
    size=(250, 250),
    units='pix',
    pos=(250, 250),
    lineColor=(1, 1, 1),
    fillColor=(1, 1, 1),
    name='stimulus'
)

## full scale white noise, no ramp; same spectrum as the 50ms startle probe
noise = numpy.random.uniform(-1, 1, int(SAMPLE_RATE * STIM_DUR_SEC))
sound = Sound(noise, sampleRate=SAMPLE_RATE, hamming=False)


for i in range(100):
    trigger = 1+i
    visual = trigger % 2 == 1

    new_keys = getKeys(keyList=['q', 'esc'])
    if 'q' in new_keys or 'esc' in new_keys:
        break ## quit experiment


    time.sleep(INTER_TRIAL_INTERVAL_SEC)

    if visual:
        stimulus.draw()
    else:
        sound.play(when=win.getFutureFlipTime(clock='ptb'))
    win.callOnFlip(send_trigger, trigger)
    win.flip() # trigger on
    if visual:
        stimulus.draw()
    win.flip() # 16ms
    if visual:
        stimulus.draw()
    win.flip() # 33ms
    if visual:
        stimulus.draw()
    win.callOnFlip(send_trigger, 0)
    win.flip() # 50ms
    time.sleep(STIM_DUR_SEC-0.050)
    win.flip() # stimulus off


win.close()