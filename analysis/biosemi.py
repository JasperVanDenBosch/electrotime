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
- drop channels except: Status (trigger), EXG1 (audio) and Erg1 (photosensor)
- after that the data has a similar shape so we follow the same approach

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

## BioSemi runs in recording order: (device, stimulus); see lab notes above
BIOSEMI_RUNS = [('mkIII', 'tone')] + [('mkIII', 'noise')] * 4 + [('mkII', 'noise')] * 5
## Which ElectroTime device was recording in each GUI session
SESSION_DEVICE = {
    '2026-09-29T205435': 'mkIII',
    '2026-09-29T210142': 'mkIII',
    '2026-09-29T210622': 'mkIII',
    '2026-09-29T211340': 'mkII',
    '2026-09-29T212014': 'mkII',
}
## skip mkIII recordings and pure tone stimulus
ANALYSED = [('mkII', 'noise')]
BS_SOUND_CH, BS_LIGHT_CH, BS_TRIGGER_CH = 'EXG1', 'Erg1', 'Status'
ET_LIGHT_COL, ET_SOUND_COL, ET_TRIGGER_COL, ET_TIME_COL = 0, 1, 2, 3
VALID_TRIGGERS = set(range(1, 101))
EPOCH_TMIN = -100  ## ms, start of epoch wrt trigger
EPOCH_TMAX = 300   ## ms, end of epoch wrt trigger
ONSET_FRACTION = 0.2  ## onset = first sample beyond this fraction of the peak
MIN_SNR = 10  ## peak deviation must exceed this many baseline SDs
ET_NOISE_FLOOR = 1  ## ADC counts; light baseline is often perfectly flat
MIN_TRIGGER_MS = 5  ## shorter non-zero trigger runs are glitches
MATCH_TOL_S = 20  ## max deviation from the clock offset; same values recur every ~2 min
## Some samples are delayed due to SD issues
MAX_EDGE_GAP_MS = 2
COLORS = {'BioSemi': '#2a78d6', 'ElectroTime': '#eb6834', 'mkII': '#1baf7a', 'mkIII': '#4a3aa7'}
MARKERS = {'mkII': 'o', 'mkIII': '^'}
## how the two systems are named in the latency figures (neutral, for the manuscript)
LABELS = {'BioSemi': 'Amplifier', 'ElectroTime': 'ElectroTime'}
INK, INK_MUTED = '#0b0b0b', '#52514e'
seaborn.set_theme(style='ticks', rc={
    'axes.edgecolor': INK_MUTED, 'axes.labelcolor': INK, 'text.color': INK,
    'xtick.color': INK_MUTED, 'ytick.color': INK_MUTED,
    'axes.spines.top': False, 'axes.spines.right': False,
})

data_dir = expanduser(sys.argv[1] if len(sys.argv) > 1 else '~/data/electrotime/vs_biosemi')
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


################################################################################
## BioSemi
################################################################################
bdf_path = glob(join(data_dir, '*.bdf'))[0]
raw = mne.io.read_raw_bdf(bdf_path, preload=False, verbose='error')
fs = raw.info['sfreq']
## header time is local wall clock; mne labels it UTC
bdf_start = raw.info['meas_date'].replace(tzinfo=None)
bs_sound, bs_light, bs_status = raw.get_data(picks=[BS_SOUND_CH, BS_LIGHT_CH, BS_TRIGGER_CH])
bs_trigger = bs_status.astype(numpy.int64) & 0xFF
log.info(f'BioSemi: {basename(bdf_path)}, {fs:.0f} Hz, {bs_trigger.size/fs:.0f} s from {bdf_start}')

starts, values = run_lengths(bs_trigger)
ends = numpy.r_[starts[1:], bs_trigger.size]
bs_rows = []
run = -1
for start, end, value in zip(starts, ends, values):
    if value == 0:
        continue
    if value not in VALID_TRIGGERS:
        log.warning(f'BioSemi: unexpected trigger {value} at {start/fs:.3f} s')
        continue
    if value == 1:
        run += 1
    device, stimulus = BIOSEMI_RUNS[run]
    modality = modality_of(value)
    i0, i1 = start + round(EPOCH_TMIN * fs / 1000), start + round(EPOCH_TMAX * fs / 1000)
    signal = bs_light if modality == 'light' else bs_sound
    rel_ms = numpy.arange(i0 - start, i1 - start) / fs * 1000
    delay, trace = find_onset(rel_ms, signal[i0:i1], 0)
    bs_rows.append(dict(
        bs_index=len(bs_rows), run=run, device=device, stimulus=stimulus,
        trigger=value, modality=modality, time_s=start / fs,
        pulse_ms=(end - start) / fs * 1000, delay=delay, trace=(rel_ms, trace),
    ))
