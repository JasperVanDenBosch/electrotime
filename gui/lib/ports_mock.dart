// Mock implementation for web compatibility
// This file provides the same interface as flutter_libserialport for web builds

import 'dart:typed_data';

class SerialPort {
  final String _name;
  
  SerialPort(this._name);
  
  static List<String> get availablePorts => [];
  
  String get description => 'Mock Serial Port';
  int get transport => SerialPortTransport.usb;
  String? get manufacturer => 'Mock Manufacturer';
  String? get productName => 'Mock Device';
  String? get serialNumber => '12345';
  String? get macAddress => null;
  
  SerialPortConfig get config => SerialPortConfig();
  set config(SerialPortConfig config) {}
  
  bool openRead() => true;
  void close() {}
}

class SerialPortConfig {
  int baudRate = 115200;
  int bits = 8;
  int parity = 0;
  int stopBits = 1;
}

class SerialPortReader {
  SerialPortReader(SerialPort port);
  
  Stream<Uint8List> get stream async* {
    // Mock stream - never yields data for web
    yield* Stream.empty();
  }
}

class SerialPortTransport {
  static const int usb = 0;
  static const int bluetooth = 1;
  static const int native = 2;
} 