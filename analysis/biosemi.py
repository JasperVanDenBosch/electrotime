"""
Compare the latency of ElectroTime with
a Biosemi "photosensor" and audio signal routed to EXG 1.

data: ~/data/electrotime/vs_biosemi_round2 (recorded 2026-10-06, mkII only)
experiment: ./experiment/run.py
notes: ./experiment/audio-biosemi-notes.md

The data folder has one subfolder per sound stimulus (see STIMULI), each with
the BioSemi recordings (*.bdf) and the ElectroTime files recorded alongside:

- unknown_seed: electro3.bdf; the noise burst was generated without a seed
- known_seed: electro4.bdf and electro5.bdf; noise burst from seed 0

Each start of run.py plays 10 runs of 100 trials (one "block") with one noise burst.
Cross-correlating the BioSemi sound epochs confirms that all known_seed blocks
played the same burst, and that the unknown_seed burst differs from it.
Only the known_seed results go into the manuscript; unknown_seed is used to see
how the noise burst affects the measured sound latency.

Only trials recorded by both systems are analysed.

## electrotime data analysis
see analyse_goettingen.py for an example of how to analyse the electrotime data.

## biosemi data analysis
- read bdf
- drop channels except: Status (trigger), EXG1 (audio) and Erg1 (photosensor)
- after that the data has a similar shape so we follow the same approach

## matching trials
Trigger values 1-100 repeat every run (~118 s). An ElectroTime trial is matched to
the BioSemi trigger with the same value that is nearest to its approximate BioSemi
time: GUI session start + device time + PC_OFFSET_S. This needs to be right within
half a run (59 s); it is within 2.5 s for this data. If the offset is wrong by a run
or more, the matches are off by whole runs without any error, so check the matches
with biosemi_clock_check.py when the PCs or their clocks change.
"""
import re
import sys
import logging
from datetime import datetime
from glob import glob
from os import makedirs
from os.path import basename, expanduser, join
import numpy
import pandas
import seaborn
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import mne
matplotlib.use('agg')
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('electrotime')

## data subfolder: label of the sound stimulus
STIMULI = {'unknown_seed': 'noise, unknown seed', 'known_seed': 'noise, seed 0'}
MANUSCRIPT_STIMULUS = 'known_seed'
BS_SOUND_CH, BS_LIGHT_CH, BS_TRIGGER_CH = 'EXG1', 'Erg1', 'Status'
ET_LIGHT_COL, ET_SOUND_COL, ET_TRIGGER_COL, ET_TIME_COL = 0, 1, 2, 3
VALID_TRIGGERS = set(range(1, 101))
EPOCH_TMIN = -100  ## ms, start of epoch wrt trigger
EPOCH_TMAX = 300   ## ms, end of epoch wrt trigger
ONSET_FRACTION = 0.2  ## onset = first sample beyond this fraction of the peak
MIN_SNR = 10  ## peak deviation must exceed this many baseline SDs
ET_NOISE_FLOOR = 1  ## ADC counts; light baseline is often perfectly flat
MIN_TRIGGER_MS = 5  ## shorter non-zero trigger runs are glitches
BLOCK_GAP_S = 125  ## runs within a block start every ~118 s; a longer gap starts a new block
## BioSemi PC clock - ElectroTime PC clock (s), including the delay from GUI start to
## device boot; measured on 2026-10-06 with biosemi_clock_check.py (-561 to -563 s)
PC_OFFSET_S = -562
MATCH_TOL_S = 20  ## max time error of a match; same values recur every ~118 s
## Some samples are delayed due to SD issues
MAX_EDGE_GAP_MS = 2
COLORS = {'BioSemi': '#2a78d6', 'ElectroTime': '#eb6834', 'unknown_seed': '#4a3aa7', 'known_seed': '#1baf7a'}
## how the two systems are named in the latency figures (neutral, for the manuscript)
LABELS = {'BioSemi': 'Amplifier', 'ElectroTime': 'ElectroTime'}
INK, INK_MUTED = '#0b0b0b', '#52514e'
seaborn.set_theme(style='ticks', rc={
    'axes.edgecolor': INK_MUTED, 'axes.labelcolor': INK, 'text.color': INK,
    'xtick.color': INK_MUTED, 'ytick.color': INK_MUTED,
    'axes.spines.top': False, 'axes.spines.right': False,
})