bs = pandas.DataFrame(bs_rows)
if run + 1 != len(BIOSEMI_RUNS):
    log.warning(f'BioSemi: found {run+1} runs, expected {len(BIOSEMI_RUNS)}')
log.info(f'BioSemi: {len(bs)} triggers in {run+1} runs, '
         f'{bs.delay.isna().sum()} without a detectable stimulus')


################################################################################
## ElectroTime
################################################################################
fname_pattern = re.compile(r'electrotime_(?P<session>[\d-]+T\d{6})_(?P<counter>\d{5})(?P<boot>\d{3})\.txt')
et_files = []
for fpath in glob(join(data_dir, 'electrotime_datafiles', 'electrotime_*.txt')):
    parts = fname_pattern.match(basename(fpath)).groupdict()
    with open(fpath) as fhandle:
        lines = fhandle.read().splitlines()
    rows = []
    for line in lines[1:]:
        cells = line.strip().strip(',').split(',')
        if len(cells) == 4 and all(c.isdigit() for c in cells):
            rows.append([int(c) for c in cells])
    et_files.append(dict(
        file=basename(fpath), session=parts['session'], boot=parts['boot'],
        counter=int(parts['counter']), start_us=int(lines[0]), data=numpy.array(rows),
        bad_lines=len(lines) - 1 - len(rows),
    ))
et_files.sort(key=lambda f: (f['session'], f['start_us'], f['counter']))
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
            session=f['session'], file=f['file'], value=value, kind=kind,
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
            session=f['session'], boot=f['boot'], file=f['file'],
            session_device=SESSION_DEVICE.get(f['session'], 'unknown'),
            trigger=value, modality=modality, device_s=(f['start_us'] + t0) / 1e6,
            pulse_ms=duration, delay=delay, trace=(rel_ms, trace),
            gap_trigger_ms=gap_trigger_ms, gap_onset_ms=gap_onset_ms,
        ))
runs_df = pandas.DataFrame(trigger_runs)
runs_df['device'] = runs_df.session.map(SESSION_DEVICE).fillna('unknown')
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
session_offset_s = numpy.array([
    (datetime.strptime(s, '%Y-%m-%dT%H%M%S') - bdf_start).total_seconds() for s in et.session
])
## approximate: assumes the device booted when the GUI session started
et['approx_s'] = session_offset_s + et.device_s
diffs = numpy.concatenate([
    bs.time_s[bs.trigger == row.trigger].values - row.approx_s for row in et.itertuples()
])
counts, edges = numpy.histogram(diffs, bins=numpy.arange(diffs.min(), diffs.max() + 2, 1))
mode = edges[counts.argmax()] + 0.5
clock_offset = numpy.median(diffs[numpy.abs(diffs - mode) < MATCH_TOL_S])
log.info(f'clock offset BioSemi PC - ElectroTime PC: {clock_offset:.1f} s')

et['bs_index'] = -1
for i, row in et.iterrows():
    candidates = bs[bs.trigger == row.trigger]
    err = numpy.abs(candidates.time_s - row.approx_s - clock_offset)
    if err.min() < MATCH_TOL_S:
        et.loc[i, 'bs_index'] = candidates.bs_index.iloc[err.argmin()]
duplicates = et[(et.bs_index >= 0) & et.bs_index.duplicated(keep=False)]
if len(duplicates):
    log.warning(f'{len(duplicates)} ElectroTime triggers matched the same BioSemi trigger')
matched = et.bs_index >= 0
log.info(f'matched {matched.sum()} / {len(et)} ElectroTime triggers')

