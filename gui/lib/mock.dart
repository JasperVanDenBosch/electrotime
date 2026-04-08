import 'dart:async';
import 'dart:io';
import 'dart:math';
import 'package:latrec/analysis.dart';
import 'package:latrec/ports.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;

/// Returns a stream that emits realistic mock [EpochResult]s every 8 seconds,
/// simulating a connected device without requiring actual hardware.
Stream<EpochResult> mockRecordingStream() {
  final controller = StreamController<EpochResult>();
  final random = Random();
  int epochIndex = 0;
  int baseTs = 100000000; // starting timestamp in µs

  Timer? timer;

  Future<void> emitEpoch() async {
    epochIndex++;
    final sdFilename = 'REC${epochIndex.toString().padLeft(4, '0')}.csv';
    final baseName = sdFilename.contains('.')
        ? sdFilename.substring(0, sdFilename.lastIndexOf('.'))
        : sdFilename;
    final ts = Random().nextInt(9999);


    final lines = _generateEpochLines(random, baseTs);

    final Directory? downloadsDir = await getDownloadsDirectory();
    if (downloadsDir == null) {
      return;
    }
    final localFilename = 'electrotime_DEMO$ts\_$sdFilename.txt';
    final filepath = path.join(downloadsDir.path, localFilename);
    final sink = File(filepath).openWrite();
    for (final line in lines) {
      sink.writeln(line);
    }


    // Advance base timestamp by the generated epoch duration (~5.1s in µs)
    baseTs += 5100000;



    final summary = summarizeEpoch(lines);
    if (!controller.isClosed) {
      controller.add(EpochResult(
        sdFilename: sdFilename,
        localFilename: localFilename,
        sampleCount: lines.length,
        summary: summary,
      ));
    }
  }

  // Emit first epoch after a short delay, then every 8 seconds.
  Timer(const Duration(seconds: 2), () {
    if (controller.isClosed) return;
    emitEpoch();
    timer = Timer.periodic(const Duration(seconds: 8), (_) {
      if (controller.isClosed) {
        timer?.cancel();
        return;
      }
      emitEpoch();
    });
  });

  controller.onCancel = () {
    timer?.cancel();
  };

  return controller.stream;
}

/// Generates ~7300 CSV lines: `light,sound,status,timestamp`
List<String> _generateEpochLines(Random random, int startTs) {
  const sampleCount = 7300;
  const sampleIntervalUs = 700; // ~1428 Hz
  const triggerStatuses = [1, 2, 3, 4, 8, 16, 25, 67, 128, 133, 245];

  // Plan trigger runs: 4–6 runs scattered across the epoch.
  final runCount = 4 + random.nextInt(3); // 4, 5, or 6
  // Each run: start index and length
  final runs = <({int start, int length, int status})>[];
  final positions = <int>{};
  for (int r = 0; r < runCount; r++) {
    final runLen = 5 + random.nextInt(8); // 5–12
    // Pick a start that doesn't overlap existing runs (simple retry).
    int start;
    int attempts = 0;
    do {
      start = 200 + random.nextInt(sampleCount - 400);
      attempts++;
    } while (attempts < 20 && _overlaps(positions, start, runLen));
    for (int i = start; i < start + runLen; i++) {
      positions.add(i);
    }
    runs.add((
      start: start,
      length: runLen,
      status: triggerStatuses[random.nextInt(triggerStatuses.length)],
    ));
  }

  // Build a status array
  final statuses = List<int>.filled(sampleCount, 0);
  for (final run in runs) {
    for (int i = run.start; i < run.start + run.length && i < sampleCount; i++) {
      statuses[i] = run.status;
    }
  }

  final lines = <String>[];
  for (int i = 0; i < sampleCount; i++) {
    final light = 370 + random.nextInt(11) - 5; // 365–375
    final sound = 509 + random.nextInt(7) - 3;  // 506–512
    final status = statuses[i];
    final ts = startTs + i * sampleIntervalUs;
    lines.add('$light,$sound,$status,$ts,');
  }
  return lines;
}

bool _overlaps(Set<int> occupied, int start, int length) {
  for (int i = start; i < start + length; i++) {
    if (occupied.contains(i)) return true;
  }
  return false;
}
