+++
title = "Data Analysis"
description = "Python-based data analysis tools for recorded data"
SequenceNumber = 3
+++

# 📊 Data Analysis

The current code can be found under "analysis" in the repository. 📂

## 📚 Preparation

- 📥 Clone the git repository
- 🐍 Install python
- 📦 Install python dependencies

## 📈 Data Format

### Binary Data Structure

The latency recorder outputs binary data with the following format:

```
[timestamp (4 bytes)][sensor_value (2 bytes)][trigger_state (1 byte)]
```

### Data Fields

- **Timestamp**: Microseconds since device start (uint32)
- **Sensor Value**: ADC reading from photodiode (0-1023)
- **Trigger State**: Parallel port pin states (8 bits)

### Sample Rate

- Default: 1000 Hz (1ms intervals)
- Configurable via firmware constants

## 🔍 Analysis Scripts

### Basic Data Reading

```python
import struct
import numpy as np

def read_latency_data(filename):
    """Read binary data from latency recorder"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Parse binary data
    records = []
    for i in range(0, len(data), 7):  # 7 bytes per record
        if i + 7 <= len(data):
            timestamp, sensor, trigger = struct.unpack('<IHB', data[i:i+7])
            records.append({
                'timestamp': timestamp,
                'sensor': sensor,
                'trigger': trigger
            })
    
    return records
```

### Latency Calculation

```python
def calculate_latencies(data):
    """Calculate latencies between trigger and light detection"""
    latencies = []
    
    for i in range(1, len(data)):
        # Detect trigger onset (rising edge)
        if data[i]['trigger'] > 0 and data[i-1]['trigger'] == 0:
            trigger_time = data[i]['timestamp']
            
            # Find corresponding light onset
            for j in range(i, min(i+1000, len(data))):  # Search 1 second
                if data[j]['sensor'] > threshold:
                    light_time = data[j]['timestamp']
                    latency = (light_time - trigger_time) / 1000  # Convert to ms
                    latencies.append(latency)
                    break
    
    return latencies
```

## 📊 Visualization Examples

### Latency Distribution

```
import matplotlib.pyplot as plt

def plot_latency_distribution(latencies):
    """Plot histogram of measured latencies"""
    plt.figure(figsize=(10, 6))
    plt.hist(latencies, bins=50, alpha=0.7, color='blue', edgecolor='black')
    plt.xlabel('Latency (ms)')
    plt.ylabel('Count')
    plt.title('Stimulus Presentation Latency Distribution')
    plt.axvline(np.mean(latencies), color='red', linestyle='--', 
                label=f'Mean: {np.mean(latencies):.2f} ms')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
```

### Time Series Plot

```python
def plot_time_series(data, start_idx=0, duration=5000):
    """Plot sensor values and triggers over time"""
    # Extract time window
    window = data[start_idx:start_idx+duration]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Plot sensor values
    times = [d['timestamp']/1000 for d in window]  # Convert to ms
    sensors = [d['sensor'] for d in window]
    ax1.plot(times, sensors, 'b-', linewidth=0.5)
    ax1.set_ylabel('Sensor Value')
    ax1.set_title('Photodiode Response')
    ax1.grid(True, alpha=0.3)
    
    # Plot triggers
    triggers = [d['trigger'] for d in window]
    ax2.plot(times, triggers, 'r-', linewidth=1)
    ax2.set_ylabel('Trigger State')
    ax2.set_xlabel('Time (ms)')
    ax2.set_title('Trigger Signal')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
```

## 🧮 Statistical Analysis

### Summary Statistics

```python
def analyze_latencies(latencies):
    """Generate comprehensive latency statistics"""
    stats = {
        'mean': np.mean(latencies),
        'median': np.median(latencies),
        'std': np.std(latencies),
        'min': np.min(latencies),
        'max': np.max(latencies),
        'q1': np.percentile(latencies, 25),
        'q3': np.percentile(latencies, 75),
        'iqr': np.percentile(latencies, 75) - np.percentile(latencies, 25)
    }
    
    # Detect outliers (> 1.5 * IQR)
    outlier_threshold = stats['q3'] + 1.5 * stats['iqr']
    outliers = [l for l in latencies if l > outlier_threshold]
    stats['outlier_count'] = len(outliers)
    stats['outlier_percentage'] = (len(outliers) / len(latencies)) * 100
    
    return stats
```