data_dir = expanduser(sys.argv[1] if len(sys.argv) > 1 else '~/data/electrotime/vs_biosemi_round2')
out_dir = join(data_dir, 'derivatives')
plot_dir = join(out_dir, 'plots')
makedirs(plot_dir, exist_ok=True)


def modality_of(trigger: int) -> str:
    return 'light' if trigger % 2 == 1 else 'sound'


def find_onset(rel_ms: numpy.ndarray, signal: numpy.ndarray, noise_floor: float):
    """Return (onset_ms, normalised deviation) or (nan, None) without a clear response"""
    pre = rel_ms < 0
    post = ~pre
    baseline = numpy.median(signal[pre])
    noise = max(signal[pre].std(), noise_floor)
    dev = signal - baseline
    peak = numpy.abs(dev[post]).max()
    if peak < MIN_SNR * noise:
        return numpy.nan, None
    first = numpy.argmax(numpy.abs(dev[post]) > ONSET_FRACTION * peak)
    return rel_ms[post][first], dev / peak


def run_lengths(values: numpy.ndarray):
    """Start indices and values of runs of constant value"""
    starts = numpy.r_[0, numpy.flatnonzero(numpy.diff(values) != 0) + 1]
    return starts, values[starts]


def clock_str(wall_s: float) -> str:
    return f'{int(wall_s // 3600):02d}:{int(wall_s % 3600 // 60):02d}'


################################################################################
## BioSemi
################################################################################
bdfs = []
for stimulus in STIMULI:
    for bdf_path in glob(join(data_dir, stimulus, '*.bdf')):
        raw = mne.io.read_raw_bdf(bdf_path, preload=False, verbose='error')
        ## header time is local wall clock (1 s resolution); mne labels it UTC
        bdfs.append(dict(stimulus=stimulus, path=bdf_path, raw=raw,
                         start=raw.info['meas_date'].replace(tzinfo=None)))
bdfs.sort(key=lambda b: b['start'])
## all times below are in seconds since midnight, on each PC's own clock
day = bdfs[0]['start'].replace(hour=0, minute=0, second=0, microsecond=0)

bs_rows = []
run, block, last_run_start = -1, -1, -numpy.inf
for b in bdfs:
    raw, stimulus, bdf = b['raw'], b['stimulus'], basename(b['path'])
    fs = raw.info['sfreq']
    bdf_s = (b['start'] - day).total_seconds()
    bs_sound, bs_light, bs_status = raw.get_data(picks=[BS_SOUND_CH, BS_LIGHT_CH, BS_TRIGGER_CH])
    bs_trigger = bs_status.astype(numpy.int64) & 0xFF
    log.info(f'BioSemi: {bdf} ({stimulus}), {fs:.0f} Hz, {bs_trigger.size/fs:.0f} s from {b["start"]}')
    starts, values = run_lengths(bs_trigger)
    ends = numpy.r_[starts[1:], bs_trigger.size]
    in_run = False
    for start, end, value in zip(starts, ends, values):
        if value == 0:
            continue
        if value not in VALID_TRIGGERS:
            log.warning(f'BioSemi: unexpected trigger {value} at {start/fs:.3f} s in {bdf}')
            continue
        wall_s = bdf_s + start / fs
        if value == 1:
            run += 1
            in_run = True
            if not bs_rows or bs_rows[-1]['bdf'] != bdf or wall_s - last_run_start > BLOCK_GAP_S:
                block += 1
                block_start_s = wall_s
            last_run_start = wall_s
        if not in_run:
            log.warning(f'BioSemi: trigger {value} before the first run in {bdf}')
            continue
        modality = modality_of(value)
        i0, i1 = start + round(EPOCH_TMIN * fs / 1000), start + round(EPOCH_TMAX * fs / 1000)
        signal = bs_light if modality == 'light' else bs_sound
        rel_ms = numpy.arange(i0 - start, i1 - start) / fs * 1000
        delay, trace = find_onset(rel_ms, signal[i0:i1], 0)
        bs_rows.append(dict(
            bs_index=len(bs_rows), stimulus=stimulus, bdf=bdf, block=block,
            block_start_s=block_start_s, run=run, trigger=value, modality=modality,
            wall_s=wall_s, pulse_ms=(end - start) / fs * 1000, delay=delay, trace=(rel_ms, trace),
        ))
    del bs_sound, bs_light, bs_status, bs_trigger
