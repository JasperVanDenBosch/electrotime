import 'package:flutter/material.dart';
import 'package:latrec/dashboard_data.dart';

class Dashboard extends StatelessWidget {
  final DashboardData data;

  const Dashboard({super.key, required this.data});

  static const _mono = TextStyle(fontFamily: 'Courier New', fontSize: 13);

  String _abbreviateSamples(int count) {
    if (count < 1000) return '$count';
    final k = count / 1000;
    return k == k.truncateToDouble() ? '${k.toInt()}k' : '${k.toStringAsFixed(1)}k';
  }

  Widget _buildTriggerRow(BuildContext context, MapEntry<int, int> entry) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
            decoration: BoxDecoration(
              border: Border.all(color: Theme.of(context).colorScheme.outline),
            ),
            child: Text('${entry.key}', style: _mono),
          ),
          const SizedBox(width: 12),
          Text('${entry.value}', style: _mono),
        ],
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
        Text(
          'EPOCHS: ${data.epochCount}   SAMPLES: ${_abbreviateSamples(data.sampleCount)}',
          style: _mono,
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
