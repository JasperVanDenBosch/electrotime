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

The firmware is documented using Rust's built-in documentation system. The API documentation includes:

- **Bit manipulation functions**: `bools2num()` and `num2bools()` for converting between boolean arrays and numeric values
- **Hardware abstractions**: Low-level interfaces for AVR microcontroller
- **Usage examples**: Comprehensive code examples for all functions

### View API Documentation

<div style="margin: 2rem 0; padding: 1.5rem; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 0.5rem;">
  <h4 style="margin-top: 0;">📚 Rust Firmware API Reference</h4>
  <p>Explore the complete API documentation for the latreclib core library.</p>
  <a href="/developers/hardware-api" style="display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem; background: #3b82f6; color: white; text-decoration: none; border-radius: 0.25rem;">
    View API Documentation →
  </a>
</div>

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