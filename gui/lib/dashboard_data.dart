import 'package:latrec/ports.dart';

class DashboardData {
  final int epochCount;
  final int sampleCount;

  const DashboardData._({this.epochCount = 0, this.sampleCount = 0});

  factory DashboardData.empty() => const DashboardData._();

  DashboardData addEpoch(EpochResult result) => this; // stub
}
