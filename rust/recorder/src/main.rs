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

    let mut dpins = [
        pins.d2.downgrade(),
        pins.d3.downgrade(),
        pins.d4.downgrade(),
        pins.d5.downgrade(),
        pins.d6.downgrade(),
        pins.d7.downgrade(),
        pins.d8.downgrade(),
        pins.d9.downgrade(),
    ];

    // what is limiting factor? ADC? Serial?
    loop {
        let v = a0.analog_read(&mut adc);
        //let a = v.to_be_bytes();

        let mut bools: [bool; 8] = [false, false, false, false, false, false, false, false];
        for (i, pin) in dpins.iter_mut().enumerate() {
            if pin.is_high() {
                bools[i] = true;
            }
        }
        let num = bools2num(bools);

        // or .write_byte(byte:u8)
        ufmt::uwriteln!(&mut serial, "{} {}", v, num).unwrap_infallible();
        arduino_hal::delay_ms(200);
    }
}

fn bools2num(val: [bool; 8]) -> u8 {
    // big endian
    match val {
        [false, false, false, false, false, false, false, false] => 0,
        [true, false, false, false, false, false, false, false] => 1,
        [false, true, false, false, false, false, false, false] => 2,
        _ => 0,
    }
}
