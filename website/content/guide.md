# User Guide

## Quick Start

### What You'll Need

- ✅ **Assembled Latency Recorder** ([Hardware Guide](hardware.md))
- ✅ **USB Cable** (Arduino to computer)
- ✅ **DB37 Cable** (to your EEG trigger system)
- ✅ **Computer** (Windows, macOS, or Linux)
- ✅ **Display** (for stimulus presentation)

### 5-Minute Setup

1. **Connect Hardware**
   - Plug Arduino into computer via USB
   - Connect DB37 cable to your EEG trigger system
   - Position photodiode sensor near display

2. **Install Software**
   - Download GUI from [GitHub Releases](https://github.com/JasperVanDenBosch/latency-recorder/releases)
   - Install for your platform (Windows/Mac/Linux)

3. **Upload Firmware**
   - Use Arduino IDE or command line tools
   - Flash the optimized Rust firmware

4. **Start Measuring**
   - Launch GUI application
   - Select Arduino port
   - Begin recording latency data

---

## Detailed Setup Instructions

### 1. Hardware Assembly

If you haven't built the hardware yet, follow the **[Hardware Guide](hardware.md)** for complete assembly instructions.

#### Verification Checklist
- [ ] Arduino powers on (LED indicators)
- [ ] Photodiode responds to light (test with flashlight)
- [ ] DB37 connections secure
- [ ] USB communication established

### 2. Software Installation

#### Option A: Pre-built Releases (Recommended)

1. **Download** the latest release for your platform:
   - **Windows**: `latency-recorder-windows.exe`
   - **macOS**: `latency-recorder-macos.dmg`
   - **Linux**: `latency-recorder-linux.AppImage`

2. **Install** following platform-specific instructions:
   ```bash
   # Windows: Run installer
   ./latency-recorder-windows.exe
   
   # macOS: Mount and drag to Applications
   open latency-recorder-macos.dmg
   
   # Linux: Make executable and run
   chmod +x latency-recorder-linux.AppImage
   ./latency-recorder-linux.AppImage
   ```

#### Option B: Build from Source

1. **Install Dependencies**:
   ```bash
   # Install Flutter SDK
   flutter --version
   
   # Install Rust toolchain
   rustup install nightly-2024-05-01
   
   # Install AVR tools
   sudo apt install gcc-avr binutils-avr avr-libc  # Linux
   brew install avr-gcc avr-binutils avr-libc      # macOS
   ```

2. **Clone and Build**:
   ```bash
   git clone https://github.com/JasperVanDenBosch/latency-recorder
   cd latency-recorder
   
   # Build firmware
   cd firmware/recorder
   cargo build --release
   
   # Build GUI
   cd ../../gui
   flutter build [linux|windows|macos] --release
   ```

### 3. Firmware Upload

#### Using Arduino IDE (Beginner-Friendly)

1. **Install Arduino IDE** from [arduino.cc](https://www.arduino.cc/en/software)
2. **Open firmware sketch** (if available) or use command line
3. **Select board**: Arduino Uno
4. **Select port**: Your Arduino's USB port
5. **Upload** the firmware

#### Using Command Line (Advanced)

```bash
# Convert Rust binary to hex format
avr-objcopy -O ihex target/avr-atmega328p/release/recorder.elf recorder.hex

# Upload using avrdude
avrdude -c arduino -p atmega328p -P /dev/ttyUSB0 -U flash:w:recorder.hex

# Windows: Use COM port (e.g., COM3)
# macOS: Use /dev/cu.usbmodem* 
# Linux: Use /dev/ttyUSB* or /dev/ttyACM*
```

---

## Using the System

### 1. Starting the GUI Application

1. **Launch** the Latency Recorder GUI
2. **Select Arduino Port** from the dropdown menu
3. **Verify Connection** (status indicator turns green)
4. **Check Photodiode** (light level readings update)

### 2. Basic Measurement

#### Simple Latency Test

1. **Position Photodiode**: Place sensor near display area where stimuli appear
2. **Configure Settings**:
   - **Sampling Rate**: 15.625 kHz (default)
   - **Epoch Length**: 4 seconds (default)
   - **Trigger Threshold**: Adjust based on your system
3. **Start Recording**: Click "Start" button
4. **Generate Stimulus**: Use your EEG software to present stimulus
5. **Stop Recording**: Click "Stop" or wait for epoch to complete
6. **View Results**: Check latency measurements and statistics

#### Advanced Configuration

```yaml
# Configuration options
sampling_rate: 15625  # Hz
epoch_length: 4.0     # seconds  
trigger_threshold: 2.5  # volts
photodiode_threshold: 100  # ADC units
data_format: csv      # csv, json
auto_save: true       # automatic file saving
```

### 3. Interpreting Results

#### Data Columns

| Column | Description | Units | Example |
|--------|-------------|-------|---------|
| `epoch` | Recording session number | integer | 0, 1, 2... |
| `timestamp_us` | Time since epoch start | microseconds | 0, 64, 128... |
| `light_level` | Photodiode reading | ADC units (0-1023) | 150, 800, 200... |
| `trigger_value` | Digital trigger state | 8-bit integer | 0, 1, 255... |
| `calculated_latency` | Measured delay | microseconds | 16000, 18500... |

#### Typical Results

```csv
epoch,timestamp_us,light_level,trigger_value,calculated_latency
0,0,120,0,
0,64,125,0,
0,15872,130,1,      # Trigger detected
0,15936,135,1,
0,32000,800,1,      # Light detected  
0,32064,820,1,      # Latency = 32000 - 15872 = 16128 μs
```

**Interpretation**: The stimulus trigger occurred at 15.872ms, and the light was detected at 32.000ms, giving a **16.128ms latency**.

### 4. Data Analysis

#### Using Built-in GUI Analysis

1. **Statistics Panel**: View mean, std dev, min/max latencies
2. **Histogram**: Distribution of latency measurements  
3. **Time Series**: Latency over time
4. **Export**: Save data as CSV/JSON for external analysis

#### Using Python Analysis Scripts

```python
# Load and analyze data
import pandas as pd
import matplotlib.pyplot as plt

# Read measurement file
data = pd.read_csv('measurements_2024-05-30.csv')

# Calculate statistics
latencies = data.dropna(subset=['calculated_latency'])['calculated_latency']
mean_lat = latencies.mean() / 1000  # Convert to ms
std_lat = latencies.std() / 1000

print(f"Mean latency: {mean_lat:.2f} ± {std_lat:.2f} ms")

# Plot distribution
plt.hist(latencies / 1000, bins=30, alpha=0.7)
plt.xlabel('Latency (ms)')
plt.ylabel('Count')
plt.title('Stimulus Presentation Latency')
plt.show()
```

---

## Experimental Setup Guidelines

### 1. Photodiode Placement

#### Optimal Positioning
- **Location**: Corner or edge of display
- **Distance**: 2-5mm from screen surface
- **Angle**: Perpendicular to screen (~90°)
- **Coverage**: Ensure stimulus will illuminate sensor

#### Common Placements

```
┌─────────────────────────────────┐
│ Display Screen                  │
│                                 │
│  [●] ← Photodiode here          │
│     (top-left corner)           │
│                                 │
│                                 │
│              OR                 │
│                                 │
│                     [●] ←       │
│                (bottom-right)   │
└─────────────────────────────────┘
```

### 2. Trigger System Integration

#### Standard EEG Setups

| EEG System | Trigger Method | Connection |
|------------|----------------|------------|
| **BrainVision** | Parallel port | DB37 directly |
| **NetStation** | TTL triggers | DB37 via adapter |
| **OpenViBE** | Serial/parallel | Custom interface |
| **PsychoPy** | Parallel port | Standard DB37 |
| **E-Prime** | Parallel port | Standard DB37 |

#### Trigger Timing

```python
# Example PsychoPy integration
from psychopy import visual, core, parallel

# Setup
win = visual.Window()
port = parallel.ParallelPort(address=0x378)

# Stimulus presentation with trigger
def present_stimulus():
    # Send trigger BEFORE preparing stimulus
    port.setData(1)  # Trigger = 1
    
    # Create and draw stimulus
    stim = visual.TextStim(win, text="Hello")
    stim.draw()
    win.flip()  # This is when light appears
    
    # Clear trigger
    core.wait(0.01)  # 10ms trigger duration
    port.setData(0)
```

### 3. Calibration Procedure

#### Initial Calibration

1. **Dark Baseline**: Record with display off
   ```
   Expected: light_level ≈ 50-150 (dark level)
   ```

2. **Bright Reference**: Record with white screen
   ```
   Expected: light_level ≈ 800-1000 (bright level)
   ```

3. **Trigger Test**: Send known trigger patterns
   ```
   Send: 0, 1, 2, 4, 8, 16, 32, 64, 128, 255
   Verify: trigger_value matches sent values
   ```

4. **Timing Verification**: Use oscilloscope (if available)
   ```
   Measure: Trigger output to light detection
   Compare: With Latency Recorder measurements
   ```

#### Ongoing Calibration

- **Daily**: Check dark/bright levels
- **Weekly**: Verify trigger connections  
- **Monthly**: Full timing verification
- **Per experiment**: Document setup parameters

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Arduino Not Detected

**Symptoms**: GUI shows "No Arduino found"

**Solutions**:
- Check USB cable connection
- Verify Arduino powers on (LED indicators)
- Try different USB port
- Install Arduino drivers (Windows)
- Check permissions (Linux): `sudo usermod -a -G dialout $USER`

**Linux Serial Port Permissions**:
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Or temporary permission
sudo chmod 666 /dev/ttyUSB0
```

#### 2. No Light Detection

**Symptoms**: `light_level` doesn't change with display

**Solutions**:
- Verify photodiode wiring
- Check op-amp power supply
- Adjust photodiode position
- Test with flashlight
- Verify ADC reference voltage

**Debug Commands**:
```bash
# Test analog input directly
arduino-cli board list
arduino-cli monitor -p /dev/ttyUSB0 -c baudrate=115200
```

#### 3. Trigger Not Working

**Symptoms**: `trigger_value` always 0 or constant

**Solutions**:
- Check DB37 cable connections
- Verify EEG software trigger output
- Test with multimeter (should see 0-5V)
- Check Arduino digital pin configuration
- Verify common ground connection

**Trigger Testing**:
```python
# Test trigger with simple script
import serial
import time

# Manual trigger test
ser = serial.Serial('/dev/ttyUSB0', 115200)
while True:
    line = ser.readline().decode().strip()
    print(f"Data: {line}")
    time.sleep(0.1)
```

#### 4. Noisy Measurements

**Symptoms**: Erratic readings, false triggers

**Solutions**:
- Add decoupling capacitors
- Improve grounding
- Shield cables
- Reduce wire lengths
- Filter in software

**Noise Reduction**:
```python
# Software filtering example
import numpy as np
from scipy import signal

# Low-pass filter
def filter_signal(data, cutoff=1000, fs=15625):
    nyquist = fs / 2
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(4, normal_cutoff, btype='low')
    return signal.filtfilt(b, a, data)
```

#### 5. Timing Accuracy Issues

**Symptoms**: Inconsistent latency measurements

**Solutions**:
- Verify hardware timer configuration
- Check for interrupt conflicts
- Optimize firmware timing loops
- Use oscilloscope for verification
- Calibrate against known delays

### Performance Optimization

#### Firmware Optimization
- **Reduce Serial Output**: Lower data rate if needed
- **Optimize Sampling**: Adjust sample rate for your application
- **Minimize Interrupts**: Disable unnecessary Arduino features

#### System Optimization
- **Dedicated USB Port**: Use isolated USB connection
- **Real-time Priority**: Set GUI to high priority
- **Disable Power Management**: Prevent USB sleep mode

```bash
# Linux: Disable USB power management
echo -1 > /sys/module/usbcore/parameters/autosuspend

# Windows: Device Manager > USB settings > Power management
# Uncheck "Allow computer to turn off this device"
```

---

## Advanced Usage

### 1. Custom Firmware Modifications

#### Changing Sample Rate

```rust
// In main.rs: Modify timer prescaler
// Current: 15625 Hz (1024 prescaler)
timer1.tccr1b.write(|w| w.cs1().prescale_1024());

// Faster: 31250 Hz (512 prescaler) 
timer1.tccr1b.write(|w| w.cs1().prescale_512());

// Slower: 7812.5 Hz (2048 prescaler)
timer1.tccr1b.write(|w| w.cs1().prescale_2048());
```

#### Adding Digital Outputs

```rust
// Add status LED
let mut status_led = pins.d13.into_output();

// In main loop
status_led.set_high();  // Recording active
// ... measurement code ...
status_led.set_low();   // Recording inactive
```

### 2. Integration with Research Software

#### PsychoPy Integration

```python
# psychopy_latency_recorder.py
import serial
import threading
import queue

class LatencyRecorder:
    def __init__(self, port='/dev/ttyUSB0'):
        self.ser = serial.Serial(port, 115200)
        self.data_queue = queue.Queue()
        self.recording = False
        
    def start_recording(self):
        self.recording = True
        self.thread = threading.Thread(target=self._read_data)
        self.thread.start()
        
    def _read_data(self):
        while self.recording:
            line = self.ser.readline().decode().strip()
            self.data_queue.put(line)
            
    def get_latest_data(self):
        data = []
        while not self.data_queue.empty():
            data.append(self.data_queue.get())
        return data
```

#### MATLAB Integration

```matlab
% matlab_latency_recorder.m
function data = read_latency_recorder(port, duration)
    % Connect to Arduino
    s = serialport(port, 115200);
    
    % Read data for specified duration
    tic;
    data = {};
    i = 1;
    
    while toc < duration
        if s.NumBytesAvailable > 0
            line = readline(s);
            data{i} = char(line);
            i = i + 1;
        end
    end
    
    % Clean up
    clear s;
end
```

### 3. Batch Processing

#### Automated Analysis Pipeline

```python
# batch_analysis.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def process_session_folder(folder_path):
    """Process all CSV files in a session folder"""
    results = {}
    
    for csv_file in Path(folder_path).glob('*.csv'):
        data = pd.read_csv(csv_file)
        latencies = data.dropna(subset=['calculated_latency'])['calculated_latency']
        
        results[csv_file.stem] = {
            'mean_latency': latencies.mean(),
            'std_latency': latencies.std(),
            'n_measurements': len(latencies),
            'outliers': len(latencies[abs(latencies - latencies.mean()) > 3 * latencies.std()])
        }
    
    return results

def generate_report(results, output_path):
    """Generate summary report"""
    df = pd.DataFrame(results).T
    df.to_csv(output_path)
    
    # Create summary plot
    plt.figure(figsize=(12, 8))
    plt.errorbar(range(len(df)), df['mean_latency'], yerr=df['std_latency'], 
                fmt='o-', capsize=5)
    plt.xlabel('Session')
    plt.ylabel('Latency (μs)')
    plt.title('Latency Measurements Across Sessions')
    plt.xticks(range(len(df)), df.index, rotation=45)
    plt.tight_layout()
    plt.savefig(output_path.replace('.csv', '.png'), dpi=300)
```

---

## Data Management

### File Organization

```
experiment_data/
├── 2024-05-30_session1/
│   ├── measurements_001.csv
│   ├── measurements_002.csv
│   └── session_config.json
├── 2024-05-30_session2/
│   ├── measurements_001.csv
│   └── session_config.json
└── analysis/
    ├── summary_report.csv
    ├── combined_data.csv
    └── plots/
        ├── latency_distribution.png
        └── session_comparison.png
```

### Backup and Archival

1. **Immediate Backup**: Copy to external drive daily
2. **Cloud Storage**: Sync important results to cloud
3. **Version Control**: Use Git for analysis scripts
4. **Documentation**: Keep detailed lab notebooks

---

## Getting Help

### Support Resources

- **[GitHub Issues](https://github.com/JasperVanDenBosch/latency-recorder/issues)**: Bug reports and feature requests
- **[Discussions](https://github.com/JasperVanDenBosch/latency-recorder/discussions)**: Community support
- **[Wiki](https://github.com/JasperVanDenBosch/latency-recorder/wiki)**: Extended documentation
- **Email Support**: Contact project maintainers

### Contributing

- **Bug Reports**: Use GitHub Issues template
- **Feature Requests**: Describe use case and requirements  
- **Code Contributions**: Follow contribution guidelines
- **Documentation**: Help improve guides and tutorials

**Ready to start measuring?** Download the latest release and begin exploring the precision timing capabilities of your experimental setup! 