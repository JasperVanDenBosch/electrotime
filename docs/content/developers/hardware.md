+++
title = "Hardware Development"
description = "Guide for hardware developers working on the Latency Recorder"
SequenceNumber = 10
+++

# Hardware Development

This section contains information for hardware developers working on the Latency Recorder project.

## Firmware Documentation

The latency recorder firmware is written in Rust and consists of three main components:

### Core Library (latreclib)
A `#![no_std]` library providing helper functions and abstractions for the latency recorder hardware.

### Recorder Firmware
The main firmware application that runs on the Arduino hardware. This handles:
- ADC sampling at high frequency
- Serial communication with the host computer
- Timing and synchronization
- Hardware control

### Simulator
A hardware simulator that allows testing the firmware logic without physical Arduino hardware.

## API Documentation

### 📚 Rust Firmware API

> **[📖 View latreclib API Documentation →](/docs-api/firmware/latreclib/)**  
> Core library with helper functions for bit manipulation and hardware abstraction

The firmware documentation includes:
- **Bit manipulation functions**: `bools2num()` and `num2bools()` for converting between boolean arrays and numeric values
- **Hardware abstractions**: Low-level interfaces for AVR microcontroller
- **Usage examples**: Comprehensive code examples for all functions

### Generating Documentation

To regenerate the API documentation for the firmware:

```bash
./generate-docs.sh
```

Note: The recorder and simulator documentation requires the AVR toolchain to be properly configured.

## Hardware Components

### Arduino Nano
- ATmega328P microcontroller
- 16 MHz clock speed
- 10-bit ADC with up to 15 kHz sampling rate
- Serial communication at 115200 baud

### Signal Conditioning
- TLV2462 op-amp for signal amplification
- Voltage divider for input protection
- Low-pass filtering for noise reduction

## Development Setup

1. Install Rust and required targets:
   ```bash
   rustup target add avr-unknown-gnu-atmega328
   ```

2. Install AVR toolchain (macOS):
   ```bash
   brew tap osx-cross/avr
   brew install avr-gcc avrdude
   ```

3. Build the firmware:
   ```bash
   cd firmware/recorder
   cargo build --release
   ```

4. Flash to Arduino:
   ```bash
   avrdude -p atmega328p -c arduino -P /dev/tty.usbserial-* -b 115200 -U flash:w:target/avr-atmega328p/release/recorder.elf:e
   ```