"""
test.py - Tests for the single-cycle processor.

Runs the full processor pipeline against all 16 boolean input combinations
for Y = A*B + C'*D, then a handful of 32-bit integer cases.
Each result is verified against the Python reference formula.
"""

import sys
import os
import contextlib

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from main import SingleCycleProcessor


def expected(A, B, C, D):
    """
    Reference formula: Y = (A AND B) OR (NOT C AND D), 32-bit unsigned.
    """
    return ((A & B) | ((~C & 0xFFFFFFFF) & D)) & 0xFFFFFFFF


def run_test(A, B, C, D):
    """
    Run one processor simulation and return (result, passed, expected).
    """
    proc = SingleCycleProcessor(A = A, B = B, C = C, D = D)
    # Suppress simulation trace so only test results are printed
    with open(os.devnull, "w") as null, contextlib.redirect_stdout(null):
        proc.run(verbose = False)
    result = proc.get_final_result()
    exp = expected(A, B, C, D)
    return result, result == exp, exp


def print_result(label, result, exp, passed):
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {label:30s}  Y = 0x{result:08X}  (expected 0x{exp:08X})")


# Boolean truth table (all 16 combinations) 

def test_boolean_inputs():
    print("=" * 65)
    print("Boolean truth table  (A,B,C,D in {0,1}, 16 combinations)")
    print("=" * 65)

    passed = 0
    failed = 0

    for A in range(2):
        for B in range(2):
            for C in range(2):
                for D in range(2):
                    result, ok, exp = run_test(A, B, C, D)
                    label = f"A = {A}, B = {B}, C = {C}, D = {D}"
                    print_result(label, result, exp, ok)
                    if ok:
                        passed += 1
                    else:
                        failed += 1

    print(f"\n  {passed}/16 passed, {failed} failed")
    return failed == 0


# 32-bit integer inputs

def test_32bit_inputs():
    print("\n" + "=" * 65)
    print("32-bit integer inputs")
    print("=" * 65)

    cases = [
        # (label,          A,           B,           C,           D)
        ("all zeros",      0x00000000,  0x00000000,  0x00000000,  0x00000000),
        ("all ones",       0xFFFFFFFF,  0xFFFFFFFF,  0xFFFFFFFF,  0xFFFFFFFF),
        ("A = B = 0xFF",       0x000000FF,  0x000000FF,  0x00000000,  0xFFFFFFFF),
        ("alternating",    0xAAAAAAAA,  0x55555555,  0xAAAAAAAA,  0x55555555),
        ("C masks all D",  0xFFFFFFFF,  0xFFFFFFFF,  0xFFFFFFFF,  0x12345678),
        ("mixed nibbles",  0x0F0F0F0F,  0xF0F0F0F0,  0x0F0F0F0F,  0xF0F0F0F0)
        ]

    passed = 0
    failed = 0

    for label, A, B, C, D in cases:
        result, ok, exp = run_test(A, B, C, D)
        print_result(label, result, exp, ok)
        if ok:
            passed += 1
        else:
            failed += 1

    total = len(cases)
    print(f"\n  {passed}/{total} passed, {failed} failed")
    return failed == 0


# Run Tests

if __name__ == "__main__":
    bool_ok = test_boolean_inputs()
    int_ok = test_32bit_inputs()

    print("\n" + "=" * 65)
    if bool_ok and int_ok:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
    print("=" * 65)
