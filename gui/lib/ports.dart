import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_libserialport/flutter_libserialport.dart';


class EpochResult {
  final String sdFilename;
  final String localFilename;
  final int sampleCount;

  const EpochResult({
    required this.sdFilename,
    required this.localFilename,
    required this.sampleCount,
  });
}

enum _RecordState {
  idle,
  waitingForSdFilename,
  waitingForTransfer,
  collectingData,
}

String _sessionTimestamp() {
  final now = DateTime.now().toLocal();
  return '${now.year}'
      '-${now.month.toString().padLeft(2, '0')}'
      '-${now.day.toString().padLeft(2, '0')}'
      'T${now.hour.toString().padLeft(2, '0')}'
      '${now.minute.toString().padLeft(2, '0')}'
      '${now.second.toString().padLeft(2, '0')}';
}

Future<void> _saveEpoch(
  List<String> lines,
  String sdFilename,
  String sessionTs,
  StreamController<EpochResult> controller,
) async {
  final baseName = sdFilename.contains('.')
      ? sdFilename.substring(0, sdFilename.lastIndexOf('.'))
      : sdFilename;
  final localFilename = 'latrec_${sessionTs}_$baseName.txt';
  final sink = File(localFilename).openWrite();
  for (final line in lines) {
    sink.writeln(line);
  }
  await sink.flush();
  await sink.close();
  if (!controller.isClosed) {
    controller.add(EpochResult(
      sdFilename: sdFilename,
      localFilename: localFilename,
      sampleCount: lines.length,
    ));
  }
}

Stream<EpochResult> recordingStream(String address) {
  final controller = StreamController<EpochResult>();
  final sessionTs = _sessionTimestamp();

  final port = SerialPort(address);
  final _ = port.openRead();
  final config = port.config;
  config.baudRate = 115200;
  port.config = config;
  final reader = SerialPortReader(port);

  var state = _RecordState.idle;
  var sdFilename = '';
  final dataLines = <String>[];
  var lineBuffer = '';

  late final StreamSubscription<Uint8List> sub;
  sub = reader.stream.listen(
    (Uint8List chunk) {
      // The OS delivers bytes in arbitrarily-sized chunks, not line by line.
      // Append to a persistent buffer so partial lines survive across calls.
      lineBuffer += String.fromCharCodes(chunk);

      // Find the last complete line in the buffer. Using lastIndexOf means we
      // process everything up to and including the final '\n' in one pass,
      // leaving only the trailing incomplete fragment behind.
      final lastNl = lineBuffer.lastIndexOf('\n');
      if (lastNl == -1) return; // no complete line yet — wait for more chunks

      final complete = lineBuffer.substring(0, lastNl + 1);
      lineBuffer = lineBuffer.substring(lastNl + 1); // keep the incomplete tail

      for (final rawLine in complete.split('\n')) {
        final line = rawLine.trimRight(); // remove trailing \r (Arduino sends CRLF)
        if (line.isEmpty) continue;

        // --- State machine ---
        // The device protocol follows a fixed sequence each epoch:
        //   "File opened successfully!"  → next line is the SD card filename
        //   <filename.csv>              → then ~6 s of silence while recording
        //   "Record completed. Transferring file..."  → CSV rows follow
        //   <rows...>
        //   "File opened successfully!"  → next epoch begins (previous one is done)

        if (state == _RecordState.waitingForSdFilename) {
          // The line immediately after "File opened successfully!" is the filename.
          sdFilename = line;
          state = _RecordState.waitingForTransfer;
        } else if (state == _RecordState.collectingData) {
          if (line == 'File opened successfully!') {
            // This line marks the end of the current epoch's transfer.
            // Snapshot the accumulated data and kick off an async file save.
            // The save runs during the next ~6 s silent recording phase, so it
            // completes long before more data arrives.
            // We copy before clearing so the save closure holds its own data.
            if (dataLines.isNotEmpty) {
              final epochSdFilename = sdFilename;
              final epochLines = List<String>.from(dataLines);
              dataLines.clear();
              unawaited(_saveEpoch(epochLines, epochSdFilename, sessionTs, controller));
            }
            state = _RecordState.waitingForSdFilename;
          } else {
            dataLines.add(line);
          }
        } else {
          // idle or waitingForTransfer: watch for the two protocol trigger lines,
          // ignore everything else (boot messages, blank lines, etc.)
          if (line == 'File opened successfully!') {
            state = _RecordState.waitingForSdFilename;
          } else if (line == 'Record completed. Transferring file...') {
            dataLines.clear();
            state = _RecordState.collectingData;
          }
        }
      }
    },
    onError: (Object e) {
      controller.addError(e);
      controller.close();
      port.close();
    },
    onDone: () {
      controller.close();
      port.close();
    },
    cancelOnError: true,
  );

  controller.onCancel = () async {
    await sub.cancel();
    port.close();
  };

  return controller.stream;
}


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
