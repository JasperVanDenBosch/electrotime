# Audio latency via Biosemi: progress notes

Last updated: 2026-10-09

## Goal

Compare electrotime with a second way of measuring audio latency: feed the PC's audio output straight into the Biosemi Active 2 EEG amplifier, and measure the time from each trigger to the sound onset in the recording. Both are recorded **at the same time**, from the same trials.

## Status

The setup works end to end. Round 1 recorded 2026-09-29 and round 2 on 2026-10-06 (see "Round 2" at the end). **Next:** more recordings with a fixed noise seed; fix the trial matching in `biosemi.py`; investigate the electrotime recording gaps.

## Experiment script (`experiment/run.py`)

- **Odd triggers** (1, 3, 5, …): visual trial. Two white 250 px squares for 200 ms, one in the **centre** and one flush with the **bottom-right corner** at `(835, -415)`, for the photo sensors.
- **Even triggers** (2, 4, 6, …): sound trial. The screen stays black, and the sound starts on the same screen refresh as the trigger (`sound.play(when=win.getFutureFlipTime(clock='ptb'))`).
- Triggers start at 1, because 0 can't be seen on the port. The trigger pulse is 50 ms for both trial types. 100 trials, 2 s between trials.
- **Sound:** 200 ms of full-scale white noise, generated in code, 44100 Hz, mono, no fade-in (`hamming=False`). Its spectrum matches the 50 ms startle probe from HajcakFoti2008 (flat white noise); only the length differs.
- The `USE_TONE` switch (250 Hz sine tone for wiring tests) was used during setup and has since been removed from the script. To test wiring with a tone again, replace the noise with `Sound(250, secs=STIM_DUR_SEC, sampleRate=SAMPLE_RATE, stereo=False, hamming=False)`.

### Lessons from getting the sound to run on the lab PC

- The lab PC (Windows, standard PsychoPy 2024.2.4, **offline**) only gets code by USB, or by typing it in by hand, so keep changes small.
- The first version crashed with `TypeError: cannot unpack non-iterable NoneType object` when creating the sound. PsychoPy's PTB sound backend needs an **explicit `stereo=` argument** when the sound is an array; otherwise it never opens an audio stream. `../multisite-resting-state` does the same (`paradigm/utils/generic_stimuli.py:32`), citing PsychoPy issue #6765.
- We copied multisite-resting-state's setup: **44100 Hz, `stereo=False`**, and **no `prefs.hardware` settings** (PsychoPy uses PTB by default).

## Working setup (for rebuilding)

### Audio chain

```
PC headphone socket → slider cable 1 (at MAX) → splitter ─┬─ slider cable 2 → terminal plug → breadboard (100 Ω between signal and ground) → Biosemi
                                                          └─ audio cable → electrotime audio input
```

- **Windows volume** sets the level for the **electrotime**. **Slider cable 2** sets the level for the **Biosemi**, without affecting the electrotime branch.
- The **100 Ω resistor between signal and ground** is needed for slider cable 2 to work. The slider is apparently a variable series resistor, which only works when current flows through a load; the Biosemi draws practically none. Anything from 47 to 470 Ω works. It is **not** in series with the ground.
- **Water ends of the wires:** stripped copper ends, not Dupont pins. Dupont pins vary in metal and plating from batch to batch.
- Electrotime branch: a braided (3-contact) aux cable is safest. A 4-pole aux cable usually works too.

### Biosemi ("bucket test", no participant connected)

- Electrodes, including **CMS and DRL**, are in a bucket of salt water.
- The **ground wire's** copper end goes into the bucket.
- A separate **EXG electrode in the EXG1 socket** sits in a **small separate glass of salt water** (the "signal glass"), filled from the bucket, together with the **signal wire's** copper end. Keep the glass and the bucket apart.
- Don't plug jumpers straight into the EXG sockets: they're active electrode sockets, with power pins.
- **Fallback:** a **salt bridge** (paper towel or cloth soaked in the bucket water, from glass to bucket) keeps EXG1's offset normal if the wires alone don't. It still lets the tone through. Keep it wet; a cover over glass and bucket slows evaporation.

### Triggers

- The electrotime has only one trigger (DB37) connector, so a home-made **parallel port splitter** sits between the stimulus PC's trigger cable and both the electrotime and the Biosemi USB trigger box.
- If triggers are missing **entirely**, check the splitter's ground wire and connectors first; it was loose once. A single wrong data wire only gives wrong values.

### ActiView settings

- **Sample rate:** set by the speed mode switch on the AD box (mode 4 = 2048 Hz), further reduced in software with the **decimation** selector in the right sidebar. For example, 1/2 gives 1024 Hz. Note: 1024 Hz means about 1 ms per sample.
- **Channels to save:** channel setting including "+8", so EXG1–8 are saved. **Erg1** (photo sensor) must be **shown on the Sensors tab** and sensors must be saved (CFG: `[save]` section, `Sensors=1`). The triggers are always saved in the last channel, **Status**.
- Settings can be stored via About/Configure → Save CFG (`DEFAULT.CFG` loads at start-up).

