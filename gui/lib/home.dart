import 'dart:async';
import 'package:flutter/material.dart';
import 'package:latrec/about.dart';
import 'package:latrec/dashboard.dart';
import 'package:latrec/dashboard_data.dart';
import 'package:latrec/device.dart';
import 'package:latrec/mock.dart';
import 'package:latrec/ports.dart';
import 'package:latrec/recordbutton.dart';


class HomePage extends StatefulWidget {
  const HomePage({super.key});

  static const title = 'ElectroTime';

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {

  String? selectedPortAddress;
  bool recording = false;
  int secondsElapsed = 0;
  Timer? timer;
  StreamSubscription<EpochResult>? _recordingSubscription;
  DashboardData _dashboardData = DashboardData.empty();

  String timeElapsedString() {
    final mins = (secondsElapsed / 60).floor();
    final secs = (secondsElapsed % 60).floor();
    final secsPadded = secs.toString().padLeft(2, '0');
    return '$mins:$secsPadded';
  }

  void startRecording() {
    setState(() {
      secondsElapsed = 0;
      recording = true;
      _dashboardData = DashboardData.empty();
      timer = Timer.periodic(const Duration(seconds: 1), (Timer t) {
        setState(() {
          secondsElapsed += 1;
        });
      });
    });
    final stream = selectedPortAddress == demoPortAddress
        ? mockRecordingStream()
        : recordingStream(selectedPortAddress!);
    _recordingSubscription = stream.listen(
      (EpochResult result) {
        debugPrint('Epoch saved: ${result.localFilename} (${result.sampleCount} samples)');
        setState(() {
          _dashboardData = _dashboardData.addEpoch(result);
        });
      },
      onError: (Object e) {
        debugPrint('Recording error: $e');
        _finishRecording();
      },
      onDone: _finishRecording,
    );
  }

  void stopRecording() {
    _recordingSubscription?.cancel();
    _recordingSubscription = null;
    _finishRecording();
  }

  void _finishRecording() {
    timer?.cancel();
    setState(() {
      recording = false;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Saved ${_dashboardData.epochCount} epochs (${_dashboardData.sampleCount} samples)'),
      )
    );
  }

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        // Brand colors — blue: RGB(80,145,171), yellow: RGB(238,209,83)
        backgroundColor: const Color.fromRGBO(80, 145, 171, 1),
        title: Padding(
          padding: const EdgeInsets.symmetric(vertical: 20),
          child: Image.asset('assets/title.png', height: 32),
        ),
        centerTitle: true,
      ),
      body: Center(
        child: Container(
          constraints: const BoxConstraints(maxWidth: 400),
          padding: const EdgeInsets.all(4),
          child:Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
            const SizedBox(height: 10),
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
                  callback: recording ? stopRecording : startRecording,
                ),
                const Spacer(),
                Text(timeElapsedString()),
              ]
            ),
            const SizedBox(height: 10),
            Expanded(child: Dashboard(data: _dashboardData)),
          ]
        )
        ),
      ),
      bottomSheet: const AboutSection(),
    );
  }
}
