import 'package:flutter/material.dart';
import 'package:latrec/ports.dart';


class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.title});

  final String title;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String? selectedPortAddress;

  @override
  void initState() {
    super.initState();
  }

  Future<void> _changePort(BuildContext context) async {

    selectedPortAddress = await Navigator.push<String?>(
      context,
      MaterialPageRoute(builder: (context) => PortsPage(selectedPortAddress)),
    );

    // When a BuildContext is used from a StatefulWidget, the mounted property
    // must be checked after an asynchronous gap.
    if (!context.mounted) return;
    setState(() {});

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
        title: Text(widget.title),
      ),
      body: Column(
        children: [
          Text(selectedPortLabel()),
          ElevatedButton(
            child: Icon(Icons.device_unknown),
            onPressed: () { _changePort(context); }
          ),
        ]
      )
    );
  }
}
