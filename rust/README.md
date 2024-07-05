# Firmware
One package per device. Open IDE on the level of the package, as rust-analyzer etc currently do not support monorepo or deep packages such as this structure. Same goes for terminal cargo commands.

A workspace wouldn't work as we'd like to run unit tests against the library which the avr-hal target doesn't support. A single package with two binary crates wouldn't work as the delivery tool wouldn't know which binary to deploy.

Deploy: `cargo run`
Lint: `cargo clippy -- -W clippy::pedantic`


