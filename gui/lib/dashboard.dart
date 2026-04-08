import 'package:flutter/material.dart';
import 'package:latrec/counter.dart';
import 'package:latrec/dashboard_data.dart';

class Dashboard extends StatelessWidget {
  final DashboardData data;

  const Dashboard({super.key, required this.data});

  Widget _buildTriggerRow(BuildContext context, MapEntry<int, int> entry) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3),
      child: Align(
        alignment: Alignment.centerRight,
        child: Counter(value: entry.value, label: '${entry.key}'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (data.epochCount == 0) return const SizedBox.shrink();

    final sortedTriggers = data.triggers.entries.toList()
      ..sort((a, b) => a.key.compareTo(b.key));

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Counter(value: data.epochCount, label: 'EPOCHS', labelPosition: LabelPosition.below),
            const SizedBox(width: 16),
            Counter(value: data.sampleCount, label: 'SAMPLES', labelPosition: LabelPosition.below),
          ],
        ),
        const Divider(),
        Expanded(
          child: ListView.builder(
            itemCount: sortedTriggers.length,
            itemBuilder: (context, i) => _buildTriggerRow(context, sortedTriggers[i]),
          ),
        ),
      ],
    );
  }
}
