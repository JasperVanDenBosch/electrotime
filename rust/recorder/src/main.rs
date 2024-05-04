#![no_std]
#![no_main]

use arduino_hal::prelude::*;
use panic_halt as _;

#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);
    let mut serial = arduino_hal::default_serial!(dp, pins, 115200);
    let mut adc = arduino_hal::Adc::new(dp.ADC, Default::default());
    let a0 = pins.a0.into_analog_input(&mut adc);
    ufmt::uwriteln!(&mut serial, "Hello from Arduino!").unwrap();

    loop {
        let v = a0.analog_read(&mut adc);
        ufmt::uwriteln!(&mut serial, "{}", v).unwrap_infallible();
        arduino_hal::delay_ms(500);
    }
}
