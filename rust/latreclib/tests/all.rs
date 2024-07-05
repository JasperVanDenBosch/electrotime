use latreclib::num2bools;
use latreclib::bools2num;

#[test]
fn test_num2bools() {
    assert_eq!(num2bools(0), [false, false, false, false, false, false, false, false]);
    assert_eq!(num2bools(1), [true, false, false, false, false, false, false, false]);
    assert_eq!(num2bools(2), [false, true, false, false, false, false, false, false]);
    assert_eq!(num2bools(85), [true, false, true, false, true, false, true, false]);
    assert_eq!(num2bools(255), [true, true, true, true, true, true, true, true]);
}

#[test]
fn test_bools2num() {
    assert_eq!(bools2num([false, false, false, false, false, false, false, false]), 0);
    assert_eq!(bools2num([true, false, false, false, false, false, false, false]), 1);
    assert_eq!(bools2num([false, true, false, false, false, false, false, false]), 2);
    assert_eq!(bools2num([true, false, true, false, true, false, true, false]), 85);
    assert_eq!(bools2num([true, true, true, true, true, true, true, true]), 255);
}
