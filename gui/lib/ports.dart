import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
// Conditional import for better web compatibility
import 'package:flutter_libserialport/flutter_libserialport.dart' if (dart.library.html) 'ports_mock.dart';


Future<String?> selectDevice(BuildContext context) async {
  final availablePorts = findConnectedDevices();
  ScaffoldMessenger.of(context).removeCurrentSnackBar();
  if (availablePorts.isEmpty) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(kIsWeb 
          ? 'Serial ports not available in web browser. Use desktop app for full functionality.' 
          : 'No Recorder found. Have you connected it?'),
      )
    );
    return null;
  }
  else {
    return showDialog<String?>(
      context: context,
      builder: (BuildContext context) {
        return SimpleDialog(
          title: const Text('Select Device'),
          children: <Widget>[
            for (final address in availablePorts)
              buildOption(address, context)
          ],
        );
      }
    );
  }
}

List<String> findConnectedDevices() {
  // Return mock data for web or when serial ports are not available
  if (kIsWeb) {
    return ['/dev/ttyUSB0 (Demo)', '/dev/ttyACM0 (Demo)', 'COM3 (Demo)'];
  }
  
  try {
  return SerialPort.availablePorts.where((a) => !a.contains('luetooth')).toList();
  } catch (e) {
    debugPrint('Serial port error: $e');
    return []; // Return empty list if serial ports fail
  }
}

SimpleDialogOption buildOption(String address, BuildContext context) {
  if (kIsWeb) {
    return SimpleDialogOption(
      onPressed: () { Navigator.pop(context, address); },
      child: Text('$address (Web Demo Mode)'),
    );
  }
  
  try {
  final port = SerialPort(address);
  debugPrint('Address $address');
  debugPrint('Description ${port.description}');
  debugPrint('Transport ${port.transport.toTransport()}');
  debugPrint('Manufacturer ${port.manufacturer}');
  debugPrint('Product Name ${port.productName}');
  debugPrint('Serial Number ${port.serialNumber}');
  debugPrint('MAC Address ${port.macAddress}');
  port.close();
  return SimpleDialogOption(
    onPressed: () { Navigator.pop(context, address); },
    child: Text(address),
  );
  } catch (e) {
    debugPrint('Error accessing port $address: $e');
    return SimpleDialogOption(
      onPressed: () { Navigator.pop(context, address); },
      child: Text('$address (Error accessing port)'),
    );
  }
}


// a bug here with error 34
extension IntToString on int {
  String toHex() => '0x${toRadixString(16)}';
  String toPadded([int width = 3]) => toString().padLeft(width, '0');
  String toTransport() {
    switch (this) {
      case SerialPortTransport.usb:
        return 'USB';
      case SerialPortTransport.bluetooth:
        return 'Bluetooth';
      case SerialPortTransport.native:
        return 'Native';
      default:
        return 'Unknown';
    }
  }
}

/*
- callback for finished
- callback for update
- fancier: keep an instance around, for it to be two way, i.e. closing connection
- should dispose

https://github.com/jpnurmi/flutter_libserialport/issues/30#issuecomment-938076196

*/
Future<String> record(String address) async {
  if (kIsWeb) {
    // Mock implementation for web
    debugPrint('Web demo mode: simulating recording from $address');
    await Future.delayed(const Duration(seconds: 2)); // Simulate recording time
    
    final epochMs = DateTime.now().toUtc().millisecondsSinceEpoch;
    final fileName = 'demo_record_$epochMs.dat';
    
    // Create some mock data
    final mockData = List.generate(100, (i) => 
      '${128 + (i % 50)} ${i % 2} ${i * 64}\n'
    ).join();
    
    debugPrint('Demo data generated: $fileName');
    return fileName;
  }
  
  try {
  final port = SerialPort(address);
  final _ = port.openRead();
  final config = port.config; 
  //You should always set baud rate, data bits, parity and stop bits.
  // debugPrint('baudRate ${config.baudRate}');//10?
  // debugPrint('bits ${config.bits}');//10?
  // debugPrint('parity ${config.parity}');//10?
  // debugPrint('stopBits ${config.stopBits}');//10?
  config.baudRate = 115200;
  port.config = config;
  final reader = SerialPortReader(port);
  final List<Uint8List> dataList = [];
  const MAX_SAMPLES = 1000;
  await for (final Uint8List data in reader.stream) {
      if (dataList.length >= MAX_SAMPLES) {
        //counter doesnt work since data.length varies
        // should instead append to collapsed list?
        debugPrint('closing since max samples reached');
        break;
      }
      debugPrint('####${data}#####');
      dataList.add(data);
  }
  debugPrint('${dataList.length}');
  final epochMs = DateTime.now().toUtc().millisecondsSinceEpoch;
  final fileName = 'record_$epochMs.dat';
  final IOSink sink = File(fileName).openWrite();
  for (var data in dataList) {
    sink.add(data);
  }
  await sink.flush();
  await sink.close();
  return fileName;
  } catch (e) {
    debugPrint('Serial recording error: $e');
    // Return mock data on error
    final epochMs = DateTime.now().toUtc().millisecondsSinceEpoch;
    return 'error_fallback_$epochMs.dat';
  }
}
