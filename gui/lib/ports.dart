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
