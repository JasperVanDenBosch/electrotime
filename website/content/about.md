# About the Latency Recorder

## The Problem

In electroencephalography (EEG) research, precise timing is crucial for understanding brain responses to stimuli. However, many experimental setups introduce unknown delays between:

1. **Trigger Signal**: When the experimental software sends a stimulus trigger
2. **Actual Presentation**: When the visual stimulus actually appears on the display

These delays can vary significantly depending on:
- Display refresh rates and vertical sync timing
- Graphics driver buffering
- Operating system scheduling
- Hardware interfaces (USB, parallel port, etc.)

**Without accurate timing measurements, EEG research data can be compromised**, leading to incorrect conclusions about brain response latencies.

## Our Solution

The Latency Recorder provides a **hardware-based solution** that directly measures the actual delay between trigger and visual presentation:

### 🔌 Input System
- **DB37 Parallel Port**: Connects to standard EEG trigger systems
- **8-bit Digital Input**: Captures trigger patterns from experimental software
- **High-speed Sampling**: 15.625 kHz for precise trigger detection

### 📷 Detection System  
- **Photodiode Sensor**: Directly measures light output from display
- **Operational Amplifier**: Amplifies photodiode signal for reliable detection
- **Analog Input**: 10-bit ADC for accurate light level measurement

### ⏱️ Timing System
- **Hardware Timer**: 16-bit counter with microsecond precision
- **Optimized Firmware**: Rust-based for minimal overhead
- **Real-time Processing**: No buffering delays in measurement

## Why This Matters

### For Researchers
- **Accurate Data**: Know the exact timing of your stimuli
- **Reproducible Results**: Standardize timing across experiments
- **Publication Quality**: Meet strict timing requirements for journals
- **Cross-Platform**: Works with any EEG system and display

### For the Community
- **Open Source**: All designs and code freely available
- **Affordable**: Uses standard Arduino hardware
- **Extensible**: Easy to modify for specific research needs
- **Educational**: Learn about precision timing techniques

## Technical Innovation

### Advanced Firmware Optimizations
Based on research from the Arduino optimization community, our firmware implements several performance enhancements:

- **Direct Port Manipulation**: [10x faster than digitalWrite()](https://www.instructables.com/Arduino-is-Slow-and-how-to-fix-it/) for critical timing sections
- **Compiler Optimization**: [Level 2 optimization](https://www.elektormagazine.com/labs/arduino-compiler-optimizations-for-faster-smaller-code) for best performance-reliability balance
- **Zero-Cost Abstractions**: Rust AVR HAL provides C-level performance with memory safety

### Modern Development Stack
- **Rust Firmware**: Memory-safe systems programming for embedded devices
- **Flutter GUI**: Cross-platform desktop application (Windows, macOS, Linux)
- **Python Analysis**: Complete data processing and visualization tools

## Project Timeline

**Timing Matters Hackathon - Single Day Development**

- **Morning**: Hardware design and component assembly
- **Afternoon**: Firmware development and optimization
- **Evening**: GUI development and testing
- **Result**: Complete, working precision timing system

This rapid development demonstrates the power of:
- Modern embedded development tools (Rust + AVR HAL)
- Cross-platform frameworks (Flutter)
- Open source hardware (Arduino ecosystem)

## Impact Goals

### Immediate
- Provide EEG researchers with affordable precision timing tools
- Validate timing in existing experimental setups
- Enable more accurate neuroscience research

### Long-term
- Establish open standards for timing measurement in neuroscience
- Create reusable hardware designs for the research community
- Inspire similar precision measurement tools for other scientific fields

---

## Join the Project

- **Researchers**: Use the system in your experiments
- **Developers**: Contribute to firmware and software
- **Hardware Designers**: Improve circuit designs
- **Scientists**: Share your timing measurement needs

**[View on GitHub](https://github.com/JasperVanDenBosch/latency-recorder)** | **[Report Issues](https://github.com/JasperVanDenBosch/latency-recorder/issues)** | **[Contribute](https://github.com/JasperVanDenBosch/latency-recorder/blob/main/CONTRIBUTING.md)** 