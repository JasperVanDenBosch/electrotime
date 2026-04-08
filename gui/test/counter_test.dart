import 'package:flutter_test/flutter_test.dart';
import 'package:latrec/counter.dart';

void main() {
  group('Counter.format()', () {
    test('small values shown as-is', () {
      expect(Counter.format(0), '0');
      expect(Counter.format(1), '1');
      expect(Counter.format(999), '999');
      expect(Counter.format(1999), '1999');
    });

    test('2000 is the k threshold', () {
      expect(Counter.format(2000), '2k');
      expect(Counter.format(2001), '2k');
    });

    test('k range uses integer division', () {
      expect(Counter.format(9999), '9k');
      expect(Counter.format(10000), '10k');
      expect(Counter.format(999999), '999k');
      expect(Counter.format(1999999), '1999k');
    });

    test('2 000 000 is the M threshold', () {
      expect(Counter.format(2000000), '2M');
      expect(Counter.format(2000001), '2M');
    });

    test('M range uses integer division', () {
      expect(Counter.format(999000000), '999M');
    });
  });
}