bs = pandas.DataFrame(bs_rows)
run_starts = bs[bs.trigger == 1].wall_s.diff()
run_period = run_starts[run_starts < BLOCK_GAP_S].median()
log.info(f'BioSemi: {len(bs)} triggers in {run+1} runs and {block+1} blocks (run period {run_period:.2f} s), '
         f'{bs.delay.isna().sum()} without a detectable stimulus')


################################################################################
## ElectroTime
################################################################################
fname_pattern = re.compile(r'electrotime_(?P<session>[\d-]+T\d{6})_(?P<counter>\d{5})(?P<boot>\d{3})\.txt')
et_files = []
for stimulus in STIMULI:
    for fpath in glob(join(data_dir, stimulus, 'electrotime_*.txt')):
        parts = fname_pattern.match(basename(fpath)).groupdict()
        with open(fpath) as fhandle:
            lines = fhandle.read().splitlines()
        rows = []
        for line in lines[1:]:
            cells = line.strip().strip(',').split(',')
            if len(cells) == 4 and all(c.isdigit() for c in cells):
                rows.append([int(c) for c in cells])
        et_files.append(dict(
            file=basename(fpath), stimulus=stimulus, session=parts['session'], boot=parts['boot'],
            counter=int(parts['counter']), start_us=int(lines[0]), data=numpy.array(rows),
            bad_lines=len(lines) - 1 - len(rows),
        ))
et_files.sort(key=lambda f: (f['session'], f['boot'], f['counter']))
## the device clock (micros) wraps every 2^32 us (71.6 min); unwrap per boot
wraps = 0
for prev, f in zip([None] + et_files[:-1], et_files):
    if prev is None or (prev['session'], prev['boot']) != (f['session'], f['boot']):
        wraps = 0
    elif f['start_us'] + wraps * 2**32 < prev['start_us']:
        wraps += 1
    f['start_us'] += wraps * 2**32
log.info(f'ElectroTime: {len(et_files)} files, {sum(f["bad_lines"] for f in et_files)} malformed lines')

## Trigger runs: how did the triggers arrive?
trigger_runs = []
et_rows = []
for f in et_files:
    data = f['data']
    if data.size == 0:
        continue
    t_us = data[:, ET_TIME_COL]
    starts, values = run_lengths(data[:, ET_TRIGGER_COL])
    next_t = numpy.r_[t_us[starts[1:]], t_us[-1]]
    durations_ms = (next_t - t_us[starts]) / 1000
    n_samples = numpy.diff(numpy.r_[starts, len(t_us)])
    for start, value, duration, n in zip(starts, values, durations_ms, n_samples):
        if value == 0:
            kind = 'idle'
        elif duration < MIN_TRIGGER_MS:
            kind = 'glitch'
        elif value in VALID_TRIGGERS:
            kind = 'valid'
        else:
            kind = 'aberrant'
        trigger_runs.append(dict(
            stimulus=f['stimulus'], session=f['session'], file=f['file'], value=value, kind=kind,
            onset_ms=t_us[start] / 1000, duration_ms=duration, n_samples=n,
        ))
        if kind != 'valid':
            continue
        t0 = t_us[start]
        if t0 + EPOCH_TMIN * 1000 < t_us[0] or t0 + EPOCH_TMAX * 1000 > t_us[-1]:
            continue  ## epoch not fully inside this file
        mask = (t_us >= t0 + EPOCH_TMIN * 1000) & (t_us <= t0 + EPOCH_TMAX * 1000)
        rel_ms = (t_us[mask] - t0) / 1000
        modality = modality_of(value)
        col = ET_LIGHT_COL if modality == 'light' else ET_SOUND_COL
        delay, trace = find_onset(rel_ms, data[mask, col].astype(float), ET_NOISE_FLOOR)
        ## sample interval just before each edge = how late that edge may have been
        ## recorded (see MAX_EDGE_GAP_MS); start >= 1 because the epoch fits in the file
        gap_trigger_ms = (t0 - t_us[start - 1]) / 1000
        gap_onset_ms = numpy.nan
        if not numpy.isnan(delay):
            onset = numpy.searchsorted(t_us, t0 + round(delay * 1000))
            gap_onset_ms = (t_us[onset] - t_us[onset - 1]) / 1000
        et_rows.append(dict(
            stimulus=f['stimulus'], session=f['session'], boot=f['boot'], file=f['file'],
            trigger=value, modality=modality, device_s=(f['start_us'] + t0) / 1e6,
            pulse_ms=duration, delay=delay, trace=(rel_ms, trace),
            gap_trigger_ms=gap_trigger_ms, gap_onset_ms=gap_onset_ms,
        ))
