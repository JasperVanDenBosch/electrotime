# Hardware Components

## Bill of Materials (BOM)

### Core Components

| Component | Description | Quantity | Approximate Cost |
|-----------|-------------|----------|------------------|
| Arduino Uno Rev3 | ATmega328P microcontroller board | 1 | $25 |
| Photodiode | Light sensor (e.g., BPW21, BPW34) | 1 | $2 |
| Operational Amplifier | Signal amplifier (e.g., LM358, TL072) | 1 | $1 |
| DB37 Female Connector | Parallel port interface | 1 | $5 |
| Resistors | Various values for amplifier circuit | 5-10 | $2 |
| Capacitors | Decoupling and filtering | 3-5 | $2 |
| Breadboard/PCB | Circuit assembly | 1 | $5-15 |
| Jumper Wires | Connections | 20+ | $3 |
| USB Cable | Arduino programming/power | 1 | $5 |

**Total Estimated Cost: ~$50-60**

### Optional Components

| Component | Description | Purpose |
|-----------|-------------|---------|
| 3D Printed Enclosure | Custom housing | Protection and mounting |
| LED Indicators | Status lights | Visual feedback |
| External Power Supply | 5V/9V adapter | Independent power |
| Mounting Hardware | Screws, standoffs | Professional assembly |

## Circuit Design

### Photodiode Amplifier Circuit

The photodiode signal is amplified using a simple operational amplifier circuit:

```
Photodiode (BPW21)
    |
    +-- [10kΩ] -- VCC (5V)
    |
    +-- Op-Amp (+) Input
    |
GND |
    
Op-Amp (-) Input -- [100kΩ feedback] -- Op-Amp Output
    |
    +-- [1kΩ] -- GND

Op-Amp Output --> Arduino A0 (Analog Input)
```

### Digital Input Interface (DB37)

The DB37 connector provides 8-bit digital input from the EEG trigger system:

```
DB37 Pin Mapping:
Pin 2  --> Arduino Digital Pin 2 (LSB)
Pin 3  --> Arduino Digital Pin 3
Pin 4  --> Arduino Digital Pin 4
Pin 5  --> Arduino Digital Pin 5
Pin 6  --> Arduino Digital Pin 6
Pin 7  --> Arduino Digital Pin 7
Pin 8  --> Arduino Digital Pin 8
Pin 9  --> Arduino Digital Pin 9 (MSB)

Pin 18-25 --> GND (Common Ground)
```

### Power Distribution

```
Arduino 5V  -->  Op-Amp VCC
Arduino GND -->  Op-Amp GND, DB37 GND
USB Power   -->  Arduino VIN
```

## Assembly Instructions

### 1. Breadboard Assembly (Prototyping)

1. **Mount Arduino** on breadboard or development board
2. **Wire Photodiode Circuit**:
   - Connect photodiode cathode to Arduino A0 through op-amp
   - Add pull-up resistor (10kΩ) from photodiode anode to 5V
   - Configure op-amp as non-inverting amplifier
3. **Wire DB37 Interface**:
   - Connect DB37 pins 2-9 to Arduino digital pins 2-9
   - Connect DB37 ground pins to Arduino GND
4. **Add Decoupling Capacitors**: 100nF near op-amp power pins
5. **Test Connections** with multimeter

### 2. PCB Assembly (Production)

For a more permanent solution, design a custom PCB:

1. **Schematic Capture**: Use KiCad, Eagle, or similar
2. **PCB Layout**: Minimize noise with proper ground planes
3. **Manufacturing**: Use services like JLCPCB, PCBWay
4. **Assembly**: Solder components following silkscreen

### 3. Enclosure Design

The 3D printed enclosure provides:
- **Protection**: Safe housing for electronics
- **Mounting**: Secure attachment to experimental setup
- **Access**: Ports for USB, DB37, and photodiode
- **Cooling**: Ventilation for Arduino

