#![no_std]
#![no_main]

use arduino_hal::prelude::*;
use panic_halt as _;

#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);
    let mut led_d12 = pins.d12.into_output();
    let mut dpins = [
        pins.d2.into_output().downgrade(),
        pins.d3.into_output().downgrade(),
        pins.d4.into_output().downgrade(),
        pins.d5.into_output().downgrade(),
        pins.d6.into_output().downgrade(),
        pins.d7.into_output().downgrade(),
        pins.d8.into_output().downgrade(),
        pins.d9.into_output().downgrade(),
    ];
    let triggers: [u8; 11] = [1, 2, 3, 4, 5, 6, 8, 16, 32, 64, 255];


    loop {
        //let v = a0.analog_read(&mut adc);
        //ufmt::uwriteln!(&mut serial, "{}", v).unwrap_infallible();
        
        for t in triggers {
            
            led_d12.set_high();
            let vals = num2bools(t);
            for (i, pin) in dpins.iter_mut().enumerate() {
                if vals[i] {
                    pin.set_high();
                }
            }

            // after 200ms, turn everything off
            arduino_hal::delay_ms(200);
            led_d12.set_low();
            for pin in dpins.iter_mut() {
                pin.set_low();
            }

            // now wait before next trial
            arduino_hal::delay_ms(2000);
        }
    }
}

fn num2bools(val: u8) -> [bool; 8] {
    // big endian
    match val {
        0 => [false, false, false, false, false, false, false, false],
        1 => [true, false, false, false, false, false, false, false],
        2 => [false, true, false, false, false, false, false, false],
        _ => [false, false, false, false, false, false, false, false],
    }
}
