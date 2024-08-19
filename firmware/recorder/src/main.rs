#![no_std]
#![no_main]

use arduino_hal::prelude::*;
use panic_halt as _;
use latreclib::bools2num;

#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);
    let mut serial = arduino_hal::default_serial!(dp, pins, 115200);
    let mut adc = arduino_hal::Adc::new(dp.ADC, Default::default());
    let a0 = pins.a0.into_analog_input(&mut adc);

    let mut epoch_counter = 0;

    // 15625Hz, or 64us / timepoint.
    // max val is 2ˆ16 = 65536 = 4.19s
    // safer to stop earlier, e.g 62500 = 4s
    const STOP_VAL: u16 = 62500;
    let timer1 = dp.TC1;
    timer1.tccr1b.write(|w| w.cs1().prescale_1024());

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

    loop {
        // reset timer
        ufmt::uwriteln!(&mut serial, "reset {}", epoch_counter).unwrap_infallible();
        timer1.tcnt1.write(|w| { w.bits(0) });

        let mut tval =0;
        while tval < STOP_VAL { // can do loop better
           tval = timer1.tcnt1.read().bits();

           let light = a0.analog_read(&mut adc);

           let mut bools: [bool; 8] = [false, false, false, false, false, false, false, false];
           for (i, pin) in dpins.iter_mut().enumerate() {
               if pin.is_high() {
                   bools[i] = true;
               }
           }
           let trigger = bools2num(bools);
   
           // or .write_byte(byte:u8)
           ufmt::uwriteln!(&mut serial, "{} {} {}", light, trigger, tval).unwrap_infallible();
           arduino_hal::delay_us(100)
        }
        epoch_counter += 1;
         
    }
}