## per boot: linear clock fit, gives Arduino drift and trigger timing agreement
et['clock_residual_ms'] = numpy.nan
clock_rows = []
for (session, boot), group in et[matched].groupby(['session', 'boot']):
    bs_time = bs.time_s.values[group.bs_index.values]
    ## fit only on triggers seen without a gap before them; a trigger recorded late
    ## would bias the fit (residuals are still stored for every matched trigger)
    fit = (group.gap_trigger_ms <= MAX_EDGE_GAP_MS).values
    row = dict(session=session, boot=boot, n=len(group), n_fit=fit.sum(),
               device=SESSION_DEVICE.get(session, 'unknown'))
    if fit.sum() >= 3:
        slope, intercept = numpy.polyfit(group.device_s[fit], bs_time[fit], 1)
        residual_ms = (bs_time - (slope * group.device_s + intercept)) * 1000
        et.loc[group.index, 'clock_residual_ms'] = residual_ms
        row.update(drift_ppm=(slope - 1) * 1e6, residual_sd_ms=residual_ms[fit].std(),
                   residual_max_ms=numpy.abs(residual_ms[fit]).max())
    clock_rows.append(row)
clock_df = pandas.DataFrame(clock_rows)
clock_df.to_csv(join(out_dir, 'clock_fits.csv'), float_format='%.3f', index=False)

for col in ('run', 'device', 'stimulus', 'time_s', 'delay', 'pulse_ms'):
    et[f'bs_{col}'] = numpy.where(matched, bs[col].values[et.bs_index.clip(0)], numpy.nan)
mismatch = et[matched & (et.bs_device != et.session_device)]
if len(mismatch):
    log.warning(f'{len(mismatch)} matches disagree with SESSION_DEVICE')
et['difference'] = et.delay - et.bs_delay


################################################################################
## Tables
################################################################################
def describe(df: pandas.DataFrame, value: str, by: list) -> pandas.DataFrame:
    return df.groupby(by)[value].agg(['count', 'mean', 'std', 'min', 'median', 'max']).reset_index()


def in_analysis(df: pandas.DataFrame, device: str, stimulus: str) -> pandas.Series:
    """True for rows whose (device, stimulus) is one of ANALYSED"""
    return pandas.Series(list(zip(df[device], df[stimulus])), index=df.index).isin(ANALYSED)


## latency comparison: only the ANALYSED groups
bs_an = bs[in_analysis(bs, 'device', 'stimulus')]
## ElectroTime results are reported twice: for all matched trials, and for the
## trials left after dropping those with a sampling gap before an edge (et_clean).
## The plots use et_clean.
et_matched = et[matched & in_analysis(et, 'bs_device', 'bs_stimulus')]
et_clean = et_matched[et_matched.edge_ok]
bs_an.drop(columns='trace').to_csv(join(out_dir, 'biosemi_trials.csv'), float_format='%.3f', index=False)
et_matched.drop(columns='trace').to_csv(join(out_dir, 'electrotime_trials.csv'), float_format='%.3f', index=False)
clean_label = f'edge gaps <= {MAX_EDGE_GAP_MS} ms'
et_selections = (('all matched', et_matched), (clean_label, et_clean))
by = ['system', 'selection', 'device', 'stimulus', 'modality']
summary = pandas.concat(
    [describe(bs_an.assign(system='BioSemi', selection='all'), 'delay', by)]
    + [describe(df.assign(system='ElectroTime', selection=label, device=df.bs_device, stimulus=df.bs_stimulus),
                'delay', by) for label, df in et_selections]
)
summary.to_csv(join(out_dir, 'delay_summary.csv'), float_format='%.3f', index=False)
paired = pandas.concat([
    describe(df.dropna(subset=['difference']).assign(selection=label), 'difference',
             ['selection', 'bs_device', 'bs_stimulus', 'modality'])
    for label, df in et_selections
])
paired.to_csv(join(out_dir, 'paired_difference.csv'), float_format='%.3f', index=False)

## per session overview of the trigger channel
sessions = []
for session, group in runs_df.groupby('session'):
    seconds = group.groupby('file').onset_ms.max().sum() / 1000
    n = group.kind.value_counts()
    sessions.append(dict(
        session=session, device=SESSION_DEVICE.get(session, 'unknown'), recorded_s=seconds,
        valid=n.get('valid', 0), glitch=n.get('glitch', 0), aberrant=n.get('aberrant', 0),
        aberrant_values=' '.join(str(v) for v in sorted(group[group.kind == 'aberrant'].value.unique())),
        aberrant_per_s=n.get('aberrant', 0) / seconds,
        matched=int(((et.session == session) & matched).sum()),
        valid_pulse_ms_median=group[group.kind == 'valid'].duration_ms.median(),
    ))
