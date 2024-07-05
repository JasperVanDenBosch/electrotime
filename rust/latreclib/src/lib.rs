//! # Latency Recorder library (latreclib)
//! 
//! Helper functions for the device firmware 

#![no_std]

use core::array::from_fn;

/// Convert an unsigned 8-bit integer to an array of 8 bools
/// 
/// # Examples
/// 
/// ```
/// let out = latreclib::num2bools(33);
/// 
/// assert_eq!(out, [true, false, false, false, false, true, false, false])
/// ````
#[must_use]
pub fn num2bools(val: u8) -> [bool; 8] {
    // big endian
    from_fn(|i| (val >> i & 1) == 1)
}

/// Convert an array of 8 bools to an unsigned 8-bit integer
/// 
/// # Examples
/// 
/// ```
/// let out = latreclib::bools2num([true, false, true, false, false, false, false, true]);
/// 
/// assert_eq!(out, 133)
/// ````
#[must_use]
pub fn bools2num(val: [bool; 8]) -> u8 {
    // big endian
    const Z: [u8; 8] = [1, 2, 4, 8, 16, 32, 64, 128];
    val.iter().enumerate().map(
        |(i, b)| {if *b { Z[i]} else {0}}
    ).sum()
}
