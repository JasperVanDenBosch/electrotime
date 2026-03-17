/*
  ## Wishlist

	- [ ] nr of triggers, break down by nr, sort by count. hashmap?
		- [ ] have to keep track of changed value
	- [ ] distribution of light? 1024/20
	- [ ] total duration by sound by bin
		- [ ] subtract 512 and abs.
		- [ ] may have to weigh by amplitude. Even high amplitude has lower values
		- [ ] or average over 10 samples?

220,510,0,251350588,
218,510,0,251359392,
217,510,0,251360084,

*/

class EpochSummary {
  final int sampleCount;
  // duration in seconds; difference between timestamp of first and last sample
  final double duration;
  // key: unique trigger, value: count
  final Map<int, int> triggers;

  const EpochSummary({
    required this.sampleCount,
    required this.duration,
    required this.triggers,
  });
}

EpochSummary summarizeEpoch(List<String> lines) {

  List<String> cells = [];
  int light = 0;
  int sound = 0;
  int status = 0;
  int ts = 0;
  int lastStatus = 0;
  String line = '';
  Map<int, int> triggers = new Map();
  int firstTs = -1;
  int lastTs = -1;
  for (int l = 0; l < lines.length; l++) {
    line = lines[l];
    cells = line.split(',');
    if (cells.length >= 4) {
      light = int.parse(cells[0]);
      sound = int.parse(cells[1]);
      status = int.parse(cells[2]);
      ts = int.parse(cells[3]);
      if (status != lastStatus) {
        triggers.update(status, (val) => val + 1, ifAbsent: () => 1);
        lastStatus = status;
      }
      if (l == 0) {
        firstTs = ts;
      }
      if (l == (lines.length - 1)) {
        lastTs = ts;
      }
    }
  }

  return EpochSummary(
    sampleCount: lines.length,
    duration: (lastTs - firstTs) / 1e6,
    triggers: triggers
  );
}