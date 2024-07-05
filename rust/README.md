# Firmware
One package per device.
A workspace wouldn't work as we'd like to run unit tests against the library which the avr-hal target doesn't support. A single package with two binary crates wouldn't work as the delivery tool wouldn't know which binary to deploy.
