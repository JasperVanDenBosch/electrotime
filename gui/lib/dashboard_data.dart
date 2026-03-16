import 'package:latrec/ports.dart';

class DashboardData {
  final int epochCount;
  final int sampleCount;
  final Map<int, int> triggers;

  const DashboardData._({
    this.epochCount = 0,
    this.sampleCount = 0,
    this.triggers = const {},
  });

  factory DashboardData.empty() => const DashboardData._();

  DashboardData addEpoch(EpochResult result) {
    final merged = Map<int, int>.from(triggers);
    result.summary.triggers.forEach((k, v) {
      merged.update(k, (existing) => existing + v, ifAbsent: () => v);
    });
    return DashboardData._(
      epochCount: epochCount + 1,
      sampleCount: sampleCount + result.sampleCount,
      triggers: merged,
    );
  }
}
