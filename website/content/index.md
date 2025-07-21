# Latency Recorder

## Precision Timing for EEG Research

The **Latency Recorder** is an Arduino Uno Rev3-based precision measurement system designed specifically for electroencephalography (EEG) experiments. It accurately measures the latency between stimulus triggers and actual visual stimulus presentation, addressing a critical need in neuroscience research.

## 🎯 Project Overview

This project was developed during the **Timing Matters Hackathon** to solve precision timing challenges in EEG experiments. Many EEG setups suffer from unknown delays between when a stimulus trigger is sent and when the visual stimulus actually appears on screen. The Latency Recorder provides microsecond-accurate measurements of these delays.

## ⚡ Key Features

- **High Precision**: Microsecond-accurate timing measurements
- **DB37 Parallel Port Input**: Standard interface for EEG trigger systems
- **Photodiode Detection**: Direct measurement of actual light output
- **Cross-Platform GUI**: Flutter-based interface for Windows, macOS, and Linux
- **Real-time Monitoring**: Live data display and logging
- **Open Source**: MIT licensed hardware and software designs
- **3D Printed Enclosure**: Complete assembly instructions included

## 🔬 Perfect for Research

- **EEG Experiments**: Measure stimulus presentation latency
- **Psychophysics Studies**: Verify timing accuracy
- **Display Calibration**: Characterize monitor response times
- **System Validation**: Verify experimental timing setup

## 🚀 Performance Optimizations

Our firmware uses advanced optimization techniques to minimize measurement latency:

- **Direct Port Manipulation**: 10x faster than standard Arduino digitalWrite() based on research from [Instructables](https://www.instructables.com/Arduino-is-Slow-and-how-to-fix-it/)
- **Compiler Optimizations**: Level 2 optimization for best performance-stability balance as recommended by [Elektor Magazine](https://www.elektormagazine.com/labs/arduino-compiler-optimizations-for-faster-smaller-code)
- **Rust AVR HAL**: Modern, zero-cost abstractions for maximum efficiency
- **Inline Assembly**: Critical timing sections use optimized assembly code

## 📊 Technical Specifications

- **Microcontroller**: Arduino Uno Rev3 (ATmega328P)
- **Input Sampling**: 15.625 kHz (64μs per sample)
- **Timer Resolution**: 16-bit counter with 1024 prescaler
- **Maximum Recording**: 4 seconds per epoch (62,500 samples)
- **Data Interface**: USB Serial (115200 baud)
- **Trigger Interface**: DB37 parallel port (8-bit)

## 🏆 Hackathon Achievement

This project demonstrates how open-source hardware and modern software development can solve real scientific problems. Built in a single hackathon day, it showcases rapid prototyping of precision measurement systems.

---

## Getting Started

1. **[Hardware Setup](hardware.md)** - Build or order the components
2. **[Software Installation](software.md)** - Install firmware and GUI
3. **[User Guide](guide.md)** - Complete setup and usage instructions
4. **[GitHub Repository](https://github.com/JasperVanDenBosch/latency-recorder)** - Source code and designs

---

*Built during the Timing Matters Hackathon • Open Source Hardware & Software • MIT License* 