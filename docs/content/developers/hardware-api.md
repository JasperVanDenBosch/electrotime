+++
Title = "Hardware API Reference"
Description = "Auto-generated API documentation for the firmware components"
SequenceNumber = 3
+++

# Hardware API Reference

This section contains auto-generated API documentation for the firmware components.

## Components

### latreclib
Core library providing helper functions and abstractions for the latency recorder.

[View Documentation →](/api/firmware/latreclib/index.html)

### recorder
Main firmware application that runs on the Arduino hardware.

[View Documentation →](/api/firmware/recorder/index.html)

### simulator
Hardware simulator for testing without physical Arduino.

[View Documentation →](/api/firmware/simulator/index.html)

## Building Documentation Locally

To regenerate the documentation:

```bash
cd firmware/latreclib
cargo doc --no-deps --open
```

