
![ElectroTime logo](https://github.com/JasperVanDenBosch/electrotime/blob/main/docs/assets/electrotime-dark.svg??raw=true)

# ElectroTime

The ElectroTime is an Arduino-based device that measures the latency of auditory and visual stimuli
in your EEG/MEG lab.

- Project Website: [electrotime.org](https://electrotime.org)
- [Discord Server](https://discord.gg/nQ2GPxXEPy)

[![Website deployment status](https://github.com/JasperVanDenBosch/electrotime/actions/workflows/docs.yml/badge.svg)](https://github.com/JasperVanDenBosch/electrotime/actions/workflows/docs.yml)

![Photograph of an ElectroTime prototype.](https://github.com/JasperVanDenBosch/electrotime/blob/main/docs/assets/device.jpg?raw=true)

## 🗂️ Repository Structure

### `/firmware/`

Contains the embedded code that runs on the Arduino device.

- **`/recorder/`** - Main firmware application for the Arduino Uno
- **`/latreclib/`** - Rust library with supporting logic
- **`/simulator/`** - Firmware for a second device that functions as a simulated EEG lab environment

The firmware is written in Rust using the AVR HAL library.

### `/firmware_C/`

Alpha versions of firmware for quick prototyping during the development phase, in C.

### `/gui/`

Flutter-based cross-platform desktop application for interfacing with the device.

Built with Flutter/Dart for Windows, macOS, and Linux compatibility.

### `/experiment/`

Python scripts for running sample experiments for validation


### `/analysis/`

Data analysis tools and example outputs.


### `/fritzing/`

Hardware schematics and PCB designs. See also the docs/assets/ folder for circuit diagrams.

- **`fritzing_sketch.fzz`** - Complete circuit design
- **`fritzing_sketch_bb.png`** - Breadboard view
- **`TLV2462.fzpz`** - Custom op-amp component


### `/enclosure/`

Model files for the 3D printed case. 

### `/docs/`

Contains the Syrinx-based website documenting the project.

## 👥 Credits

Developed at the University of Leeds. 

Many thanks to participants at the Timing Matters Hackathon at the University of Leeds who contributed code and hardware suggestions.

For questions or support, please open an issue on GitHub or join our [Discord community](https://discord.gg/47mBnvJM).

Made with ❤️ for the global neuroscience community
