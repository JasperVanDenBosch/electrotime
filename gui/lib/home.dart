import 'dart:async';
import 'package:flutter/material.dart';
import 'package:latrec/about.dart';
import 'package:latrec/device.dart';
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

  String timeElapsedString() {
    final mins = (secondsElapsed / 60).floor();
    final secs = (secondsElapsed % 60).floor();
    final secsPadded = secs.toString().padLeft(2, '0');
    return '$mins:$secsPadded';
  }

  void onRecordingFinished(String fileName) {
    final previousTimer = timer;
    if (previousTimer != null) {
      previousTimer.cancel();
    }
    setState(() {
      recording = false;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Saved recording as $fileName'),
      )
    );
  }

  void startRecording() {
    setState(() {
      secondsElapsed = 0;
      recording = true;
      timer = Timer.periodic(const Duration(seconds: 1), (Timer t) {
        setState(() {
          secondsElapsed += 1;
        });
      });
      record(selectedPortAddress!).then(onRecordingFinished);
    });
  }

  @override
  void initState() {
    super.initState();
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
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
            DeviceSelector(
              disabled: recording,
              onDeviceChanged: (address) { 
                setState(() {
                  selectedPortAddress = address;
                });
               },
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                RecordButton(
                  disabled: selectedPortAddress == null,
                  active: recording,
                  callback: startRecording
                ),
                const Spacer(),
                Text(timeElapsedString()),
              ]
            )
          ]
        )
        ),
      ),
      bottomSheet: const AboutSection(),
    );
  }
}
