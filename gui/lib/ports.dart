import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_libserialport/flutter_libserialport.dart';


Future<String?> selectDevice(BuildContext context) async {
  final availablePorts = findConnectedDevices();
  ScaffoldMessenger.of(context).removeCurrentSnackBar();
  if (availablePorts.isEmpty) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('No Recorder found. Have you connected it?'),
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
  return SerialPort.availablePorts.where((a) => !a.contains('luetooth')).toList();
}

SimpleDialogOption buildOption(String address, BuildContext context) {
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
}
