import 'package:flutter/material.dart';

enum LabelPosition { left, below }

class Counter extends StatelessWidget {
  final int value;
  final String label;
  final LabelPosition labelPosition;

  const Counter({
    super.key,
    required this.value,
    required this.label,
    this.labelPosition = LabelPosition.left,
  });

  static String format(int n) {
    if (n >= 2000000) return '${n ~/ 1000000}M';
    if (n >= 2000) return '${n ~/ 1000}k';
    return '$n';
  }

  static const _labelStyle = TextStyle(
    color: Colors.black54,
    fontSize: 17,
    letterSpacing: 1.2,
  );

  @override
  Widget build(BuildContext context) {
    final text = format(value).padLeft(4);
    final chars = text.characters.toList();

    final digitBox = Container(
      decoration: BoxDecoration(
        color: const Color(0xFF3C4148),
        borderRadius: BorderRadius.circular(8),
      ),
      clipBehavior: Clip.antiAlias,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          for (int i = 0; i < chars.length; i++) ...[
            SizedBox(
              width: 26,
              height: 40,
              child: Center(
                child: Text(
                  chars[i],
                  style: const TextStyle(
                    fontFamily: 'Courier New',
                    fontSize: 26,
                    color: Colors.white,
                    height: 1,
                  ),
                ),
              ),
            ),
            if (i < chars.length - 1)
              Container(
                width: 1,
                height: 40,
                color: const Color(0xFF252830),
              ),
          ],
        ],
      ),
    );

    if (labelPosition == LabelPosition.below) {
      return Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          digitBox,
          if (label.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 4),
              child: Text(label, style: _labelStyle),
            ),
        ],
      );
    }

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (label.isNotEmpty) ...[
          Text(label, style: _labelStyle),
          const SizedBox(width: 8),
        ],
        digitBox,
      ],
    );
  }
}
