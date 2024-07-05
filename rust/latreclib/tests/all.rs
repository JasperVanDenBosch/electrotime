use latreclib::num2bools;

#[test]
fn test_num2bools() {
    assert_eq!(num2bools(0), [false, false, false, false, false, false, false, false]);
    assert_eq!(num2bools(1), [true, false, false, false, false, false, false, false]);
    assert_eq!(num2bools(2), [false, true, false, false, false, false, false, false]);
    assert_eq!(num2bools(85), [true, false, true, false, true, false, true, false]);
    assert_eq!(num2bools(255), [true, true, true, true, true, true, true, true]);
}
