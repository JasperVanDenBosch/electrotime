import 'package:flutter/material.dart';
import 'package:latrec/ports.dart';

class DeviceSelector extends StatefulWidget {
  const DeviceSelector({super.key, required this.disabled, required this.onDeviceChanged});
  final bool disabled;
  final void Function(String? address) onDeviceChanged;

  @override
  State<DeviceSelector> createState() => _DeviceSelectorState();
}

class _DeviceSelectorState extends State<DeviceSelector> {

  final TextEditingController deviceController = TextEditingController();

  void Function()? getDeviceSelectionCallback() {
    return widget.disabled ? null : () { 
      selectDevice(context).then((newPortAddress) {
        setState(() {
          if (newPortAddress == null) {
            deviceController.text = '';
          }
          else {
            deviceController.text = newPortAddress;
          }
          widget.onDeviceChanged(newPortAddress);
        });
      });
    };
  }

  @override
  void dispose() {
    deviceController.dispose(); // You need to do this.
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return TextField(
      enabled: !widget.disabled,
      onTap: getDeviceSelectionCallback(),
      controller: deviceController,
      readOnly: true,
      decoration: const InputDecoration(
        border: OutlineInputBorder(),
        labelText: 'Device',
        suffixIcon: IconButton(
          onPressed: null,
          icon: Icon(Icons.electrical_services)
        )
      ),
    );
  }
}