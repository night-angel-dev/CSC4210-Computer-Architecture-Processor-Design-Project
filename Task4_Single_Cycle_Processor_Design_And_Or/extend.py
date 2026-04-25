"""
extend.py -

Extends immediate values from instruction to 32bits.
For R type insturctions immediate extension is not used

For types I, S, B, J, U immediate extension is apply differently due to each haveing different instruction encoding templates.

- Takes immediate bits from instruction
- Sign extends to 32 bits
- used by ALUSrc MUX for immediate operands
"""

import sys
import os

# Get directory from current file 
current_dir = os.path.dirname(os.path.abspath(__file__))

# Goes up one level and into Task 1 folder
task1_path = os.path.join(current_dir, "..", "Task1_Data_Systems")

# add to path
if task1_path not in sys.path:
    sys.path.insert(0, task1_path)

try:
    from binary_utils import (decimal_to_padded_binary, binary_to_decimal, mask_to_32bits)
    

except ImportError as e:
    print(f"Import from Task1 failed: {e}")


class SignExtend:
    """
    Sign extension component for immediate values.
    
    Supoorts the following
    I type - 12 bit immediate (31:20)
    S type - 12 bits imeddiate (31:25 and 11:7) logic for this can also be used for B type from the looks of it
    U type - 20 bits immediate (31:12) shifted left by 12 in order to placed in upper 20 bits of a 32 bit instruction
    """
    
    def __init__(self):
        """
        Initialize sign extend unit
        """
        self.extended_value = 0
        
    def extend_i_type(self, imm12):
        """
        Sign extend 12 bit immediate to 32 bits (I type)

        @param imm12 - 12 bit immediate value (31:20)
        @return - 32 bit sign extended value
        """
        # Get the 12 bit binary string representation
        binary_str = decimal_to_padded_binary(imm12, 12)

        # MSB (bit 11) is the sign bit: '0' = positive, '1' = negative
        sign_bit = binary_str[0]

        # Prepend 20 copies of the sign bit to reach 32 bits.
        # Positive: fills with '0's (zero extend). Negative: fills with '1's (sign extend).
        extended = sign_bit * (32 - 12) + binary_str

        # Convert binary string back to integer, then mask to 32-bit
        self.extended_value = mask_to_32bits(binary_to_decimal(extended))
        return self.extended_value

    def extend_s_type(self, imm12):
        """
        Sign extend 12 bit immediate to 32 bits (S type)

        @param imm12 - assembled 12 bit immediate (imm[11:5] from bits 31:25, imm[4:0] from bits 11:7)
        @return - 32bit sign extended value
        """
        # S type splits its immediate across two fields in the instruction word,
        # but once assembled into a single 12 bit value the sign extension is the same to I type
        binary_str = decimal_to_padded_binary(imm12, 12)

        # MSB (bit 11) is the sign bit
        sign_bit = binary_str[0]

        # Fill upper 20 bits with sign bit to reach 32 bits
        extended = sign_bit * (32 - 12) + binary_str

        self.extended_value = mask_to_32bits(binary_to_decimal(extended))
        return self.extended_value

    def extend_u_type(self, imm20):
        """
        Zero extend and shift 20 bit immedate (U Type)

        @param imm20 - 20 bit immediate value (31:12)
        @return - 32 bit value shifted left by 12
        """
        # U-type places the immediate in the upper 20 bits of the result
        # Mask to 20 bits first to discard any extra bits, then shift left by 12
        # Lower 12 bits are implicitly zeroed by the shift
        self.extended_value = mask_to_32bits((imm20 & 0xFFFFF) << 12)
        return self.extended_value

    def extend(self, imm, imm_type):
        """
        Generic extend method

        @param imm - immediate value from instruction
        @param imm_type - Type "I", "S", or "U" , in future can add on for B and J type
        """
        # ImmSrc signal from the control unit determines which format to use
        if imm_type == "I":
            return self.extend_i_type(imm)
        elif imm_type == "S":
            return self.extend_s_type(imm)
        elif imm_type == "U":
            return self.extend_u_type(imm)
        else:
            self.extended_value = 0
            return 0

    def get_extend(self):
        """
        Get the last extended value

        @return - 32 bit extended value
        """
        return self.extended_value

    def reset(self):
        """
        Reset the extend component
        """
        self.extended_value = 0

# Independent file testing
if __name__ == "__main__":
    print("=" * 60)
    print("Testing SignExtend")
    print("=" * 60)

    se = SignExtend()

    def check(label, result, expected):
        status = "PASS" if result == expected else "FAIL"
        print(f"  {label}: {hex(result)} (expected {hex(expected)}) {status}")

    print("\nI-type (12-bit sign extend):")
    check("0 -> 0x00000000",        se.extend_i_type(0),    0x00000000)
    check("1 -> 0x00000001",        se.extend_i_type(1),    0x00000001)
    check("2047 -> 0x000007FF",     se.extend_i_type(2047), 0x000007FF)
    check("2048 -> 0xFFFFF800",     se.extend_i_type(2048), 0xFFFFF800)
    check("4095 (-1) -> 0xFFFFFFFF",se.extend_i_type(4095), 0xFFFFFFFF)

    print("\nS-type (12-bit sign extend, assembled immediate):")
    check("0 -> 0x00000000",        se.extend_s_type(0),    0x00000000)
    check("4095 (-1) -> 0xFFFFFFFF",se.extend_s_type(4095), 0xFFFFFFFF)

    print("\nU-type (20-bit shift left 12):")
    check("1 -> 0x00001000",        se.extend_u_type(1),       0x00001000)
    check("0xFFFFF -> 0xFFFFF000",  se.extend_u_type(0xFFFFF), 0xFFFFF000)
    check("0 -> 0x00000000",        se.extend_u_type(0),       0x00000000)

    print("\nGeneric extend() dispatch:")
    check('extend(4095,"I")',  se.extend(4095, "I"),    0xFFFFFFFF)
    check('extend(4095,"S")',  se.extend(4095, "S"),    0xFFFFFFFF)
    check('extend(1,"U")',     se.extend(1, "U"),       0x00001000)

    print("\nget_extend() returns last value:")
    check("last value 0x00001000", se.get_extend(), 0x00001000)

    print("\nreset():")
    se.reset()
    check("after reset -> 0x00000000", se.get_extend(), 0x00000000)

    print("\n" + "=" * 60)
    print("SignExtend Tests Complete")
    print("=" * 60)
        
        
        
        