### Drift Analysis

```python
def analyze_drift(data):
    """Analyze latency drift over time"""
    # Group latencies by time windows
    window_size = 60000  # 1 minute windows
    windows = []
    
    for i in range(0, len(data), window_size):
        window_data = data[i:i+window_size]
        window_latencies = calculate_latencies(window_data)
        if window_latencies:
            windows.append({
                'time': i // window_size,
                'mean_latency': np.mean(window_latencies),
                'std_latency': np.std(window_latencies)
            })
    
    return windows
```

## 💡 Analysis Ideas

### Idea 1: Real-time Analysis Dashboard

- Live plotting of incoming data
- Running statistics display
- Automatic anomaly detection
- Export functionality

### Idea 2: Machine Learning Integration

- Predict latency patterns
- Classify different stimulus types
- Detect hardware degradation
- Optimize experiment timing

### Idea 3: Comparative Analysis Tools

- Compare different display technologies
- Benchmark various stimulus software
- Statistical significance testing
- Generate publication-ready figures
- Nicer graphs with customizable themes
- More flexible analysis pipelines
- Compare software used (PsychoPy, E-Prime, etc.)
- Compare hardware used (CRT vs LCD vs LED monitors)
- Do additional testing with different experimental paradigms

## 📊 Advanced Visualization and Comparative Analysis

### Creating Publication-Quality Graphs

```python
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# Set publication-quality defaults
rcParams['figure.dpi'] = 300
rcParams['savefig.dpi'] = 300
rcParams['font.size'] = 12
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']

def create_comparison_plot(results_dict):
    """Create a comparison plot for different hardware/software combinations"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Hardware comparison
    hardware_data = results_dict['hardware']
    sns.boxplot(data=hardware_data, x='display_type', y='latency', ax=ax1)
    ax1.set_title('Latency by Display Technology')
    ax1.set_xlabel('Display Type')
    ax1.set_ylabel('Latency (ms)')
    
    # Software comparison
    software_data = results_dict['software']
    sns.violinplot(data=software_data, x='software', y='latency', ax=ax2)
    ax2.set_title('Latency by Stimulus Software')
    ax2.set_xlabel('Software')
    ax2.set_ylabel('Latency (ms)')
    
    plt.tight_layout()
    return fig
```

### Flexible Analysis Pipeline

```python
class LatencyAnalyzer:
    """Flexible analysis pipeline for latency data"""
    
    def __init__(self, config=None):
        self.config = config or self.default_config()
        self.results = {}
    
    def default_config(self):
        return {
            'threshold_method': 'adaptive',
            'outlier_method': 'iqr',
            'smoothing': True,
            'baseline_correction': True
        }
    
    def add_comparison(self, name, data, metadata):
        """Add a dataset for comparison"""
        self.results[name] = {
            'data': data,
            'metadata': metadata,
            'stats': self.analyze_dataset(data)
        }
    
    def analyze_dataset(self, data):
        """Comprehensive analysis of a single dataset"""
        latencies = self.calculate_latencies(data)
        return {
            'latencies': latencies,
            'summary': self.get_summary_stats(latencies),
            'drift': self.analyze_drift(data),
            'quality_metrics': self.assess_data_quality(data)
        }
    
    def compare_all(self):
        """Compare all added datasets"""
        comparison = {}
        for metric in ['mean', 'median', 'std', 'reliability']:
            comparison[metric] = {
                name: results['stats']['summary'][metric]
                for name, results in self.results.items()
            }
        return comparison
```

### Hardware Comparison Framework

```python
def compare_hardware_setups(data_files):
    """Compare latency across different hardware configurations"""
    results = {}
    
    hardware_configs = {
        'CRT': {'refresh_rate': 100, 'technology': 'cathode_ray'},
        'LCD': {'refresh_rate': 60, 'technology': 'liquid_crystal'},
        'LED': {'refresh_rate': 144, 'technology': 'led_backlit'},
        'OLED': {'refresh_rate': 120, 'technology': 'organic_led'}
    }
    
    for display_type, config in hardware_configs.items():
        if display_type in data_files:
            data = read_latency_data(data_files[display_type])
            latencies = calculate_latencies(data)
            
            results[display_type] = {
                'latencies': latencies,
                'mean': np.mean(latencies),
                'std': np.std(latencies),
                'config': config,
                'theoretical_min': 1000 / config['refresh_rate']
            }
    
    return results
```

