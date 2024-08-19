#![no_std]
#![no_main]

//use arduino_hal::prelude::*;
use panic_halt as _;
use latreclib::num2bools;

#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);
    let mut led_d12 = pins.d12.into_output();
    let mut dpins = [
        pins.d0.into_output().downgrade(),
        pins.d1.into_output().downgrade(),
        pins.d2.into_output().downgrade(),
        pins.d3.into_output().downgrade(),
        pins.d4.into_output().downgrade(),
        pins.d5.into_output().downgrade(),
        pins.d6.into_output().downgrade(),
        pins.d7.into_output().downgrade(),
    ];
    let triggers: [u8; 12] = [1, 2, 3, 4, 5, 6, 8, 16, 32, 64, 129, 255];
    const LATENCY: u16 = 20;
    const TRIG_DUR: u16 = 10;
    const STIM_DUR: u16 = 50;
    const SHORT_ITI: u16 = 800;
    const LONG_ITI: u16 = 1200;
    const STIM_DELAY: u16 = LATENCY - TRIG_DUR;

    loop {
        for t in triggers {
            let vals = num2bools(t);
            for (i, pin) in dpins.iter_mut().enumerate() {
                if vals[i] {
                    pin.set_high();
                }
            }
            arduino_hal::delay_ms(TRIG_DUR);
            for pin in dpins.iter_mut() {
                pin.set_low();
            }
            arduino_hal::delay_ms(STIM_DELAY);
            led_d12.set_high();
            arduino_hal::delay_ms(STIM_DUR);
            led_d12.set_low();

            if (t % 4) > 0 {
                arduino_hal::delay_ms(SHORT_ITI);
            }
            else {
                arduino_hal::delay_ms(LONG_ITI);
            }
        }
    }
}
