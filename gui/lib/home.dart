import 'dart:async';

import 'package:flutter/material.dart';
import 'package:latrec/ports.dart';
import 'package:latrec/recordbutton.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  static const title = 'Latency Recorder';
  
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String? selectedPortAddress;
  bool recording = false;
  int secondsElapsed = 0;
  Timer? timer;
  final TextEditingController deviceController = TextEditingController();

  String timeElapsedString() {
    final mins = (secondsElapsed / 60).floor();
    final secs = (secondsElapsed % 60).floor();
    final secsPadded = secs.toString().padLeft(2, '0');
    return '$mins:$secsPadded';
  }

  void record() {
    secondsElapsed = 0;
    final previousTimer = timer;
    if (previousTimer != null) {
      previousTimer.cancel();
    }
    timer = Timer.periodic(const Duration(seconds: 1), (Timer t) {
      setState(() {
        secondsElapsed += 1;
      });
    });
    setState(() {
      recording = !recording;
    });
  }

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    deviceController.dispose(); // You need to do this.

    super.dispose();
  }

  String selectedPortLabel() {
    final _selectedPortAddress = selectedPortAddress;
    if (_selectedPortAddress != null) {
      return _selectedPortAddress;
    }
    else {
      return 'Select Device';
    }
  }

  void Function()? getDeviceSelectionCallback() {
    return recording ? null : () { 
      selectDevice(context).then((newPortAddress) {
        setState(() {
          selectedPortAddress = newPortAddress;
          if (newPortAddress != null) {
            deviceController.text = selectedPortAddress!;
          }
        });
      });
    };
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text(HomePage.title),
      ),
      body: Center(
        child: Container(
          constraints: const BoxConstraints(maxWidth: 400),
          padding: const EdgeInsets.all(4),
          child:Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              TextField(
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
                ),
            Row(
              children: [
                RecordButton(
                  active: recording,
                  callback: record
                ),
                const Spacer(),
                Text(timeElapsedString()),
              ]
            )
          ]
        )
        ),
      )
    );
  }
}
