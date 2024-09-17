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

  @override
  void initState() {
    super.initState();
  }

  Future<void> _changePort(BuildContext context) async {

    //selectedPortAddress = 
    selectDevice(context).then((newPortAddress) {
      setState(() {
        selectedPortAddress = newPortAddress;
      });
    });

  }

  String selectedPortLabel() {
    final _selectedPortAddress = selectedPortAddress;
    if (_selectedPortAddress != null) {
      return _selectedPortAddress;
    }
    else {
      return '';
    }
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text(HomePage.title),
      ),
      body: Column(
        children: [
          Text(selectedPortLabel()),
          ElevatedButton(
            child: const Icon(Icons.device_unknown),
            onPressed: () { 
              selectDevice(context).then((newPortAddress) {
                setState(() {
                  selectedPortAddress = newPortAddress;
                });
              });
            }
          ),
        ]
      ),
      floatingActionButton: RecordButton(
        active: recording,
        callback: () {
          setState(() {
            recording = !recording;
          });
        }
      )
    );
  }
}