### Software Comparison Tools

```python
def compare_stimulus_software(experiments):
    """Compare different stimulus presentation software"""
    software_comparison = {
        'PsychoPy': [],
        'E-Prime': [],
        'Presentation': [],
        'OpenSesame': [],
        'Custom': []
    }
    
    for exp_name, exp_data in experiments.items():
        software = exp_data['metadata']['software']
        latencies = calculate_latencies(exp_data['data'])
        
        software_comparison[software].extend(latencies)
    
    # Statistical comparison
    from scipy import stats
    comparison_matrix = {}
    
    for sw1 in software_comparison:
        comparison_matrix[sw1] = {}
        for sw2 in software_comparison:
            if sw1 != sw2 and software_comparison[sw1] and software_comparison[sw2]:
                stat, p_value = stats.ttest_ind(
                    software_comparison[sw1], 
                    software_comparison[sw2]
                )
                comparison_matrix[sw1][sw2] = {
                    'p_value': p_value,
                    'significant': p_value < 0.05,
                    'mean_diff': np.mean(software_comparison[sw1]) - 
                                np.mean(software_comparison[sw2])
                }
    
    return comparison_matrix
```

### Additional Testing Protocols

```python
def run_comprehensive_tests(device):
    """Run additional tests for thorough validation"""
    test_protocols = {
        'refresh_rate_test': test_refresh_rates,
        'color_dependency': test_color_effects,
        'brightness_test': test_brightness_levels,
        'position_test': test_screen_positions,
        'temporal_stability': test_long_term_stability,
        'stress_test': test_high_frequency_triggers
    }
    
    results = {}
    for test_name, test_func in test_protocols.items():
        print(f"Running {test_name}...")
        results[test_name] = test_func(device)
    
    return results

def test_refresh_rates(device):
    """Test latency at different monitor refresh rates"""
    refresh_rates = [60, 75, 120, 144, 240]
    results = {}
    
    for rate in refresh_rates:
        # Set monitor refresh rate (OS-specific)
        set_refresh_rate(rate)
        time.sleep(2)  # Allow monitor to stabilize
        
        # Collect data
        data = collect_samples(device, n_samples=100)
        latencies = calculate_latencies(data)
        
        results[rate] = {
            'mean_latency': np.mean(latencies),
            'std_latency': np.std(latencies),
            'theoretical_min': 1000 / rate
        }
    
    return results
```

## 🔗 Useful Links

### Python Libraries

- 📊 [NumPy Documentation](https://numpy.org/doc/stable/)
- 📈 [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- 🐼 [Pandas for Data Analysis](https://pandas.pydata.org/)
- 📉 [Seaborn Statistical Plots](https://seaborn.pydata.org/)

### Neuroscience Tools

- 🧠 [MNE-Python](https://mne.tools/) - EEG/MEG analysis
- 📊 [Psychopy](https://www.psychopy.org/) - Stimulus presentation
- 🔬 [EEGLAB](https://eegmanylabs.dev/) - EEG analysis toolbox

### Sample Data

- 📁 [Sample Data Files](https://drive.google.com/file/d/1CWcmZ3lSZ2r-ONvxLq3t8nrp7U5ydV-8/view?usp=sharing)

## 📝 Best Practices

### Data Collection

1. **Calibration**: Always calibrate before experiments
2. **Environment**: Control ambient light conditions
3. **Multiple Trials**: Collect sufficient data for statistics
4. **Documentation**: Record experimental conditions

### Analysis Workflow

1. **Data Validation**: Check for corrupted records
2. **Preprocessing**: Filter noise and artifacts
3. **Statistical Testing**: Use appropriate tests
4. **Visualization**: Create clear, informative plots
5. **Reproducibility**: Document analysis code