runs_df = pandas.DataFrame(trigger_runs)
runs_df.to_csv(join(out_dir, 'electrotime_trigger_runs.csv'), float_format='%.3f', index=False)
et = pandas.DataFrame(et_rows)
log.info(f'ElectroTime: {len(et)} valid triggers with a full epoch')
## edge_ok: both edges were sampled without a long gap just before them.
## Trials without a detected onset (gap_onset_ms is NaN) are never edge_ok.
et['edge_ok'] = (et.gap_trigger_ms <= MAX_EDGE_GAP_MS) & (et.gap_onset_ms <= MAX_EDGE_GAP_MS)
detected = et.delay.notna()
log.info(f'ElectroTime: {(detected & ~et.edge_ok).sum()} of {detected.sum()} trials with a detected onset '
         f'have a sampling gap > {MAX_EDGE_GAP_MS} ms before the trigger or the onset')


################################################################################
## Match ElectroTime triggers to BioSemi triggers
################################################################################
## BioSemi trigger times per (stimulus, trigger value)
bs_lookup = {key: (g.wall_s.values, g.bs_index.values) for key, g in bs.groupby(['stimulus', 'trigger'])}


def nearest_bs(stimulus: str, triggers: numpy.ndarray, times: numpy.ndarray):
    """bs_index of the BioSemi trigger with the same value nearest in time
    (-1 if none within MATCH_TOL_S), and its time minus the given time (s)"""
    index = numpy.full(len(times), -1)
    err = numpy.full(len(times), numpy.nan)
    for i, (trigger, t) in enumerate(zip(triggers, times)):
        wall, idx = bs_lookup.get((stimulus, trigger), ([], []))
        if len(wall):
            j = numpy.abs(wall - t).argmin()
            err[i] = wall[j] - t
            if abs(err[i]) < MATCH_TOL_S:
                index[i] = idx[j]
    return index, err


## approximate: device time counts from boot, so this assumes a constant delay between
## GUI session start and device boot; biosemi_clock_check.py checks the resulting matches
session_s = et.session.map(lambda session: (datetime.strptime(session, '%Y-%m-%dT%H%M%S') - day).total_seconds())
et['bs_index'] = -1
et['match_error_s'] = numpy.nan
for stimulus, group in et.groupby('stimulus'):
    index, err = nearest_bs(stimulus, group.trigger.values, session_s[group.index] + group.device_s + PC_OFFSET_S)
    et.loc[group.index, 'bs_index'] = index
    et.loc[group.index, 'match_error_s'] = err
log.info(f'time error of the match per session (s):\n'
         f'{et.groupby("session").match_error_s.agg(["min", "max"]).round(2)}')

matched = et.bs_index >= 0
duplicates = et[matched & et.bs_index.duplicated(keep=False)]
if len(duplicates):
    log.warning(f'{len(duplicates)} ElectroTime triggers matched the same BioSemi trigger')
log.info(f'matched {matched.sum()} / {len(et)} ElectroTime triggers')
for col in ('bdf', 'block', 'block_start_s', 'run', 'wall_s', 'delay', 'pulse_ms'):
    et[f'bs_{col}'] = numpy.where(matched, bs[col].values[et.bs_index.clip(0)], numpy.nan)
et['difference'] = et.delay - et.bs_delay
bs['matched'] = bs.bs_index.isin(et.bs_index[matched])

## only trials recorded by both systems, with a detected stimulus on both;
## clean: without a sampling gap before an ElectroTime edge. The plots use clean.
pairs = et[matched & et.delay.notna() & et.bs_delay.notna()]
clean = pairs[pairs.edge_ok]
n_missing = (matched & (et.delay.isna() | et.bs_delay.isna())).sum()
log.info(f'{len(pairs)} matched trials with a detected stimulus on both systems '
         f'({n_missing} without), {len(clean)} without edge gaps')


