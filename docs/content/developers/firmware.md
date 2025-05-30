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

### 🎯 Flutter/Dart API

> **[📖 View Complete Flutter API Documentation →](/docs-api/gui/)**  
> Full API reference for all Flutter/Dart components, widgets, and utilities

### Key Classes and Components

#### Core Classes

- **[🏠 HomePage Class](/docs-api/gui/home/HomePage-class.html)** - Main application screen with recording controls and device management
- **[🔌 DeviceSelector Widget](/docs-api/gui/device/DeviceSelector-class.html)** - Dropdown widget for selecting and managing serial devices  
- **[⏺️ RecordButton Widget](/docs-api/gui/recordbutton/RecordButton-class.html)** - Animated button for starting and stopping recordings
- **[🛠️ Port Utilities](/docs-api/gui/ports/ports-library.html)** - Functions for device detection, port management, and recording

### Documentation Features

The Flutter documentation includes:
- **Complete API reference** for all public classes and functions
- **Source code links** for every documented element
- **Interactive search** to quickly find what you need
- **Inheritance diagrams** showing widget relationships
- **Usage examples** where available

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