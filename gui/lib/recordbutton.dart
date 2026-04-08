import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class RecordButton extends StatelessWidget {
  const RecordButton({super.key, required this.active, required this.callback, required this.disabled});

  final bool disabled;
  final bool active;
  final VoidCallback callback;

  static const _red = Color(0xFFFF3B30);
  static const _redDim = Color(0xFFD4998F);
  static const _base = Color(0xFFEFEFEF);
  static const _border = Color(0xFFC8C8C8);
  static const _labelIdle = Color(0xFF333333);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: disabled ? null : callback,
      child: Opacity(
        opacity: disabled ? 0.4 : 1.0,
        child: Container(
          width: 96,
          height: 96,
          decoration: BoxDecoration(
            color: _base,
            borderRadius: BorderRadius.circular(2.0),
            border: Border.all(color: _border, width: 1),
            boxShadow: const [BoxShadow(color: Color(0x20000000), blurRadius: 2, offset: Offset(0, 1))],
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: 28,
                height: 28,
                decoration: BoxDecoration(
                  color: active ? _red : _redDim,
                  shape: BoxShape.circle,
                  boxShadow: active
                      ? [BoxShadow(color: _red.withOpacity(0.5), blurRadius: 12.0, spreadRadius: 2)]
                      : null,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'REC',
                style: GoogleFonts.spaceGrotesk(
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                  color: active ? _red : _labelIdle,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
