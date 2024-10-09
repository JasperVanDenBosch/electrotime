import 'package:flutter/material.dart';

class RecordButton extends StatelessWidget {
  const RecordButton({super.key, required this.active, required this.callback});

  final bool active;
  final VoidCallback callback;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      onPressed: callback,
      icon: Icon(Icons.fiber_manual_record, color: active ? Colors.red: null),
      label: const Text('record'),
    );
  }
}