## Quick setup check (before recording)

With the terminal plug **unplugged** from slider cable 2 (PC out of the loop):
1. **Ω between the two water-end wires** (lifted out of the water), on the 200 Ω range: about **100 Ω**. If it shows "1" or OL, look for a loose joint, especially in the breadboard (centre gap, wrong row, split side rails) and the terminal block.
2. **DC volts between glass and bucket** (meter probes in the water), on the DC 2V range: close to **0 V**. Hundreds of mV means trouble.
3. **EXG1 offset** in ActiView: normal (for example about 20). A small wiggle is fine; it settles over a few minutes.
4. If it's still high: put the **salt bridge** in.

Then, with the terminal plug plugged in:
5. Offset still normal, and the sound on EXG1 swings **both ways**, with no flat edge.
6. Triggers 1, 2, 3, … appear in both ActiView and the electrotime app.
7. Erg1 shows the photo sensor; noise bursts on EXG1 don't hit the edge of the range.

## Troubleshooting history and lessons

- **Multimeter:** the only AC range is 200V~, far too coarse for an audio output of under 1 V, and DC ranges read about 0 V on audio. Useful for **continuity/Ω** (with nothing else plugged in: earbuds and a connected PC also read as low resistance) and for **DC volts between liquids**.
- **Mic adapter (pink plug):** don't use. That plug is the microphone plug, with tip and ring joined.
- **High offset, one-sided signal on EXG1** (happened twice): EXG1's channel was pinned at the edge of its ±262 mV range. Both times, EXG1 in the bucket was normal and the cause was the connection between the glass and the bucket through the wires:
  - 2026-09-29: the jumper in the terminal block wasn't making contact, so the glass was floating.
  - 2026-10-06: the wiring measured fine, but the glass sat about 0.5 V (rising) away from the bucket. The salt bridge fixed it. After switching to copper ends and re-seating everything, it worked without the bridge as well. The exact cause wasn't pinned down: probably a connection re-seated while measuring, or the fresh copper ends.
  - **Lesson:** loose connections caused three of the problems (terminal block, parallel port splitter, probably the breadboard). Check joints first.
- **Display artefact:** ActiView shows a 250 Hz tone as a few slow waves when zoomed out; the recorded data is fine.
- **Aliasing** isn't a concern for finding onsets. The Biosemi has a built-in anti-aliasing filter (check the manual), and burst onsets remain detectable.

## Next steps

1. **Analysis script:** read the BDF, find each even trigger in **Status**, find the noise-burst onset on **EXG1** (for example, the first sample where the absolute value of the high-pass filtered signal exceeds a threshold), and compute the latency per trial. Compare with the electrotime's latencies for the same trials. Photo sensor on Erg1 for the visual trials, likewise.
2. The Biosemi's filter delay is fixed. Measure it once (or take it from the manual) and subtract it.

## Round 2 (2026-10-06, mkII, `~/data/electrotime/vs_biosemi_round2`)

### Setup
- Lab PC `run.py` (not yet in the repo): 10 runs of 100 in one loop, the electrotime square moved lower, ITI about 1 s (trials 1.18 s apart), trigger pulse about 27 ms. A 27 ms pulse over 3 flips means the monitor runs at about 110 to 120 Hz; check that this is intended.
- Sound and light look good on both devices. No clipping. EXG1 is about 108 mV peak to peak (−63 to +77 mV, ±262 mV range), with a baseline of 18 mV. The electrotime sound input spans 174 to 842 out of 0 to 1023. The electrotime light peaks at about 234, but its baseline is flat at 0. Audio levels don't need changing; keep them as they are, so the rounds stay comparable.
- BioSemi: all 1000 triggers, no bad values, every stimulus detected.

### Too few electrotime trials
- Each electrotime file holds only about 5.9 s, but files start about 19 s apart. So only about 31% of the time is recorded: 257 matched trials (about 28 per run, runs 2 to 10), and 181 after the 2 ms edge-gap rule. **This limits the trial count, not the wiring.** Check the GUI or device logging settings. Not checked: whether round 1 had the same gaps.

### Matching bug in `biosemi.py`
- Trigger values 1 to 100 repeat every run (about 118 s). The clock offset from the histogram mode landed exactly one run off. Signs: the same-trial sound delays didn't correlate (r = 0.03), and the pulse lengths didn't agree.
- With the match shifted by one run: sound r = 0.96, and both spreads are tight (see the table). `check_shift.py` tests this.
- **To do:** make the matching robust. For example, pick the offset where the same-trial sound delays or pulse lengths agree best. Recheck round 1 the same way.

### Results (ElectroTime − BioSemi, same trials, corrected match, edge gaps ≤ 2 ms)

| | Round 1 | Round 2 |
|---|---|---|
| Light | −7.6 ± 0.5 (median −7.5) ms | −3.5 ± 0.5 ms |
| Sound | −2.6 ± 2.1 (median −2.0) ms | −5.0 ± 0.9 ms |

