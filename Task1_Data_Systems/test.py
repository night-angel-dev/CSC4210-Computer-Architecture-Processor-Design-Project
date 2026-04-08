"""
test.py - here will lie much of the unit tests required from section 2 of our tasks. This includes units tests for:

1. Positive values
2. Zero
3. Negative values
4. Boundary cases (min/max 32-bit values)

@author Armando Galvan
@version CSC4210 Computer Architecture Spring 2026

"""

from NumberSystemConverter import NumberSystemConverter

def run_all_tests():
    """Run all required tests from FR8."""
    
    converter = NumberSystemConverter()
    
    # Header
    print("\n" + "="*80)
    print("TEST SUITE - FR8 REQUIRED TESTS")
    print("="*80)
    
        
    test_cases = [
        # (input, format, expected_output, expected_overflow, expected_saturated)
        
        # FR8.1: Positive number
        ("123", "DEC", "123", 0, 0),
        ("123", "BIN", "00000000000000000000000001111011", 0, 0),
        ("123", "HEX", "0x0000007B", 0, 0),
        
        # FR8.2: Zero
        ("0", "DEC", "0", 0, 0),
        ("0", "BIN", "00000000000000000000000000000000", 0, 0),
        ("0", "HEX", "0x00000000", 0, 0),
        
        # FR8.3: Negative number
        ("-123", "DEC", "-123", 0, 0),
        ("-123", "BIN", "11111111111111111111111110000101", 0, 0),
        ("-123", "HEX", "0xFFFFFF85", 0, 0),
        
        # FR8.4: MAX_INT32
        ("2147483647", "DEC", "2147483647", 0, 0),
        ("2147483647", "BIN", "01111111111111111111111111111111", 0, 0),
        ("2147483647", "HEX", "0x7FFFFFFF", 0, 0),
        
        # FR8.4: MIN_INT32
        ("-2147483648", "DEC", "-2147483648", 0, 0),
        ("-2147483648", "BIN", "10000000000000000000000000000000", 0, 0),
        ("-2147483648", "HEX", "0x80000000", 0, 0),
        
        # FR8.5: Overflow - MAX_INT32 + 1
        # Should saturate to MAX
        ("2147483648", "DEC", "2147483647", 1, 1),
        ("2147483648", "BIN", "01111111111111111111111111111111", 1, 1),
        ("2147483648", "HEX", "0x7FFFFFFF", 1, 1),
        
        # FR8.5: Overflow - MIN_INT32 - 1
        # Should saturate to MIN
        ("-2147483649", "DEC", "-2147483648", 1, 1),
        ("-2147483649", "BIN", "10000000000000000000000000000000", 1, 1),
        ("-2147483649", "HEX", "0x80000000", 1, 1),
    ]
    
    
    passed = 0
    total = len(test_cases)
    
    print("Let 0 = False and 1 = True")
    
    # Loop through test cases
    for i, (input, format, expected, expected_overflow_flag, expected_saturation_flag) in enumerate(test_cases, 1):
        
        # Attempt
        try:
            result, overflow, saturated = converter.convert(input, format)
            
            if result == expected and overflow == expected_overflow_flag and saturated == expected_saturation_flag:
                status = "PASS"
                passed += 1
                
            else:
                status = "FAIL"
            
            print(f"{status} Test {i:2d}: {input:12} ({format:3}) -> {result:35} | overflow status flag = {overflow} saturated status flag = {saturated}")
            
            if status == "FAIL":
                print(f"Expected: {expected:35} | overflow status flag = {expected_overflow_flag} saturated status flag = {expected_saturation_flag}")
        
        # Error met        
        except Exception as e:
            print(f"ERROR Test {i:2d}: {input} ({format}) - {e}")
    
    
    # Results Header
    print("-" * 80)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nALL TESTS PASSED!")
        return True
    
    else:
        print("\nSome tests failed. Review failures above.")
        return False


# Run tests
if __name__ == "__main__":
    print("\n" + "="*80)
    print("TESTING NumberSystemConverter")
    print("="*80)
    
    run_all_tests()
    
    pass