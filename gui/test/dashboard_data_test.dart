import 'package:flutter_test/flutter_test.dart';
import 'package:latrec/analysis.dart';
import 'package:latrec/dashboard_data.dart';
import 'package:latrec/ports.dart';

EpochResult makeEpoch({int sampleCount = 0, Map<int, int> triggers = const {}}) {
  return EpochResult(
    sdFilename: 'test.txt',
    localFilename: 'local.txt',
    sampleCount: sampleCount,
    summary: EpochSummary(
      sampleCount: sampleCount,
      duration: 0.0,
      triggers: triggers,
    ),
  );
}

void main() {
  group('DashboardData.empty()', () {
    test('epochCount is 0', () {
      expect(DashboardData.empty().epochCount, 0);
    });

    test('sampleCount is 0', () {
      expect(DashboardData.empty().sampleCount, 0);
    });

    test('triggers is empty', () {
      expect(DashboardData.empty().triggers, isEmpty);
    });
  });

  group('DashboardData.addEpoch()', () {
    test('epochCount increments by 1', () {
      final d = DashboardData.empty().addEpoch(makeEpoch());
      expect(d.epochCount, 1);
    });

    test('sampleCount is summed correctly', () {
      final d = DashboardData.empty()
          .addEpoch(makeEpoch(sampleCount: 10))
          .addEpoch(makeEpoch(sampleCount: 5));
      expect(d.sampleCount, 15);
    });

    test('triggers from epoch added when no prior triggers', () {
      final d = DashboardData.empty().addEpoch(makeEpoch(triggers: {1: 3, 2: 7}));
      expect(d.triggers, {1: 3, 2: 7});
    });

    test('overlapping trigger keys are summed across epochs', () {
      final d = DashboardData.empty()
          .addEpoch(makeEpoch(triggers: {1: 2, 2: 4}))
          .addEpoch(makeEpoch(triggers: {1: 3, 2: 1}));
      expect(d.triggers, {1: 5, 2: 5});
    });

    test('disjoint trigger keys both appear', () {
      final d = DashboardData.empty()
          .addEpoch(makeEpoch(triggers: {1: 2}))
          .addEpoch(makeEpoch(triggers: {3: 5}));
      expect(d.triggers, {1: 2, 3: 5});
    });
  });
}
