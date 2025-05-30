+++
title = "Firmware"
description = "Device firmware written in Rust with AVR_HAL"
SequenceNumber = 3
+++

# 💻 Firmware

The device firmware is written in Rust with the [AVR_HAL](https://github.com/Rahix/avr-hal) library.

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

## 🔗 Useful Links

🦀 AVR HAL <https://github.com/Rahix/avr-hal>
