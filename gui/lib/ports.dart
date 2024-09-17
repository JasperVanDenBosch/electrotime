import 'package:flutter/material.dart';
import 'package:flutter_libserialport/flutter_libserialport.dart';


Future<String?> selectDevice(BuildContext context) async {
  return showDialog<String?>(
      context: context,
      builder: (BuildContext context) {
        return SimpleDialog(
          title: const Text('Select assignment'),
          children: <Widget>[
            SimpleDialogOption(
              onPressed: () { Navigator.pop(context, 'Treasury'); },
              child: const Text('Treasury department'),
            ),
            SimpleDialogOption(
              onPressed: () { Navigator.pop(context, 'State'); },
              child: const Text('State department'),
            ),
          ],
        );
      }
  );
}


class PortsPage extends StatefulWidget {
  const PortsPage(this.selectedPortAddress);

  final String? selectedPortAddress;


  @override
  State<PortsPage> createState() => _PortsPageState();
}

class _PortsPageState extends State<PortsPage> {
  var availablePorts = [];
  

  @override
  void initState() {
    super.initState();
    initPorts();
  }

  void initPorts() {
    setState(() => availablePorts = SerialPort.availablePorts);
    debugPrint('${availablePorts.length}');
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text('????'),
      ),
      body: Scrollbar(
          child: ListView(
            children: [
              for (final address in availablePorts)
                Builder(builder: (context) {
                  final port = SerialPort(address);
                  return ExpansionTile(
                    title: Row(
                      children: [
                        Text(address),
                        IconButton(
                          onPressed: () {
                            Navigator.pop(context, address);
                          },
                          icon: const Icon(Icons.private_connectivity),
                          tooltip: 'Select this device',
                        )
                      ]
                    ),
                    children: [
                      CardListTile('Description', port.description),
                      CardListTile('Transport', port.transport.toTransport()),
                      CardListTile('Manufacturer', port.manufacturer),
                      CardListTile('Product Name', port.productName),
                      CardListTile('Serial Number', port.serialNumber),
                      CardListTile('MAC Address', port.macAddress),
                    ],
                  );
                }),
            ],
          ),
        ),
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

class CardListTile extends StatelessWidget {
  final String name;
  final String? value;

  CardListTile(this.name, this.value);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(value ?? 'N/A'),
        subtitle: Text(name),
      ),
    );
  }
}