+++
title = "Hardware"
description = "Circuit design and assembly instructions"
SequenceNumber = 1
+++

# 🔧 Hardware

The "latency recorder" (name TBD) is based on an Arduino Uno Rev3, combined with a photodiode and an Operational amplifier or "op-amp". It also features an DB37 input port better known as a "parallel port" to receive triggers. The electronics are soldered together. A 3d filament printed enclosure has been made to house it. In the current design, it needs to be connected to a PC with a USB cable to continuously upload data points.

## 📐 Current Hardware Specifications

## 📐 Technical Specifications

### Core Processing Unit
| Component | Specification | Rationale |
|-----------|---------------|-----------|
| **Microcontroller** | Arduino Uno Rev3 (ATmega328P) | Proven reliability, extensive ecosystem |
| **Clock Speed** | 16 MHz | Sufficient for 1ms resolution timing |
| **Flash Memory** | 32 KB | Adequate for firmware + data buffering |
| **SRAM** | 2 KB | Handles circular buffers for real-time data |
| **EEPROM** | 1 KB | Stores calibration parameters |
  
### Sensor Subsystem
| Component | Specification | Performance |
|-----------|---------------|-------------|
| **Photodiode** | Silicon PIN type | Response time: <1μs | For detecting visual stimulus onset
| **Spectral Range** | 400-1100nm | Covers visible + near-IR |
| **Op-Amp** | TLV2462 (Rail-to-rail) | Low noise, high precision |
| **ADC Resolution** | 10-bit (0-1023) | 4.9mV resolution |
| **Sampling Rate** | Up to 1000 Hz | Configurable via software |

### Interface Capabilities
- **DB37 Parallel Port**: 8 digital trigger inputs + ground reference
- **USB Serial**: 115200 baud (configurable up to 2M baud)
- **External Power**: 7-12V DC input option
- **Status Indicators**: Multi-color LED for system state

### Power & Connectivity
- **Power**: Via USB (5V) or external power adapter (7-12V)
- **Data Transfer**: USB Serial (115200 baud default)
- **Status LED**: Indicates recording state

## ⚡ Circuit Architecture

### Signal Processing Chain
```
Light Stimulus → Photodiode → Transimpedance Amp → Low-pass Filter → ADC → Digital Processing → USB Output
     ↑              ↑              ↑                    ↑          ↑           ↑              ↑
   <1μs           <1μs          ~10μs              ~100μs      125μs       <1ms          ~1ms
```

## 🔌 Circuit Design

### Photodiode Circuit
The photodiode circuit uses a transimpedance amplifier configuration:
- **Op-Amp**: TLV2462 (Rail-to-rail, low noise)
- **Gain**: Adjustable via feedback resistor
- **Filtering**: Low-pass filter to reduce high-frequency noise

### Signal Flow
1. **Light Detection**: Photodiode converts light to current
2. **Current-to-Voltage**: Op-amp converts current to measurable voltage
3. **ADC Conversion**: Arduino reads analog voltage
4. **Digital Processing**: Timestamps and threshold detection
5. **Serial Output**: Data sent to computer

## 🏗️ Assembly Instructions

### Required Tools
- Soldering iron (15-25W recommended)
- Wire strippers
- Multimeter
- 3D printer (for enclosure)
- Basic hand tools

### Assembly Steps
1. **PCB Preparation**: Clean and inspect the circuit board
2. **Component Placement**: Follow the schematic diagram
3. **Soldering**: Start with low-profile components
4. **Testing**: Check continuity and voltage levels
5. **Enclosure**: Print and assemble the 3D printed case
6. **Final Assembly**: Mount all components securely

## 📊 Performance Characteristics

### Timing Accuracy
- **Sampling Rate**: Up to 1000 Hz
- **Latency**: < 1ms detection time
- **Jitter**: ± 0.5ms typical
- **Resolution**: 10-bit ADC (0-1023 values)

### Environmental Specifications
- **Operating Temperature**: 0°C to 50°C
- **Humidity**: 10% to 90% non-condensing
- **Light Sensitivity**: Adjustable via software threshold

## 💡 Idea 1: Add microphone 🎤

For paradigms with sound stimuli

## 💡 Idea 2: Store data on device 💾

So that the serial connection is not required anymore

## 💡 Idea 3: Improve design of the Enclosure 📦

A better fitting 3D printed enclosure

### Current Enclosure Limitations
- Basic rectangular design
- Limited mounting options
- No cable management
- Photodiode positioning could be improved

### Proposed Improvements
- Modular design for different configurations
- Integrated cable management
- Multiple mounting options (desk, monitor, tripod)
- Better ventilation for heat dissipation
- Clear labeling of ports and indicators

## 🛠️ Hardware Development Resources

### Design Files
- **Fritzing Sketches**: Circuit schematics in `/fritzing/`
- **3D Models**: Enclosure STL files (to be added)
- **PCB Layouts**: KiCad files (future development)

### Component Suppliers
- **Arduino**: [Official Store](https://store.arduino.cc/)
- **Electronic Components**: [Digi-Key](https://www.digikey.com/), [Mouser](https://www.mouser.com/)
- **Photodiodes**: [Thorlabs](https://www.thorlabs.com/), [Edmund Optics](https://www.edmundoptics.com/)
- **3D Printing**: [Prusaprinters](https://www.prusaprinters.org/), [Thingiverse](https://www.thingiverse.com/)

### Useful References
- 📚 [Arduino Hardware Reference](https://www.arduino.cc/reference/en/)
- 🔧 [Op-Amp Basics](https://www.analog.com/en/education/education-library/op-amp-basics.html)
- 📸 [Photodiode Circuits](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=285)
- 🖨️ [3D Printing Guide](https://www.prusaprinters.org/prints/)

## 📋 Testing & Calibration

### Hardware Testing Checklist
- [ ] Power supply voltage (5V ± 0.25V)
- [ ] Op-amp output range (0-5V)
- [ ] Photodiode dark current
- [ ] Serial communication reliability
- [ ] Trigger input functionality
- [ ] Temperature stability

### Calibration Procedures
1. **Dark Calibration**: Measure baseline with no light
2. **Light Calibration**: Test with known light source
3. **Timing Verification**: Compare with oscilloscope
4. **Trigger Testing**: Verify all parallel port pins

## 🔮 Future Hardware Roadmap

### Short-term Goals
- Implement microphone support
- Improve serial throughput
- Design modular enclosure
- Create assembly video tutorial

### Long-term Vision
- Wireless data transmission
- Multi-sensor support
- Standalone operation with display
- Professional PCB design
- CE/FCC certification for wider distribution
