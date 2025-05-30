+++
title = "UI"
description = "Cross-platform Flutter app for recording control"
SequenceNumber = 5
+++

# 🖥️ User Interface

The user interface app was made with Flutter, a cross-platform framework that is great for creating user-friendly apps that work on mobile, desktop and even the web. Flutter code is written in the language Dart. Flutter and Dart were created by Google.

Since experimenters may use a laptop that runs OSX, Windows or linux we wanted to make an app that works on either. 🌍

It currently has a button to start and stop recording ⏺️ ⏹️ and displays a timer ⏱️ while recording. There is also a dropdown to select the connected device. 🔌

You'll find the code for the app under "gui" in the github repository. 📂

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
