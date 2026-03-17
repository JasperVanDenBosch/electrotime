import 'package:flutter/material.dart';

class Counter extends StatelessWidget {
  final int value;
  final String label;

  const Counter({super.key, required this.value, required this.label});

  static String format(int n) {
    if (n >= 2000000) return '${n ~/ 1000000}M';
    if (n >= 2000) return '${n ~/ 1000}k';
    return '$n';
  }

  @override
  Widget build(BuildContext context) {
    final text = format(value).padLeft(4);
    final chars = text.characters.toList();

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
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
        ),
        if (label.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(top: 4),
            child: Text(
              label,
              style: const TextStyle(
                color: Colors.white54,
                fontSize: 11,
                letterSpacing: 1.2,
              ),
            ),
          ),
      ],
    );
  }
}