- **Light:** BioSemi stayed at 28.3 ms; electrotime went from 20.7 to 24.9 ms. Moving the square lower cut the offset by about 4 ms. The remaining 3.5 ms means the electrotime sensor is probably still higher on the screen than the BioSemi sensor; part of it may be that the two sensors respond differently.
- **Sound:** the change is mostly a measurement effect. The BioSemi filter smooths the noise burst, so the onset at "20% of the trial's peak" depends on the burst's first few ms. Only the BioSemi threshold changed, round 2: 5% gives −2.8, 10% gives −3.1, 20% gives −5.0, 30% gives −5.7, and 10 × the baseline SD gives −2.4 ms (`check_threshold.py`).
- `run.py` makes a **new random burst each time it starts**. In round 1, each run was a separate start, so each had a different burst, which explains the larger spread. In round 2 all 10 runs played the same burst.

### For the next recordings
- Add `numpy.random.seed(0)` just before the `noise = ...` line in `run.py`, so every recording plays the same burst.
- Start the ActiView recording first, and stop electrotime last.

### Analysis ideas (later; no changes to `biosemi.py` yet)
- A lower BioSemi sound threshold (5 to 10% of the peak, or a multiple of the baseline SD) is less sensitive to the burst's shape: between 5% and 10%, the result changes by only 0.3 ms.
- Shape-independent: **template matching**. Pass the known burst (fixed seed) through a model of the BioSemi filter, then fit the lag per trial. This also takes care of the BioSemi filter delay.
- Alternative: give the stimulus a sharp start, at the cost of no longer being pure white noise.

### Files
- One-off scripts and their output are in `~/data/electrotime/vs_biosemi_round2/checks/`:
  - `run_round2.py` runs `biosemi.py` unchanged, with only the run/session tables patched (this output still has the wrong match).
  - `check_round2.py`: ranges and clipping.
  - `check_shift.py`: run-shift matching test.
  - `check_threshold.py`: BioSemi onset threshold.
- Run with: `env/bin/python <script> <folder with electro3.bdf and electrotime_datafiles/>`.

## Interpretation of the absolute latencies (2026-10-09)

Based on `vs_biosemi_round2/known_seed` (2026-10-06 afternoon, seed 0), same trials on both systems, analysed with `analysis/biosemi.py`. Interpretation only: the display's input lag and the audio output latency weren't measured directly.

### Timing of the run
- The data fits a display at about **120 Hz**: the trigger (flip 1 to flip 4, so 3 frames) lasts 27 ms on both systems, and the light is visible for 172–180 ms (3 frames + 150 ms sleep + waiting for the next frame). At 60 Hz these would be 50 ms and 200–217 ms.
- So the light lasts ~175 ms rather than 200 ms, and the trigger pulse is ~27 ms. This doesn't affect the latencies.
- Trials start 1.183 s apart: 1 s interval + 3 frames + 150 ms + waiting for the next frame. `run.py` now has the 1 s interval used in the lab.

### Light: ~25 ms (ElectroTime), ~28 ms (BioSemi)
- The trigger goes out as the flip completes, when the screen starts drawing the new frame from the top. Both squares are at y = −415 px (the bottom 250 of 1080 rows), which the screen reaches ~6–8 ms into a frame.
- The remaining ~17 ms is about two frames of display delay plus the time the pixels take to switch. That's typical for a Windows desktop with an ordinary monitor.
- About 4.5% of light trials (46) come exactly one frame earlier on both systems (~17 / ~20.5 ms). Their trigger pulses are normal, so the display occasionally showed the frame one frame sooner, rather than the trigger being late.
- The two sensors were at about the same height this time, so the −3.6 ms between the systems isn't from the screen's drawing order. Candidates: the sensors themselves (rise time, and where 20% of the peak falls), and a possible lag of the BioSemi analog channels behind the Status channel from its anti-aliasing filter (check the manual). That lag would also make BioSemi look later for sound.

### Sound: ~15 ms (ElectroTime), ~16.6 ms (BioSemi)
- `sound.play(when=win.getFutureFlipTime(...))` schedules the sound for the same flip as the trigger. With sample-accurate scheduling, the delay would be the same on every trial to well under 1 ms.
- Instead it is spread evenly over ~11 ms (ElectroTime 1st–99th percentile: 9.1–20.4 ms). This looks like the sound waiting for the next audio buffer of ~10 ms, probably because PsychoPy's audio backend isn't in Windows' exclusive low-latency mode. Not checked on the lab PC.
- Useful for validating ElectroTime: a wide range of real latencies, hence the meaningful same-trial correlation (r = 0.92). For an EEG experiment it means about ±5 ms of sound timing jitter.

### To confirm on the lab PC
- `win.getActualFrameRate()` and the monitor's refresh setting.
- The audio latency mode reported in PsychoPy's log.
