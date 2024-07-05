#![no_std]

use core::array::from_fn;

#[must_use]
pub fn num2bools(val: u8) -> [bool; 8] {
    // big endian
    from_fn(|i| (val >> i & 1) == 1)
}
