+++
title = "GUI Development"
description = "Guide for GUI developers working on the Latency Recorder Flutter application"
SequenceNumber = 11
+++

# GUI Development

This section contains information for developers working on the Latency Recorder GUI application.

## Overview

The GUI is built using Flutter, providing a cross-platform desktop application for:
- Device detection and connection
- Recording control and monitoring
- Data visualization and analysis
- Export functionality

## Architecture

### Key Components

- **Device Management** (`device.dart`): Handles serial port detection and communication
- **Home Screen** (`home.dart`): Main application interface
- **Recording Control** (`recordbutton.dart`): Start/stop recording functionality
- **Port Selection** (`ports.dart`): Serial port configuration
- **About Page** (`about.dart`): Application information

### Dependencies

- `flutter_libserialport`: Serial communication
- `provider`: State management
- `fl_chart`: Data visualization (when implemented)

## API Documentation

The GUI is documented using Dart's built-in documentation system. The API documentation includes:

- **Widget documentation**: Complete reference for all custom widgets and components
- **State management**: Documentation for providers and state classes
- **Serial communication**: APIs for device detection and data handling
- **Utility functions**: Helper methods and shared functionality

### View API Documentation

<div style="margin: 2rem 0; padding: 1.5rem; background: rgba(107, 114, 128, 0.1); border: 1px solid rgba(107, 114, 128, 0.3); border-radius: 0.5rem;">
  <h4 style="margin-top: 0; color: #6b7280;">📚 Flutter/Dart API Reference</h4>
  <p style="color: #6b7280;">Explore the complete API documentation for all Flutter/Dart components, widgets, and utilities.</p>
  <span style="display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem; background: #6b7280; color: #e5e7eb; text-decoration: line-through; border-radius: 0.25rem; cursor: not-allowed;">
    View API Documentation →
  </span>
</div>

### Generating Documentation

To regenerate the API documentation:

```bash
./generate-docs.sh
```

## Development Setup

1. Install Flutter:
   ```bash
   # Download from https://flutter.dev/docs/get-started/install
   flutter doctor
   ```

2. Install dependencies:
   ```bash
   cd gui
   flutter pub get
   ```

3. Run the application:
   ```bash
   flutter run -d macos  # or linux, windows
   ```

## Building for Distribution

### macOS
```bash
flutter build macos --release
```

### Linux
```bash
flutter build linux --release
```

### Windows
```bash
flutter build windows --release
```

## Communication Protocol

The GUI communicates with the Arduino using a simple serial protocol:

- **Start Recording**: Send `'S'`
- **Stop Recording**: Send `'E'`
- **Data Format**: Comma-separated values with timestamp and ADC reading
- **Baud Rate**: 115200

## Future Enhancements

- Real-time data visualization
- Advanced analysis tools
- Experiment configuration management
- Data export in multiple formats