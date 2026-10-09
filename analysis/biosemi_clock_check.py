"""
Check the ElectroTime -> BioSemi trial matching of biosemi.py, and measure PC_OFFSET_S.

Run biosemi.py first; this reads its derivatives/electrotime_trials.csv.

Why: biosemi.py matches each ElectroTime trial to the BioSemi trigger with the same
value (1-100) nearest to an approximate time based on a fixed offset between the
clocks of the two PCs (PC_OFFSET_S). Trigger values repeat every run (~118 s), so if
that offset is wrong by half a run or more (a clock was reset or synced, or another
laptop was used), the trials are matched to the wrong run. The trigger values still
agree, so nothing else catches this; it showed up only as same-trial delays that did
not correlate.

How: within an ElectroTime boot, device time maps smoothly onto BioSemi time. For
correct matches, a smooth clock fit leaves residuals below 1 ms. For matches off by
a whole run it does not, because the run length of the stimulus PC varies by a few
ms from run to run. The fit is:
- a cubic, as the device clock rate wanders (~15 ms off a straight line over 20 min,
  probably as the resonator warms up)
- per BDF file, as the BDF header start time has 1 s resolution
- on trials without a sampling gap before the trigger (gap_trigger_ms), as a trigger
  recorded late would bias it

It also prints the measured PC offset per boot (BioSemi PC clock - ElectroTime PC
clock, including the delay from GUI start to device boot): use it to set PC_OFFSET_S
in biosemi.py for new recordings. All boots should agree within a few seconds.

data: ~/data/electrotime/vs_biosemi_round2 (or the folder given as argument)
"""
import sys
import logging
from datetime import datetime
from os.path import expanduser, join
import numpy
import pandas
logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('electrotime')

CLOCK_DEGREE = 3
CLOCK_TOL_MS = 5  ## a correct match is within this of the clock fit
MIN_WITHIN_TOL = 0.9  ## warn if a smaller fraction of a boot's trials is within CLOCK_TOL_MS
MAX_EDGE_GAP_MS = 2  ## as in biosemi.py

data_dir = expanduser(sys.argv[1] if len(sys.argv) > 1 else '~/data/electrotime/vs_biosemi_round2')
out_dir = join(data_dir, 'derivatives')
et = pandas.read_csv(join(out_dir, 'electrotime_trials.csv'))
et = et[et.bs_index >= 0]


def session_s(session: str) -> float:
    """GUI session start in seconds since midnight (biosemi.py's time base)"""
    start = datetime.strptime(session, '%Y-%m-%dT%H%M%S')
    return (start - start.replace(hour=0, minute=0, second=0)).total_seconds()


def fit_clock(x: numpy.ndarray, y: numpy.ndarray):
    """Polynomial clock fit y = p(x) that ignores outliers; None if too few points"""
    keep = numpy.ones(len(x), bool)
    for tol_s in (0.5, 0.05, None):
        if keep.sum() < 3 * (CLOCK_DEGREE + 1):
            return None
        poly = numpy.polynomial.Polynomial.fit(x[keep], y[keep], CLOCK_DEGREE)
        if tol_s:
            keep = numpy.abs(y - poly(x)) < tol_s
    return poly


rows = []
for (session, boot, bdf), group in et.groupby(['session', 'boot', 'bs_bdf']):
    x, y = group.device_s.values, group.bs_wall_s.values
    fit = group.gap_trigger_ms.values <= MAX_EDGE_GAP_MS
    row = dict(session=session, boot=boot, bdf=bdf, n=len(group), n_fit=fit.sum(),
               pc_offset_s=numpy.median(y - x - session_s(session)))
    poly = fit_clock(x[fit], y[fit])
    if poly is None:
        log.warning(f'{session} boot {boot} {bdf}: too few trials for a clock fit')
    else:
        res_ms = (y[fit] - poly(x[fit])) * 1000
        row.update(
            drift_ppm=(numpy.polyfit(x, poly(x), 1)[0] - 1) * 1e6,
            residual_sd_ms=res_ms.std(), residual_max_ms=numpy.abs(res_ms).max(),
            within_tol=(numpy.abs(res_ms) < CLOCK_TOL_MS).mean(),
        )
        if row['within_tol'] < MIN_WITHIN_TOL:
            log.warning(f'{session} boot {boot} {bdf}: only {row["within_tol"]:.0%} of trials within '
                        f'{CLOCK_TOL_MS} ms of the clock fit; matches are probably off by whole runs')
    rows.append(row)
clock_df = pandas.DataFrame(rows)
clock_df.to_csv(join(out_dir, 'clock_fits.csv'), float_format='%.3f', index=False)
with pandas.option_context('display.width', 200, 'display.max_columns', 20, 'display.precision', 2):
    log.info(f'clock fits (residuals on trials without a gap before the trigger):\n{clock_df}')
