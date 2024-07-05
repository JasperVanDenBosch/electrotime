#![no_std]

use core::array::from_fn;

#[must_use]
pub fn num2bools(val: u8) -> [bool; 8] {
    // big endian
    from_fn(|i| (val >> i & 1) == 1)
}

#[must_use]
pub fn bools2num(val: [bool; 8]) -> u8 {
    // big endian
    const Z: [u8; 8] = [1, 2, 4, 8, 16, 32, 64, 128];
    val.iter().enumerate().map(
        |(i, b)| {if *b { Z[i]} else {0}}
    ).sum()
}