sessions_df = pandas.DataFrame(sessions)
sessions_df.to_csv(join(out_dir, 'electrotime_sessions.csv'), float_format='%.3f', index=False)

with pandas.option_context('display.width', 200, 'display.max_columns', 20, 'display.precision', 2):
    log.info(f'\nElectroTime trigger channel per session:\n{sessions_df}')
    log.info(f'\nclock fits:\n{clock_df}')
    log.info(f'\ndelay summary (ms):\n{summary}')
    log.info(f'\nElectroTime - BioSemi delay (ms), matched trials:\n{paired}')
    pulse = et_matched.assign(pulse_diff=et_matched.pulse_ms - et_matched.bs_pulse_ms)
    log.info(f'\ntrigger pulse duration ElectroTime - BioSemi (ms):\n'
             f'{describe(pulse, "pulse_diff", ["session_device"])}')


################################################################################
## Plots
################################################################################
## plots 1 and 3 show the latency comparison (ANALYSED groups); plots 4-6 are
## trigger and sound-input diagnostics for both devices (see the hardware doc)
devices = sorted({device for device, _ in ANALYSED})

## 1. latency figure (for the manuscript): per modality, the normalised traces of
## both systems aligned to the trigger (A, B, D, E) and the delay of every trial
## (C, F). One file per ANALYSED group, without a title; the caption describes the data.
rng = numpy.random.default_rng(9)
systems = ('BioSemi', 'ElectroTime')
for device, stimulus in ANALYSED:
    data = {
        'BioSemi': bs_an[(bs_an.device == device) & (bs_an.stimulus == stimulus)],
        'ElectroTime': et_clean[(et_clean.bs_device == device) & (et_clean.bs_stimulus == stimulus)],
    }
    fig, axes = plt.subplots(2, 3, figsize=(12, 5.5))
    letters = iter('ABCDEF')
    for r, modality in enumerate(('light', 'sound')):
        for c, system in enumerate(systems):
            ax = axes[r, c]
            sel = data[system][(data[system].modality == modality) & data[system].delay.notna()]
            lines = [numpy.column_stack(t) for t in sel.trace]
            ax.add_collection(LineCollection(lines, colors=COLORS[system], alpha=0.15, linewidths=0.8))
            ax.axvline(0, color=INK_MUTED, linewidth=0.8)
            if len(sel):
                ax.axvline(sel.delay.median(), color=INK, linewidth=1, linestyle='--')
                ax.text(sel.delay.median() + 5, 1.12, f'median {sel.delay.median():.1f} ms',
                        color=INK, fontsize=8, va='top')
            ax.set_xlim(EPOCH_TMIN, EPOCH_TMAX)
            ax.set_ylim(-1.1, 1.15)
            ax.set_title(rf'$\bf{{{next(letters)}}}$   {LABELS[system]} (n={len(sel)})', fontsize=10, loc='left')
            ax.set_ylabel(f'{modality.capitalize()}\nnormalised signal' if c == 0 else '')
            if c:
                ax.set_yticklabels([])
            ax.set_xlabel('time from trigger (ms)' if r == 1 else '')
        ## delay of every trial, both systems; black tick = median
        ax = axes[r, 2]
        for y, system in enumerate(systems):
            d = data[system][data[system].modality == modality].delay.dropna()
            ax.scatter(d, y + rng.uniform(-0.25, 0.25, d.size), s=8, color=COLORS[system], alpha=0.6, linewidth=0)
            if d.size:
                ax.plot(d.median(), y, '|', color=INK, markersize=18, mew=2)
        ax.set_yticks([0, 1], [LABELS[system] for system in systems])
        ax.set_ylim(1.5, -0.5)
        ax.set_title(rf'$\bf{{{next(letters)}}}$   delay per trial', fontsize=10, loc='left')
        ax.set_xlabel('delay from trigger (ms)' if r == 1 else '')
    fig.tight_layout()
    fig.savefig(join(plot_dir, f'latency_{device}_{stimulus}.png'), dpi=300)
    plt.close(fig)