################################################################################
## Tables
################################################################################
def describe(df: pandas.DataFrame, value: str, by: list) -> pandas.DataFrame:
    return df.groupby(by)[value].agg(['count', 'mean', 'std', 'min', 'median', 'max']).reset_index()


def correlation(df: pandas.DataFrame, by: list) -> pandas.DataFrame:
    """Pearson r between the same-trial delays of both systems"""
    return df.groupby(by).apply(lambda g: g.delay.corr(g.bs_delay), include_groups=False).rename('r').reset_index()


bs.drop(columns='trace').to_csv(join(out_dir, 'biosemi_trials.csv'), float_format='%.3f', index=False)
## µs precision: biosemi_clock_check.py fits the trigger times
et.drop(columns='trace').to_csv(join(out_dir, 'electrotime_trials.csv'), float_format='%.6f', index=False)
selections = (('all matched', pairs), (f'edge gaps <= {MAX_EDGE_GAP_MS} ms', clean))

## both systems summarised on the same trials
by = ['selection', 'stimulus', 'modality', 'system']
summary = pandas.concat([
    describe(pandas.concat([
        df.assign(system='BioSemi', delay=df.bs_delay),
        df.assign(system='ElectroTime'),
    ]).assign(selection=label), 'delay', by)
    for label, df in selections
])
summary.to_csv(join(out_dir, 'delay_summary.csv'), float_format='%.3f', index=False)
by = ['selection', 'stimulus', 'modality']
paired = pandas.concat([
    describe(df.assign(selection=label), 'difference', by).merge(correlation(df.assign(selection=label), by))
    for label, df in selections
])
paired.to_csv(join(out_dir, 'paired_difference.csv'), float_format='%.3f', index=False)

## for the manuscript: the trials shown in latency_<MANUSCRIPT_STIMULUS>.png
ms = clean[clean.stimulus == MANUSCRIPT_STIMULUS]
manuscript = ms.groupby('modality').agg(
    n=('delay', 'size'),
    amplifier_mean=('bs_delay', 'mean'), amplifier_sd=('bs_delay', 'std'), amplifier_median=('bs_delay', 'median'),
    electrotime_mean=('delay', 'mean'), electrotime_sd=('delay', 'std'), electrotime_median=('delay', 'median'),
    difference_mean=('difference', 'mean'), difference_sd=('difference', 'std'),
    difference_median=('difference', 'median'),
).reset_index().merge(correlation(ms, ['modality']))
manuscript.to_csv(join(out_dir, 'manuscript_table.csv'), float_format='%.2f', index=False)


def num(x: float, decimals: int = 1) -> str:
    return f'{x:.{decimals}f}'.replace('-', '\u2212')  ## typographic minus


## same table as HTML: open in a browser, copy and paste into Google Docs or Word
## to get a native table
html_rows = ''.join(
    f'<tr><td>{row.modality.capitalize()}</td><td>{row.n}</td>'
    + ''.join(f'<td>{num(getattr(row, f"{col}_mean"))} \u00b1 {num(getattr(row, f"{col}_sd"))}</td>'
              f'<td>{num(getattr(row, f"{col}_median"))}</td>'
              for col in ('amplifier', 'electrotime', 'difference'))
    + f'<td>{num(row.r, 2)}</td></tr>'
    for row in manuscript.itertuples()
)
with open(join(out_dir, 'manuscript_table.html'), 'w') as fhandle:
    fhandle.write(f"""<!doctype html><meta charset="utf-8"><title>Manuscript table</title>
<table border="1" cellpadding="4" style="border-collapse: collapse; text-align: center">
<tr><th rowspan="2"></th><th rowspan="2">n</th><th colspan="2">{LABELS['BioSemi']} delay (ms)</th>
<th colspan="2">{LABELS['ElectroTime']} delay (ms)</th>
<th colspan="2">{LABELS['ElectroTime']} \u2212 {LABELS['BioSemi']} (ms)</th><th rowspan="2">r</th></tr>
<tr><th>mean \u00b1 SD</th><th>median</th><th>mean \u00b1 SD</th><th>median</th><th>mean \u00b1 SD</th><th>median</th></tr>
{html_rows}
</table>
""")

