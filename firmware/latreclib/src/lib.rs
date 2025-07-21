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
#[inline(always)]  // Force inlining for performance
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
#[inline(always)]  // Force inlining for performance
pub fn bools2num(val: [bool; 8]) -> u8 {
    // Optimized version using direct bit manipulation
    // This avoids iterator overhead and is much faster
    (val[0] as u8) |
    ((val[1] as u8) << 1) |
    ((val[2] as u8) << 2) |
    ((val[3] as u8) << 3) |
    ((val[4] as u8) << 4) |
    ((val[5] as u8) << 5) |
    ((val[6] as u8) << 6) |
    ((val[7] as u8) << 7)
}

/// Fast integer to ASCII conversion without allocation
/// Optimized for small numbers common in ADC readings (0-1023)
/// 
/// Based on optimization techniques from Rust performance discussions on the adruino website
#[must_use]
#[inline(always)]
pub fn fast_u16_to_ascii(mut val: u16, buffer: &mut [u8; 5]) -> usize {
    // Handle zero case
    if val == 0 {
        buffer[0] = b'0';
        return 1;
    }
    
    // Convert digits in reverse order (faster than division)
    let mut pos = 0;
    while val > 0 {
        buffer[pos] = b'0' + (val % 10) as u8;
        val /= 10;
        pos += 1;
    }
    
    // Reverse the digits in place
    let len = pos;
    for i in 0..len/2 {
        buffer.swap(i, len - 1 - i);
    }
    
    len
}

/// Fast u8 to ASCII conversion 
#[must_use]
#[inline(always)]
pub fn fast_u8_to_ascii(mut val: u8, buffer: &mut [u8; 3]) -> usize {
    if val == 0 {
        buffer[0] = b'0';
        return 1;
    }
    
    let mut pos = 0;
    while val > 0 {
        buffer[pos] = b'0' + (val % 10);
        val /= 10;
        pos += 1;
    }
    
    let len = pos;
    for i in 0..len/2 {
        buffer.swap(i, len - 1 - i);
    }
    
    len
}