## 3. paired comparison of matched trials (et_clean)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for c, modality in enumerate(('light', 'sound')):
    sel = et_clean[(et_clean.modality == modality)].dropna(subset=['difference'])
    ax = axes[0, c]
    for device in devices:
        d = sel[sel.bs_device == device]
        ax.scatter(d.bs_delay, d.delay, s=28, marker=MARKERS[device], color=COLORS[device],
                   edgecolor='white', linewidth=0.8, label=f'{device} (n={len(d)})')
    if len(sel):
        lim = [min(sel.bs_delay.min(), sel.delay.min()) - 2, max(sel.bs_delay.max(), sel.delay.max()) + 2]
        ax.plot(lim, lim, color=INK_MUTED, linewidth=0.8, linestyle='--')
    ax.set_xlabel(f'{LABELS["BioSemi"]} delay (ms)')
    ax.set_ylabel('ElectroTime delay (ms)')
    ax.set_title(f'{modality}: same trials', fontsize=10, loc='left')
    ax.legend(frameon=False, fontsize=8)
    ax = axes[1, c]
    for device in devices:
        d = sel[sel.bs_device == device]
        if len(d):
            ax.hist(d.difference, bins=numpy.arange(-30, 30.5, 1), histtype='step', linewidth=2,
                    color=COLORS[device], label=f'{device} median {d.difference.median():.1f} ms')
    ax.axvline(0, color=INK_MUTED, linewidth=0.8)
    ax.set_xlabel(f'ElectroTime - {LABELS["BioSemi"]} (ms)')
    ax.set_ylabel('trials')
    ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(join(plot_dir, 'paired.png'), dpi=200)
plt.close(fig)

## 4. trigger channel per session: a 1.2 s excerpt around the first valid trigger
session_list = [s for s in SESSION_DEVICE if s in set(runs_df.session)]
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
            color=COLORS[SESSION_DEVICE[session]], linewidth=1)
    ax.set_ylim(-10, 265)
    ax.set_yticks([0, 100, 255])
    ax.set_title(f'{session} ({SESSION_DEVICE[session]}) {f["file"]}', fontsize=9, loc='left')
axes[-1].set_xlabel('time from first valid trigger in session (ms)')
fig.supylabel('trigger value')
fig.tight_layout()
fig.savefig(join(plot_dir, 'trigger_channel.png'), dpi=200)
plt.close(fig)

## 5. durations of non-idle trigger runs, per device
fig, ax = plt.subplots(figsize=(8, 3.5))
nonidle = runs_df[(runs_df.kind != 'idle') & runs_df.device.isin(['mkII', 'mkIII'])]
for device in ('mkIII', 'mkII'):
    for kind, linestyle in (('valid', '-'), ('aberrant', ':'), ('glitch', '--')):
        d = nonidle[(nonidle.device == device) & (nonidle.kind == kind)]
        if len(d):
            ax.hist(d.duration_ms, bins=numpy.arange(0, 60, 1), histtype='step', linewidth=1.8,
                    linestyle=linestyle, color=COLORS[device], label=f'{device} {kind} (n={len(d)})')
ax.set_yscale('log')
ax.set_xlabel('duration of non-zero trigger value (ms)')
ax.set_ylabel('count')
ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(join(plot_dir, 'trigger_durations.png'), dpi=200)
plt.close(fig)

## 6. raw sound channel around the first sound trigger of each device
fig, axes = plt.subplots(2, 1, figsize=(10, 4.5), sharex=True, sharey=True)
for ax, device in zip(axes, ('mkIII', 'mkII')):
    row = et[(et.session_device == device) & (et.modality == 'sound')].iloc[0]
    f = next(f for f in et_files if f['file'] == row.file)
    t_ms = (f['data'][:, ET_TIME_COL] - (row.device_s * 1e6 - f['start_us'])) / 1000
    mask = (t_ms > -400) & (t_ms < 800)
    ax.plot(t_ms[mask], f['data'][mask, ET_SOUND_COL], color=COLORS[device], linewidth=0.6)
    ax.axvline(0, color=INK_MUTED, linewidth=0.8)
    ax.set_title(f'{device} sound input (A0), trigger {row.trigger}, {row.file}', fontsize=9, loc='left')
    ax.set_ylabel('ADC value')
    ax.set_ylim(-20, 1043)
axes[-1].set_xlabel('time from sound trigger (ms)')
fig.tight_layout()
fig.savefig(join(plot_dir, 'sound_channel.png'), dpi=200)
plt.close(fig)

log.info(f'\nwrote tables to {out_dir} and plots to {plot_dir}')