## per block: does the noise burst change the measured latency?
by = ['bs_block', 'stimulus', 'modality']
blocks = (clean.groupby(by)
          .agg(start=('bs_block_start_s', 'first'), n=('delay', 'size'), biosemi_median=('bs_delay', 'median'),
               electrotime_median=('delay', 'median'), difference_mean=('difference', 'mean'),
               difference_std=('difference', 'std'))
          .reset_index().merge(correlation(clean, by)))
blocks['start'] = blocks.start.map(clock_str)
blocks.to_csv(join(out_dir, 'block_summary.csv'), float_format='%.3f', index=False)

## per session overview of the trigger channel
sessions = []
for (stimulus, session), group in runs_df.groupby(['stimulus', 'session']):
    files = [f for f in et_files if f['session'] == session and f['data'].size]
    recorded_s = sum(f['data'][-1, ET_TIME_COL] - f['data'][0, ET_TIME_COL] for f in files) / 1e6
    span_s = (max(f['start_us'] + f['data'][-1, ET_TIME_COL] for f in files)
              - min(f['start_us'] + f['data'][0, ET_TIME_COL] for f in files)) / 1e6
    n = group.kind.value_counts()
    sessions.append(dict(
        session=session, stimulus=stimulus, files=len(files), recorded_s=recorded_s,
        coverage=recorded_s / span_s, valid=n.get('valid', 0), glitch=n.get('glitch', 0),
        aberrant=n.get('aberrant', 0),
        aberrant_values=' '.join(str(v) for v in sorted(group[group.kind == 'aberrant'].value.unique())),
        matched=int(((et.session == session) & matched).sum()),
        valid_pulse_ms_median=group[group.kind == 'valid'].duration_ms.median(),
    ))
sessions_df = pandas.DataFrame(sessions)
sessions_df.to_csv(join(out_dir, 'electrotime_sessions.csv'), float_format='%.3f', index=False)

with pandas.option_context('display.width', 200, 'display.max_columns', 20, 'display.precision', 2):
    log.info(f'\nElectroTime trigger channel per session:\n{sessions_df}')
    log.info(f'\ndelay summary (ms), both systems on the same trials:\n{summary}')
    log.info(f'\nElectroTime - BioSemi delay (ms), same trials:\n{paired}')
    log.info(f'\nper block, {selections[1][0]}:\n{blocks}')
    log.info(f'\nmanuscript table ({MANUSCRIPT_STIMULUS}, {selections[1][0]}), ms:\n{manuscript}')
    pulse = pairs.assign(pulse_diff=pairs.pulse_ms - pairs.bs_pulse_ms)
    log.info(f'\ntrigger pulse duration ElectroTime - BioSemi (ms):\n{describe(pulse, "pulse_diff", ["stimulus"])}')


################################################################################
## Plots
################################################################################
## plot 1 is for the manuscript (one file per stimulus; only known_seed is used),
## 2 compares the noise bursts, 3-5 are trigger and sound-input diagnostics.
## All latency plots use `clean`: the same trials on both systems.
def system_view(df: pandas.DataFrame, system: str) -> pandas.DataFrame:
    """modality, delay and trace of the given system for the trials in df"""
    if system == 'ElectroTime':
        return df[['modality', 'delay', 'trace']]
    return pandas.DataFrame(dict(modality=df.modality.values, delay=df.bs_delay.values,
                                 trace=bs.trace.values[df.bs_index.values]))


