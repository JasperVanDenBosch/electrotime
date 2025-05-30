+++
title = "User Interface"
description = "Cross-platform Flutter app for recording control"
SequenceNumber = 4
+++

# 🖥️ User Interface

The user interface app was made with Flutter, a cross-platform framework that is great for creating user-friendly apps that work on mobile, desktop and even the web. Flutter code is written in the language Dart. Flutter and Dart were created by Google.

Since experimenters may use a laptop that runs OSX, Windows or linux we wanted to make an app that works on either. 🌍

It currently has a button to start and stop recording ⏺️ ⏹️ and displays a timer ⏱️ while recording. There is also a dropdown to select the connected device. 🔌

You'll find the code for the app under "gui" in the GitHub repository. 📂

## 🌟 Core Principles

### 🔓 Open Source First

- **MIT Licensed**: Free to use, modify, and distribute
- **Transparent Development**: All code publicly available on GitHub
- **No Vendor Lock-in**: Use with any hardware configuration
- **Community Ownership**: Belongs to the research community

### 🔬 Ensure Replicability

- **Cross-platform Compatibility**: Same behavior across Windows, macOS, and Linux
- **Standardized Data Format**: Binary format documented and consistent
- **Version Control**: Tagged releases for experiment reproducibility
- **Configuration Export**: Save and share experimental setups

### 🤝 Welcome Further Development

- **Modular Architecture**: Easy to extend and modify
- **Clear Documentation**: Well-commented code and API docs
- **Plugin System** (planned): Add custom features without modifying core
- **Active Community**: Discord channel for developers and users

## 📚 Preparation

- 📥 Clone the git repository
- 🎯 Install dart and flutter
- ✅ Check if it works by building and running the app, e.g: `flutter run -d macos`

## 🪟 Windows Installation

To run on Windows you're going to still need Flutter and Dart, as stated above. To install these, Dart suggests using Chocolatey. Installing Flutter through Chocolatey will install its own compatible version of Dart alongside it, so getting it separately might not be required - though it will still be shown below if manual installations are preferred.

### Installing Chocolatey

Chocolatey's installation is described on its [webpage](https://chocolatey.org/install). This will require an administrator PowerShell, and can be done using the following command:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Installing Dart and Flutter

Once installed, both Dart and Flutter can be installed using the commands listed on their respective webpages.

Much like Chocolatey, Dart requires an administrator PowerShell to install it, but it can easily be done using the command:

```powershell
choco install dart-sdk
```

Flutter's documentation mentions installation via VS Code, or manual installation. However, given Chocolatey was required for Dart, it's just as easy to install using the command:

```powershell
choco install flutter
```

### Verifying Installation

Both Flutter and Dart can be checked for successful installs using the following commands:

```powershell
dart --version
flutter --version
```

Once installed, these will be located by default in `C:\tools`.

⚠️ **Warning:** If attempting to install any of these via a non-admin PowerShell, it can download an incomplete version of the software. Manual deletion may be required.

### Additional Platform Requirements

After this is done, you may also need some extra software for the target platforms. It's worth using the doctor command to check if Flutter is able to target the platforms you're looking into:

```powershell
flutter doctor
```

