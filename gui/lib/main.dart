import 'package:flutter/material.dart';
import 'package:latrec/home.dart';

void main() {
  runApp(const LatRecApp());
}

class LatRecApp extends StatelessWidget {
  const LatRecApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Latency Recorder',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}




