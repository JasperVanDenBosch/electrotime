// https://carbon.now.sh/?bg=rgba%28171%2C184%2C195%2C0%29&t=a11y-dark&wt=none&l=rust&width=680&ds=true&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs=14px&lh=133%25&si=false&es=2x&wm=false&code=%2523%21%255Bno_std%255D%250Ause%2520arduino_hal%253A%253Aprelude%253A%253A*%253B%250Ause%2520latreclib%253A%253Abools2num%253B%250A%250A%2523%255Barduino_hal%253A%253Aentry%255D%250Afn%2520main%28%29%2520-%253E%2520%21%2520%257B%250A%2520%2520%2520%2520let%2520dp%2520%253D%2520arduino_hal%253A%253APeripherals%253A%253Atake%28%29.unwrap%28%29%253B%250A%2520%2520%2520%2520let%2520pins%2520%253D%2520arduino_hal%253A%253Apins%21%28dp%29%253B%250A%2520%2520%2520%2520let%2520mut%2520adc%2520%253D%2520arduino_hal%253A%253AAdc%253A%253Anew%28dp.ADC%252C%2520Default%253A%253Adefault%28%29%29%253B%250A%2520%2520%2520%2520let%2520a0%2520%253D%2520pins.a0.into_analog_input%28%2526mut%2520adc%29%253B%250A%250A%2520%2520%2520%2520dp.TC1.tccr1b.write%28%257Cw%257C%2520w.cs1%28%29.prescale_1024%28%29%29%253B%250A%250A%2520%2520%2520%2520loop%2520%257B%250A%2520%2520%2520%2520%2520%2520%2520%2520dp.TC1.tcnt1.write%28%257Cw%257C%2520%257B%2520w.bits%280%29%2520%257D%29%253B%250A%250A%2520%2520%2520%2520%2520%2520%2520%2520while%2520tval%2520%253C%252062500%2520%257B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520tval%2520%253D%2520dp.TC1.tcnt1.read%28%29.bits%28%29%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520let%2520light%2520%253D%2520a0.analog_read%28%2526mut%2520adc%29%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520let%2520trigger%253A%2520%255Bbool%253B%25208%255D%2520%253D%2520bools2num%28dpins.map%28%2520%257Cpin%257C%2520%257B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520if%2520pin.downgrade%28%29.is_high%28%29%2520%257B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520bools%255Bi%255D%2520%253D%2520true%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%257D%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%257D%29%29%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520ufmt%253A%253Auwriteln%21%28%2526mut%2520serial%252C%2520light%252C%2520trigger%29.unwrap_infallible%28%29%253B%250A%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520arduino_hal%253A%253Adelay_us%2850%29%250A%2520%2520%2520%2520%2520%2520%2520%2520%257D%250A%2520%2520%2520%2520%257D%250A%257D
#![no_std]
use arduino_hal::prelude::*;
use latreclib::bools2num;

#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();
    let pins = arduino_hal::pins!(dp);
    let mut adc = arduino_hal::Adc::new(dp.ADC, Default::default());
    let a0 = pins.a0.into_analog_input(&mut adc);

    dp.TC1.tccr1b.write(|w| w.cs1().prescale_1024());

    loop {
        dp.TC1.tcnt1.write(|w| { w.bits(0) });

        while tval < 62500 {
           tval = dp.TC1.tcnt1.read().bits();
           let light = a0.analog_read(&mut adc);
           let trigger: [bool; 8] = bools2num(dpins.map( |pin| {
               if pin.downgrade().is_high() {
                   bools[i] = true;
               }
           }));
           ufmt::uwriteln!(&mut serial, light, trigger).unwrap_infallible();
           arduino_hal::delay_us(50)
        }
    }
}