## 1. latency figure (page size): one column per modality. Rows: the normalised traces
## of both systems aligned to the trigger, the delay of every trial, and the same-trial
## delays of both systems against each other. Without a title; the caption describes the data.
rng = numpy.random.default_rng(9)
systems = ('BioSemi', 'ElectroTime')
for stimulus in STIMULI:
    data = {system: system_view(clean[clean.stimulus == stimulus], system) for system in systems}
    ## one delay range for both modalities and systems (panels E-H)
    delays = clean[clean.stimulus == stimulus][['delay', 'bs_delay']]
    lo, hi = delays.min().min() - 2, delays.max().max() + 2
    plt.rcParams.update(seaborn.plotting_context('paper', font_scale=1.1))  ## page-width font sizes
    fig = plt.figure(figsize=(7.1, 9.6), layout='constrained')
    for c, (subfig, modality) in enumerate(zip(fig.subfigures(1, 2, wspace=0.04), ('light', 'sound'))):
        subfig.suptitle(modality.capitalize(), fontsize=12, fontweight='bold')
        axes = subfig.subplots(4, 1, height_ratios=(1, 1, 0.8, 1.9))
        letters = ['ABCDEFGH'[2 * r + c] for r in range(4)]  ## read across, then down
        ## traces, same time axis for both systems
        for r, system in enumerate(systems):
            ax = axes[r]
            sel = data[system][data[system].modality == modality]
            lines = [numpy.column_stack(t) for t in sel.trace]
            ax.add_collection(LineCollection(lines, colors=COLORS[system], alpha=0.15, linewidths=0.8))
            ax.axvline(0, color=INK_MUTED, linewidth=0.8)
            if len(sel):
                ax.axvline(sel.delay.median(), color=INK, linewidth=1, linestyle='--')
                ax.text(sel.delay.median() + 5, 1.35, f'median {sel.delay.median():.1f} ms',
                        color=INK, fontsize=8, va='top')
            ax.set_xlim(EPOCH_TMIN, EPOCH_TMAX)
            ax.set_ylim(-1.1, 1.4)
            ax.set_yticks([-1, 0, 1])
            ax.set_title(rf'$\bf{{{letters[r]}}}$   {LABELS[system]} (n={len(sel)})', fontsize=10, loc='left')
            ax.set_ylabel('normalised signal' if c == 0 else '')
        axes[0].tick_params(labelbottom=False)
        axes[1].set_xlabel('time from trigger (ms)')
        ## delay of every trial, both systems; black tick = median
        ax = axes[2]
        for y, system in enumerate(systems):
            d = data[system][data[system].modality == modality].delay
            ax.scatter(d, y + rng.uniform(-0.25, 0.25, d.size), s=6, color=COLORS[system], alpha=0.6, linewidth=0)
            if d.size:
                ax.plot(d.median(), y, '|', color=INK, markersize=16, mew=2)
        ax.set_yticks([0, 1], [LABELS[system] for system in systems])
        ax.set_xlim(lo, hi)
        ax.set_ylim(1.5, -0.5)
        ax.set_title(rf'$\bf{{{letters[2]}}}$   delay per trial', fontsize=10, loc='left')
        ax.set_xlabel('delay from trigger (ms)')
        ## same-trial delays; dashed line = equal delay
        ax = axes[3]
        sel = clean[(clean.stimulus == stimulus) & (clean.modality == modality)]
        ax.scatter(sel.bs_delay, sel.delay, s=8, color=INK, alpha=0.3, linewidth=0)
        ax.plot([lo, hi], [lo, hi], color=INK_MUTED, linewidth=0.8, linestyle='--')
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        if len(sel):
            ax.text(0.04, 0.96, f'r = {sel.delay.corr(sel.bs_delay):.2f}\n'
                    f'{LABELS["ElectroTime"]} - {LABELS["BioSemi"]}\n'
                    f'{sel.difference.mean():.1f} ± {sel.difference.std():.1f} ms',
                    transform=ax.transAxes, fontsize=8, va='top', color=INK)
        ax.set_aspect('equal')
        ax.set_title(rf'$\bf{{{letters[3]}}}$   same trials', fontsize=10, loc='left')
        ax.set_xlabel(f'{LABELS["BioSemi"]} delay (ms)')
        ax.set_ylabel(f'{LABELS["ElectroTime"]} delay (ms)')
    fig.savefig(join(plot_dir, f'latency_{stimulus}.png'), dpi=300)
    plt.close(fig)
    seaborn.set_context('notebook')

## 2. delays per block (one noise burst per block): BioSemi, ElectroTime, difference
block_list = sorted(clean.bs_block.unique())
fig, axes = plt.subplots(2, 3, figsize=(13, 6.5), sharex=True)
for r, modality in enumerate(('light', 'sound')):
    for c, (title, col) in enumerate(((f'{LABELS["BioSemi"]} delay', 'bs_delay'),
                                      ('ElectroTime delay', 'delay'),
                                      (f'ElectroTime - {LABELS["BioSemi"]}', 'difference'))):
        ax = axes[r, c]
        for x, blk in enumerate(block_list):
            d = clean[(clean.bs_block == blk) & (clean.modality == modality)]
            if not len(d):
                continue
            stimulus = d.stimulus.iloc[0]
            ax.scatter(x + rng.uniform(-0.25, 0.25, len(d)), d[col], s=6, color=COLORS[stimulus],
                       alpha=0.5, linewidth=0, label=STIMULI[stimulus])
            ax.plot(x, d[col].median(), '_', color=INK, markersize=18, mew=2)
        ax.set_title(f'{modality}: {title}', fontsize=10, loc='left')
        ax.set_ylabel('ms' if c == 0 else '')
        if r == 1:
            ax.set_xticks(range(len(block_list)),
                          [clock_str(clean[clean.bs_block == b].bs_block_start_s.iloc[0]) for b in block_list])
            ax.set_xlabel('block (start time)')