#### Enclosure Features
- **Material**: PLA or PETG plastic
- **Dimensions**: 120mm x 80mm x 40mm (approximate)
- **Mounting**: Standard 1/4"-20 tripod mount
- **Ports**: Precise cutouts for connectors
- **Assembly**: Snap-fit or screw-together design

## Hardware Specifications

### Electrical Characteristics

| Parameter | Value | Notes |
|-----------|-------|-------|
| Supply Voltage | 5V DC | Via USB or external adapter |
| Current Consumption | <100mA | Typical operation |
| Input Voltage Range | 0-5V | Digital and analog inputs |
| Timing Resolution | 1μs | Based on 16MHz clock |
| ADC Resolution | 10-bit | 1024 levels (0-1023) |
| Digital Input Levels | TTL Compatible | 0V = Low, >2.4V = High |

### Mechanical Characteristics

| Parameter | Value | Notes |
|-----------|-------|-------|
| Operating Temperature | 0-50°C | Typical lab environment |
| Storage Temperature | -20-60°C | Non-condensing |
| Humidity | 0-85% RH | Non-condensing |
| Dimensions | 120x80x40mm | With enclosure |
| Weight | <200g | Complete assembly |

### Optical Characteristics

| Parameter | Value | Notes |
|-----------|-------|-------|
| Photodiode Response | 400-1000nm | Visible + near-IR |
| Light Sensitivity | ~100μA/lux | Typical for BPW21 |
| Response Time | <1μs | Fast photodiode |
| Angular Response | ±30° | Typical acceptance angle |

## Performance Optimizations

### Hardware Optimizations

1. **High-Speed Photodiode**: Use fast photodiodes (BPW21, PIN diodes)
2. **Low-Noise Op-Amp**: TL072 or similar for clean amplification
3. **Short Signal Paths**: Minimize wire lengths for reduced noise
4. **Proper Grounding**: Star ground configuration
5. **Decoupling**: 100nF capacitors near all ICs

### Layout Considerations

1. **Separate Analog/Digital**: Keep analog and digital sections apart
2. **Ground Plane**: Use solid ground plane on PCB
3. **Power Distribution**: Wide traces for power connections
4. **EMI Shielding**: Consider metal enclosure for noisy environments

## Testing and Calibration

### Basic Functionality Test

1. **Power On**: Verify 5V supply to all components
2. **Digital Inputs**: Test DB37 connections with multimeter
3. **Analog Input**: Verify photodiode response to light
4. **Communication**: Test USB serial connection
5. **Timing**: Verify timer operation with oscilloscope

### Calibration Procedure

1. **Dark Calibration**: Record baseline with no light
2. **Light Response**: Test with known light sources
3. **Timing Verification**: Use oscilloscope to verify delays
4. **Temperature Stability**: Test over operating range

## Troubleshooting

### Common Issues

| Problem | Possible Causes | Solutions |
|---------|----------------|-----------|
| No response to light | Photodiode wiring, op-amp power | Check connections and power |
| Noisy readings | Poor grounding, EMI | Add decoupling, improve layout |
| Digital inputs not working | DB37 wiring, voltage levels | Verify connections and voltages |
| USB communication fails | Driver issues, baud rate | Check drivers and settings |

### Debug Tools

- **Multimeter**: Verify voltages and continuity
- **Oscilloscope**: Check signal timing and quality
- **Serial Monitor**: View Arduino debug output
- **Logic Analyzer**: Verify digital signal timing

---

## Files and Resources

- **[Fritzing Diagrams](../fritzing/)**: Visual wiring diagrams
- **[Schematic Files](../hardware/)**: KiCad/Eagle schematics
- **[3D Models](../mechanical/)**: STL files for enclosure
- **[Assembly Photos](../photos/)**: Step-by-step assembly pictures

**Need Help?** [Open an issue on GitHub](https://github.com/JasperVanDenBosch/latency-recorder/issues) for hardware-related questions. 