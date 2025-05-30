# Latency Recorder

An open-source Arduino-based device that measures stimulus presentation latency in neuroscience experiments, particularly EEG setups. This project provides hardware designs, firmware, and software tools to help researchers worldwide accurately measure and compensate for timing delays in their experimental paradigms using affordable, accessible hardware.

🌍 Mission
Enable consistent, accurate EEG testing globally by providing open-source, low-cost tools that eliminate timing uncertainties in neuroscience research. Our goal is to make precision timing accessible to researchers everywhere, regardless of budget or location.


🧠 The Problem We Solve
In EEG research, Event-Related Potentials (ERPs) require millisecond precision. However, unknown delays exist between:

Visual stimulus: Code → OS → GPU → Monitor
Trigger signal: Code → OS → Trigger device → EEG amplifier

Most EEG studies assume this delay is 0ms, leading to inaccurate timing and compromised research quality. The Latency Recorder measures these delays in real-time, enabling researchers to achieve true millisecond precision.


## 📋 Overview

The Latency Recorder helps neuroscientists measure the precise timing between trigger signals and actual stimulus presentation (visual/auditory). This is crucial for time-sensitive analyses like ERPs (Event-Related Potentials) where millisecond precision matters.

**Key Features:**

- Real-time latency measurement using photodiode for visual stimuli
- Parallel port (DB37) input for trigger signals
- Continuous data streaming via USB serial connection (15625Hz sampling rate)
- Cross-platform GUI application for data recording and analysis
- Open-source hardware and software design

For more details about the Timing Matters Hackathon and project overview, see [docs/Overview.md](docs/Overview.md).

## 🗂️ Repository Structure

### `/firmware/`

Contains the embedded code that runs on the Arduino device.

- **`/latreclib/`** - Rust library with core latency recording logic
- **`/recorder/`** - Main firmware application for the Arduino Uno
- **`/simulator/`** - Hardware simulator for testing without physical device

The firmware is written in Rust using the AVR HAL library. See [docs/Firmware.md](docs/Firmware.md) for development details.

### `/gui/`

Flutter-based cross-platform desktop application for interfacing with the device.

Features:

- Start/stop recording with visual timer
- Device selection dropdown
- Data export functionality

Built with Flutter/Dart for Windows, macOS, and Linux compatibility. See [docs/User Interface.md](docs/User%20Interface.md) for setup instructions.

### `/experiment/`

Python scripts for running experiments and collecting data.

- **`run.py`** - Main experiment runner
- **`requirements.txt`** - Python dependencies

### `/analysis/`

Data analysis tools and example outputs.

- **`analyse.py`** - Main analysis script in root directory
- **`/analysis/`** - Contains example analysis plots

See [docs/Data Analysis.md](docs/Data%20Analysis.md) for usage details.

### `/fritzing/`

Hardware schematics and PCB designs.

- **`fritzing_sketch.fzz`** - Complete circuit design
- **`fritzing_sketch_bb.png`** - Breadboard view
- **`TLV2462.fzpz`** - Custom op-amp component

### `/docs/`

Extended documentation for different aspects of the project.

- [Hardware.md](docs/Hardware.md) - Circuit design and assembly
- [Firmware.md](docs/Firmware.md) - Embedded software development
- [User Interface.md](docs/User%20Interface.md) - GUI application details
- [Data Analysis.md](docs/Data%20Analysis.md) - Analysis workflow
- [Website and Documentation.md](docs/Website%20and%20Documentation.md) - Documentation plans
- [Overview.md](docs/Overview.md) - Hackathon information and getting started

## 🚀 Quick Start

### Hardware Requirements

- Arduino Uno Rev3
- Photodiode circuit (see [hardware documentation](docs/Hardware.md))
- USB cable for data connection
- (Optional) DB37 parallel port for trigger input

📊 Technical Specifications

Sampling Rate: 15625Hz (64µs resolution)
Maximum Recording Duration: 4.19 seconds per epoch
Data Output: Light level, trigger state, timestamp (tval)
Connectivity: USB serial communication
Power: USB-powered, no external power required

### Software Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/JasperVanDenBosch/latency-recorder/
   cd latency-recorder
   ```

2. **Flash firmware to Arduino:**

   ```bash
   cd firmware/recorder
   cargo build --release
   # Upload to Arduino (see firmware docs for details)
   ```

3. **Run the GUI application:**

   ```bash
   cd gui
   flutter run
   ```

4. **Start recording data:**

   - Connect the device via USB
   - Select it in the GUI dropdown
   - Click "Start Recording"

## 📊 Data Collection and Analysis

### Basic Data Collection

```python
# Using the simple reader
python simple_reader.py

# Or the full reader with more features
python reader.py
```

### Data Analysis

```python
# Run analysis on collected data
python analyse.py
```

The data is saved in binary format with timestamps and sensor readings. See the analysis examples in `/analysis/` for visualization options.

## 🛠️ Development

### Contributing

We welcome contributions! This is an open-source hardware project. Areas for improvement include:

- **Hardware:** Add microphone for audio latency, SD card for standalone operation
- **Firmware:** Optimize serial communication performance
- **GUI:** Enhanced visualization and real-time plotting
- **Documentation:** User guides and assembly instructions

See individual documentation files in `/docs/` for specific development areas.

### Building from Source

**Firmware (Rust):**

```bash
cd firmware/recorder
cargo build --release
```

**GUI (Flutter):**

```bash
cd gui
flutter build macos  # or windows/linux
```

**Python Tools:**

```bash
pip install -r requirements.txt
```

## 📝 License

This is an open-source hardware and software project. [License details to be added]

## 🔗 Links

- **GitHub Repository:** <https://github.com/JasperVanDenBosch/latency-recorder/>
- **Discord Community:** <https://discord.gg/47mBnvJM>
- **Related Projects:** [EEGManyLabs](https://osf.io/yb3pq/)

## 👥 Credits

Developed as part of the Timing Matters Hackathon at the University of Leeds.

For questions or support, please open an issue on GitHub or join our [Discord community](https://discord.gg/47mBnvJM).

Made with ❤️ for the global neuroscience community