handles, labels = axes[1, 0].get_legend_handles_labels()
unique = dict(zip(labels, handles))
fig.legend(unique.values(), unique.keys(), frameon=False, fontsize=9, loc='upper right', markerscale=2)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(join(plot_dir, 'stimulus_blocks.png'), dpi=200)
plt.close(fig)

## 3. trigger channel per session: a 1.2 s excerpt around the first valid trigger
session_list = sorted(set(runs_df.session))
fig, axes = plt.subplots(len(session_list), 1, figsize=(10, 1.6 * len(session_list)), sharex=True)
for ax, session in zip(axes, session_list):
    valid = runs_df[(runs_df.session == session) & (runs_df.kind == 'valid')]
    files = [f for f in et_files if f['session'] == session and f['data'].size]
    if len(valid):
        f = next(f for f in files if f['file'] == valid.file.iloc[0])
        t_center = valid.onset_ms.iloc[0]
    else:
        f = files[len(files) // 2]
        t_center = 3000
    t_ms = f['data'][:, ET_TIME_COL] / 1000
    mask = (t_ms > t_center - 400) & (t_ms < t_center + 800)
    ax.step(t_ms[mask] - t_center, f['data'][mask, ET_TRIGGER_COL], where='post',
            color=COLORS['ElectroTime'], linewidth=1)
    ax.set_ylim(-10, 265)
    ax.set_yticks([0, 100, 255])
    ax.set_title(f'{session} ({f["stimulus"]}) {f["file"]}', fontsize=9, loc='left')
axes[-1].set_xlabel('time from first valid trigger in session (ms)')
fig.supylabel('trigger value')
fig.tight_layout()
fig.savefig(join(plot_dir, 'trigger_channel.png'), dpi=200)
plt.close(fig)

## 4. durations of non-idle trigger runs
fig, ax = plt.subplots(figsize=(8, 3.5))
for kind, linestyle in (('valid', '-'), ('aberrant', ':'), ('glitch', '--')):
    d = runs_df[runs_df.kind == kind]
    if len(d):
        ax.hist(d.duration_ms, bins=numpy.arange(0, 60, 1), histtype='step', linewidth=1.8,
                linestyle=linestyle, color=COLORS['ElectroTime'], label=f'{kind} (n={len(d)})')
ax.set_yscale('log')
ax.set_xlabel('duration of non-zero trigger value (ms)')
ax.set_ylabel('count')
ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(join(plot_dir, 'trigger_durations.png'), dpi=200)
plt.close(fig)

## 5. raw ElectroTime sound channel around the first sound trigger of each stimulus
fig, axes = plt.subplots(len(STIMULI), 1, figsize=(10, 4.5), sharex=True, sharey=True)
for ax, stimulus in zip(axes, STIMULI):
    row = et[(et.stimulus == stimulus) & (et.modality == 'sound')].iloc[0]
    f = next(f for f in et_files if f['file'] == row.file)
    t_ms = (f['data'][:, ET_TIME_COL] - (row.device_s * 1e6 - f['start_us'])) / 1000
    mask = (t_ms > -400) & (t_ms < 800)
    ax.plot(t_ms[mask], f['data'][mask, ET_SOUND_COL], color=COLORS[stimulus], linewidth=0.6)
    ax.axvline(0, color=INK_MUTED, linewidth=0.8)
    ax.set_title(f'{STIMULI[stimulus]}: sound input, trigger {row.trigger}, {row.file}', fontsize=9, loc='left')
    ax.set_ylabel('ADC value')
    ax.set_ylim(-20, 1043)
axes[-1].set_xlabel('time from sound trigger (ms)')
fig.tight_layout()
fig.savefig(join(plot_dir, 'sound_channel.png'), dpi=200)
plt.close(fig)

log.info(f'\nwrote tables to {out_dir} and plots to {plot_dir}')
