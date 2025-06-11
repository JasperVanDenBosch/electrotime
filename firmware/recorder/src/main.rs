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

    let dpins = [
        pins.d2.downgrade(),
        pins.d3.downgrade(),
        pins.d4.downgrade(),
        pins.d5.downgrade(),
        pins.d6.downgrade(),
        pins.d7.downgrade(),
        pins.d8.downgrade(),
        pins.d9.downgrade(),
    ];

    // Optimization: Buffer for batch output to reduce serial overhead
    const BUFFER_SIZE: usize = 16;  // Buffer 16 measurements before output
    let mut light_buffer: [u16; BUFFER_SIZE] = [0; BUFFER_SIZE];
    let mut trigger_buffer: [u8; BUFFER_SIZE] = [0; BUFFER_SIZE];
    let mut time_buffer: [u16; BUFFER_SIZE] = [0; BUFFER_SIZE];

    loop {
        // reset timer
        ufmt::uwriteln!(&mut serial, "reset {}", epoch_counter).unwrap_infallible();
        timer1.tcnt1.write(|w| { w.bits(0) });

        // Pre-allocate variables outside the tight loop for better performance
        let mut tval = 0u16;
        let mut bools: [bool; 8] = [false; 8];
        let mut buffer_count = 0usize;  // Initialize buffer counter here where it's used
        
        while tval < STOP_VAL {
            // Read timer first for most accurate timing
           tval = timer1.tcnt1.read().bits();

            // Read analog input (photodiode)
           let light = a0.analog_read(&mut adc);

            // Optimized digital pin reading - avoid iterator overhead
            // Reading pins directly for maximum speed
            bools[0] = dpins[0].is_high();
            bools[1] = dpins[1].is_high();
            bools[2] = dpins[2].is_high();
            bools[3] = dpins[3].is_high();
            bools[4] = dpins[4].is_high();
            bools[5] = dpins[5].is_high();
            bools[6] = dpins[6].is_high();
            bools[7] = dpins[7].is_high();
            
           let trigger = bools2num(bools);
   
            // Optimization: Buffer data instead of immediate output
            light_buffer[buffer_count] = light;
            trigger_buffer[buffer_count] = trigger;
            time_buffer[buffer_count] = tval;
            buffer_count += 1;

            // Output buffered data when buffer is full or at end of epoch
            if buffer_count >= BUFFER_SIZE || tval + 64 >= STOP_VAL {
                for i in 0..buffer_count {
                    ufmt::uwriteln!(&mut serial, "{} {} {}", 
                                   light_buffer[i], trigger_buffer[i], time_buffer[i])
                                   .unwrap_infallible();
                }
                buffer_count = 0;  // Reset buffer
            }
            
            // Reduced delay for higher sampling rate - but maintain stability
            arduino_hal::delay_us(50);  // Reduced from 100us to 50us
        }

        // Output any remaining buffered data
        if buffer_count > 0 {
            for i in 0..buffer_count {
                ufmt::uwriteln!(&mut serial, "{} {} {}", 
                               light_buffer[i], trigger_buffer[i], time_buffer[i])
                               .unwrap_infallible();
            }
        }

        epoch_counter += 1;
    }
}
