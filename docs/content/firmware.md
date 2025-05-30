+++
title = "Firmware"
description = "Device firmware written in Rust with AVR_HAL"
SequenceNumber = 2
+++

# 💻 Firmware

The device firmware is written in Rust with the [AVR_HAL](https://github.com/Rahix/avr-hal) library.

Currently here is the basic functionality:

1. Read out the photodiode
2. Read out the trigger input
3. Read the state of the clock
4. Send data to serial port buffer: light, trigger, tval

Clock limits

- 15625Hz, or 64us / timepoint.
- max val is 2ˆ16 = 65536 = 4.19s

So we run “epochs” or batches of samples

## 📚 Preparation

- 📥 Clone the git repository
- 🦀 Install Rust and Cargo
- 📦 Install the dependencies using Cargo

## 💡 Idea 1: Improve performance ⚡

The serial package can be optimized. This is currently the bottleneck.

Serial seems to be using UART (default for Arduino’s), effectively from what I've read this means its a 1 -> 0.8 for Baud to Bit rates (due to a leading and ending bit).

A potential way to increase data throughput would be to use a different serial protocol, effectively gaining more bits per baud cycle (effectively doubling or even up to octupling data speed).

I'm know the Arduino can't natively do this with its software, but I'm sure if it can be programed to use these other baud rates or if their will need to be additional hardware added. Might be worth looking into though

### Notes

Minor performance check, unrelated to serial writing, but reading over analog is slightly slower then digital read. Could use a slight hardware alteration to check if a digital pin is active using flash ACD. This however will obviously loose some amount of precision, from reading the accuracy of most flash ACD's are 8 bits compared to the analog read of the Arduino's as 10 bits. Effectively though, if all we need to know is if the light is above a threshold or not, then digital reading the outputs of some of these pins could be an improvement.

## 💡 Idea 2: Adapt to new hardware design 🔩

If we build a circuit with a microphone or SD card, we need to update the firmware.

Specification also mentions local network data sharing, could look into Lab Streaming Layer outlet streams?

Will need a WiFi shield.

## 📁 Code Structure

### Project Layout

```bash
firmware/
├── latreclib/          # Core library
│   ├── src/
│   │   ├── lib.rs     # Main library interface
│   │   ├── sensor.rs  # Sensor reading logic
│   │   └── serial.rs  # Serial communication
│   └── Cargo.toml
├── recorder/           # Arduino application
│   ├── src/
│   │   └── main.rs    # Main application loop
│   └── Cargo.toml
└── simulator/          # Hardware simulator
    ├── src/
    │   └── main.rs    # Simulation logic
    └── Cargo.toml
```

### Key Components

#### Main Loop (recorder/src/main.rs)

- Initializes hardware peripherals
- Reads sensor values
- Monitors trigger inputs
- Sends timestamped data via serial

#### Library Functions (latreclib/)

- Abstracts hardware interactions
- Provides reusable components
- Handles low-level timing

## 🚀 Development Setup

### Prerequisites

1. **Install Rust**:

   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

2. **Add AVR toolchain**:

   ```bash
   rustup toolchain install nightly
   rustup +nightly component add rust-src
   ```

3. **Install dependencies**:

   ```bash
   cargo install ravedude
   cargo install cargo-generate
   ```

### Building the Firmware

```bash
cd firmware/recorder
cargo build --release
```

### Flashing to Arduino

```bash
# Make sure Arduino is connected via USB
cargo run --release
```

## 🐛 Debugging Techniques

### Serial Debugging

- Use `ufmt` for formatted output (smaller than standard `println!`)
- Monitor serial output at 115200 baud
- Add debug flags for verbose output

### LED Indicators

- Use built-in LED for status indication
- Blink patterns for different states
- Error codes via LED sequences

### Logic Analyzer

- Monitor digital signals directly
- Verify timing accuracy
- Debug protocol implementations

## 📈 Performance Optimization

### Current Bottlenecks

1. **Serial Communication**: Limited by UART speed
2. **ADC Conversion**: Takes ~100 microseconds
3. **Memory Constraints**: Only 2KB RAM available

### Optimization Strategies

- **Interrupt-driven I/O**: Reduce polling overhead
- **Circular Buffers**: Efficient data management
- **Bit Packing**: Compress data before transmission
- **DMA Usage**: Direct memory access for transfers

## 🔗 Useful Links

### Rust Embedded Resources

- 🦀 [AVR HAL Documentation](https://rahix.github.io/avr-hal/)
- 📚 [Embedded Rust Book](https://docs.rust-embedded.org/book/)
- 🛠️ [AVR Microcontrollers](https://github.com/avr-rust/awesome-avr-rust)
- 💡 [Rust Embedded Examples](https://github.com/rust-embedded/awesome-embedded-rust)

### Arduino & AVR References

- 📖 [ATmega328P Datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
- 🔧 [Arduino Pinout](https://docs.arduino.cc/hardware/uno)
- ⚡ [AVR Instruction Set](https://ww1.microchip.com/downloads/en/devicedoc/atmel-0856-avr-instruction-set-manual.pdf)

### Serial Communication

- 📡 [UART Protocol](https://www.analog.com/en/analog-dialogue/articles/uart-a-hardware-communication-protocol.html)
- 🚀 [High-Speed Serial](https://www.silabs.com/documents/public/application-notes/an0065.0-efr32-usart-spi-master-slave.pdf)
- 📊 [Serial Protocols Comparison](https://www.seeedstudio.com/blog/2019/09/25/uart-vs-i2c-vs-spi/)

## 🧪 Testing Framework

### Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_sensor_reading() {
        // Test sensor value processing
    }
}
```

### Integration Tests

- Hardware-in-the-loop testing
- Automated test fixtures
- Performance benchmarks

### Simulator Testing

- Test without physical hardware
- Rapid development iteration
- Edge case exploration

## 🎯 Contributing to Firmware

### Code Style

- Follow Rust formatting guidelines
- Use `cargo fmt` before committing
- Run `cargo clippy` for linting

### Documentation

- Document public APIs
- Include examples in doc comments
- Update README for major changes

### Pull Request Process

1. Create feature branch
2. Write tests for new features
3. Ensure all tests pass
4. Update documentation
5. Submit PR with clear description