In the case of building for Windows, you can either install VS Community (the IDE) or just the build tools, both are located [here on Microsoft's page](https://visualstudio.microsoft.com/downloads/).

### IDE Configuration

Once downloaded, your IDE should be able to open and run the project, if it can locate the Flutter and Dart packages correctly.

Some IDEs may require additional packages to let them use Dart and Flutter. For IntelliJ IDEA, it requires some additional installations: the Dart and Flutter plugins for the IDE. Both plugins can be installed via the plugins section of the IDE, and then setup using their entries in the 'Languages and Frameworks' area of the IDE settings. This may require manually setting the locations of the tools installation paths, which are stored in `C:\tools` by default.

**Flutter SDK:**
```
C:\tools\flutter
```

**Dart SDK:**
```
C:\tools\flutter\bin\cache\dart-sdk
C:\tools\dart
```

## 🎨 UI Architecture

### Technology Stack
- **Framework**: Flutter 3.x
- **Language**: Dart
- **State Management**: Provider pattern
- **Serial Communication**: flutter_libserialport package
- **Data Storage**: Local file system

### Project Structure
```
gui/
├── lib/
│   ├── main.dart              # Application entry point
│   ├── screens/
│   │   ├── home_screen.dart   # Main recording interface
│   │   └── settings_screen.dart # Configuration options
│   ├── widgets/
│   │   ├── device_selector.dart # Serial port dropdown
│   │   ├── recording_timer.dart # Recording duration display
│   │   └── control_buttons.dart # Start/stop controls
│   ├── services/
│   │   ├── serial_service.dart  # Serial communication
│   │   └── file_service.dart    # Data file management
│   └── models/
│       └── recording_data.dart   # Data structures
├── test/                       # Unit and widget tests
├── assets/                     # Images and resources
└── pubspec.yaml               # Dependencies

```

## 🔧 Current Features

### Device Management
- **Auto-detection**: Scans for connected Arduino devices
- **Manual Selection**: Dropdown for port selection
- **Connection Status**: Visual indicators
- **Reconnection**: Automatic retry on disconnect

### Recording Controls
- **Start/Stop**: Large, accessible buttons
- **Timer Display**: Shows elapsed recording time
- **Data Counter**: Number of samples collected
- **Status Messages**: Real-time feedback

### Data Handling
- **Binary Format**: Efficient storage format
- **File Naming**: Timestamp-based filenames
- **Directory Selection**: Choose save location
- **Export Options**: CSV conversion (planned)

## 💡 UI Enhancement Ideas

### Idea 1: Real-time Visualization 📊
- Live waveform display of sensor data
- Trigger event markers
- Latency histogram
- Statistics panel
- **Open source visualization libraries only**
- **Export raw data for replication**

### Idea 2: Experiment Integration 🧪
- Protocol templates
- Trial counter
- Metadata recording
- Notes and annotations
- **Shareable experiment configurations**
- **Version-controlled protocols**

### Idea 3: Multi-device Support 🔌
- Connect multiple recorders
- Synchronized recording
- Device naming
- Channel mapping
- **Support for DIY hardware variants**
- **Community-contributed device profiles**

### Idea 4: Plugin Architecture 🧩
- **Community-developed extensions**
- **Custom analysis modules**
- **Integration with other tools**
- **Maintain core simplicity**

### Idea 5: Replication Features 🔄
- **One-click experiment export**
- **Complete setup documentation**
- **Hardware configuration capture**
- **Results verification tools**

## 🛠️ Development Guide

### Setting Up Development Environment

#### macOS Setup
```bash
# Install Flutter
brew install --cask flutter

# Verify installation
flutter doctor

# Run the app
cd gui
flutter run -d macos
```

#### Linux Setup
```bash
# Download Flutter
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.0.0-stable.tar.xz
tar xf flutter_linux_3.0.0-stable.tar.xz

# Add to PATH
export PATH="$PATH:`pwd`/flutter/bin"

# Install dependencies
sudo apt-get install clang cmake ninja-build pkg-config libgtk-3-dev

# Run the app
cd gui
flutter run -d linux
```

### Building for Distribution

#### Windows
```bash
flutter build windows --release
# Output: build/windows/runner/Release/
```

#### macOS
```bash
flutter build macos --release
# Output: build/macos/Build/Products/Release/
```

#### Linux
```bash
flutter build linux --release
# Output: build/linux/x64/release/bundle/
```

## 🧪 Testing

### Unit Tests
```dart
// test/services/serial_service_test.dart
import 'package:test/test.dart';
import 'package:gui/services/serial_service.dart';

void main() {
  test('Serial port detection', () {
    final service = SerialService();
    final ports = service.getAvailablePorts();
    expect(ports, isNotEmpty);
  });
}
```

### Widget Tests
```dart
// test/widgets/recording_timer_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:gui/widgets/recording_timer.dart';

void main() {
  testWidgets('Timer shows elapsed time', (WidgetTester tester) async {
    await tester.pumpWidget(RecordingTimer());
    expect(find.text('00:00'), findsOneWidget);
  });
}
```

### Integration Tests
```dart
// integration_test/app_test.dart
import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  testWidgets('Complete recording workflow', (tester) async {
    // Test device selection, recording, and file saving
  });
}
```

## 🎯 UI/UX Best Practices

### Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Screen Readers**: Semantic labels
- **High Contrast**: Visibility options
- **Large Targets**: Touch-friendly buttons

### Performance
- **Efficient Rendering**: Minimize rebuilds
- **Memory Management**: Dispose resources
- **Background Tasks**: Isolates for heavy work
- **Smooth Animations**: 60 FPS target

### Error Handling
- **User-friendly Messages**: Clear error descriptions
- **Recovery Options**: Suggest solutions
- **Logging**: Debug information
- **Crash Reporting**: Optional analytics

## 🔗 Useful Resources

### Flutter Development
- 📱 [Flutter Documentation](https://docs.flutter.dev/)
- 🎯 [Dart Language Tour](https://dart.dev/guides/language/language-tour)
- 📊 [Flutter Samples](https://flutter.github.io/samples/)
- 🛠️ [Flutter DevTools](https://docs.flutter.dev/development/tools/devtools)

### Serial Communication
- 📡 [flutter_libserialport](https://pub.dev/packages/flutter_libserialport)
- 🔌 [Serial Port Programming](https://en.wikibooks.org/wiki/Serial_Programming)
- 💻 [USB CDC Class](https://www.usb.org/document-library/class-definitions-communication-devices-12)

### UI Design
- 🎨 [Material Design](https://material.io/design)
- 🖼️ [Flutter Widget Catalog](https://docs.flutter.dev/development/ui/widgets)
- 📐 [Responsive Design](https://docs.flutter.dev/development/ui/layout/responsive)

## 🤝 Contributing to UI

### Open Source Guidelines
- **License Compliance**: Ensure all dependencies are compatible with MIT license
- **No Proprietary Code**: Keep everything open and accessible
- **Attribution**: Credit all contributors and libraries used
- **Transparency**: Document all design decisions

### Replicability Standards
- **Platform Testing**: Test on Windows, macOS, and Linux
- **Data Format Documentation**: Update specs if changing data structure
- **Backward Compatibility**: Maintain support for existing data files
- **Version Tagging**: Use semantic versioning for releases

### Welcoming Contributions
- **Beginner Friendly**: Label issues for newcomers
- **Code Reviews**: Provide constructive, educational feedback
- **Documentation**: Write for future developers
- **Community Building**: Help others get started

### Code Style
- Follow [Effective Dart](https://dart.dev/guides/language/effective-dart) guidelines
- Use `flutter format` before committing
- Add widget tests for new features
- Document public APIs

### Feature Development
1. **Discuss First**: Open an issue or chat on Discord
2. **Check Principles**: Ensure alignment with open source and replicability goals
3. **Design Mockups**: Share UI concepts with community
4. **Implement**: Follow existing patterns
5. **Test**: Add appropriate tests for all platforms
6. **Document**: Update relevant docs for users and developers
7. **Submit PR**: With clear description and rationale
