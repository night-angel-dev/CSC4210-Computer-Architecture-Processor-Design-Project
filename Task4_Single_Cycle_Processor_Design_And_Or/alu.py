"""
alu.py - Should accept SrcA (from Reg file RD1), SrcB (from Reg file RD2) after going through mux to see if there is a signImm.

ALU with operation selection and inversion flag. ALUControl is inputted for operation being done.

Outputs ALUResult, which connects to (Read port A 32 bit of Data Memory component and MemtoReg MUX. 

Should support AND and OR operations with input inversion for NOT functionaility.

"""

# Import inversion methods from task a

import sys
import os

# Get the directory of current file 
current_dir = os.path.dirname(os.path.abspath(__file__))

# Goes up one level and into Task 1 folder
task1_path = os.path.join(current_dir, "..", "Task1_Data_Systems")

# Add to path
if task1_path not in sys.path:
    sys.path.insert(0, task1_path)

try:
    from binary_utils import (decimal_to_padded_binary, invert_bits, binary_to_decimal, binary_to_hexadecimal, mask_to_32bits, mask_binary_string, mask_hex_string)
    # print("Import is a success")
    
except ImportError as e:
    print(f"Import from Task3 failed: {e}")
    

class ALU:
    """
    ALU with operations and inversion flags
    
    Operations:
    - AND: result = SrcA & SrcB
    - OR: result = SrcA | SrcB
    
    Inversion flags:
    - Invert_a: if true, apply NOT to SrcA before operation
    - Invert_b: if true, apply NOT to SrcB before operation
    
    For NOT C, set invert_a = 1, operation = AND, SrcA = C, SrcB = D for C'*D
    """
    
    def __init__(self):
        """
        Initialize ALU
        """
        self.result = 0
        self.zero = False
    
    
    
    def operate(self, src_a, src_b, alu_op, invert_a = False, invert_b = False):
        """
        Perform ALU Operation with optional input inversion
        
        @param src_a - 32 bit input A from register RD1 RF
        @param src_b - 32 bit input B from RF Register RD2 or immediate
        @param alu_op - Operation ("AND" or "OR"), add more in future if needed
        @param invert_a - If true, invert src_a before operation
        @param invert_b - if True, invert src_b before operation
        """
        
        # First mask inputs to 32 bits
        src_a = mask_to_32bits(src_a)
        src_b = mask_to_32bits(src_b)
        
        # Apply inversion using binary_utils functions if signal true
        if invert_a:
            # Convert to binary string
            binary_a = decimal_to_padded_binary(src_a, 32)
            # invert bits
            inverted_binary = invert_bits(binary_a)
            # Convert back to integer and mask
            src_a = binary_to_decimal(inverted_binary)
            src_a = mask_to_32bits(src_a)
            
        
        if invert_b:
            binary_b = decimal_to_padded_binary(src_b, 32)
            inverted_binary = invert_bits(binary_b)
            
            src_b = binary_to_decimal(inverted_binary)
            src_b = mask_to_32bits(src_b)
            
            
        # Perform operation
        if alu_op == "AND":
            self.result = src_a & src_b
        elif alu_op == "OR":
            self.result = src_a | src_b
        elif alu_op == "XOR":
            # Used by XORI with imm=-1 (0xFFFFFFFF) to compute bitwise NOT
            self.result = src_a ^ src_b
        else:
            self.result = 0
            
        # Mask rezult to 32 bits
        self.result = mask_to_32bits(self.result)
            
        # Set zero flag is result is 0
        self.zero = (self.result == 0)
        
        return self.result
    
    
    def get_result(self):
        """
        Get last ALU result. 
        
        @return - 32 bit result
        """
        
        return self.result
    
    
    def get_zero_flag(self):
        """
        Get the zero flag from the last operation.
        
        @return - True if last result was 0, False otherwise
        """
        
        return self.zero
    
    
    def reset(self):
        """
        Reset ALU Stats
        """
        
        self.result = 0
        self.zero = False


# Independent file testing
if __name__ == "__main__":
    print("=" * 60)
    print("Testing ALU with AND, OR, and Inversion")
    print("=" * 60)
    
    alu = ALU()
    
    # Helper function for clean output
    def print_result(op_name, src_a, src_b, result, expected):
        print(f"  {op_name}:")
        print(f"    src_a: {bin(src_a)} ({src_a})")
        print(f"    src_b: {bin(src_b)} ({src_b})")
        print(f"    result: {bin(result)} ({result})")
        print(f"    expected: {bin(expected)} ({expected})")
        if result == expected:
            print("    PASS")
        else:
            print("    FAIL")
    
    # Test 1: Basic AND
    print("\nTest 1: Basic AND")
    src_a = 0b11011
    src_b = 0b10000
    result = alu.operate(src_a, src_b, "AND", False, False)
    print_result("AND", src_a, src_b, result, 0b10000)
    
    # Test 2: Basic OR
    print("\nTest 2: Basic OR")
    src_a = 0b11011
    src_b = 0b10000
    result = alu.operate(src_a, src_b, "OR", False, False)
    print_result("OR", src_a, src_b, result, 0b11011)
    
    # Test 3: AND with invert_a (NOT A AND B)
    print("\nTest 3: AND with invert_a (NOT A AND B)")
    src_a = 0b11011
    src_b = 0b11111
    result = alu.operate(src_a, src_b, "AND", True, False)
    # NOT A = 0b00100 in lower 5 bits
    print_result("AND with invert_a", src_a, src_b, result, 0b00100)
    
    # Test 4: OR with invert_b (A OR NOT B) 
    print("\nTest 4: OR with invert_b (A OR NOT B)")
    src_a = 0b10101  # 21
    src_b = 0b11000  # 24
    result = alu.operate(src_a, src_b, "OR", False, True)
    # For 32-bit: NOT B = 0xFFFFFFE7, OR with 0x15 = 0xFFFFFFF7
    expected = 0xFFFFFFF7 # correct 32-bit result
    print(f"  OR with invert_b:")
    print(f"    src_a: {bin(src_a)} ({src_a})")
    print(f"    src_b: {bin(src_b)} ({src_b})")
    print(f"    result: {hex(result)} ({result})")
    print(f"    expected: {hex(expected)} ({expected})")
    if result == expected:
        print("    PASS")
    else:
        print("    FAIL")
    
    # Test 5: Both inversions (NOT A AND NOT B) = NOR 
    print("\nTest 5: Both inversions (NOT A AND NOT B) = NOR")
    src_a = 0b11011  # 27
    src_b = 0b10101  # 21
    result = alu.operate(src_a, src_b, "AND", True, True)
    # For 32-bit: NOT A = 0xFFFFFFE4, NOT B = 0xFFFFFFEA, AND = 0xFFFFFFE0
    expected = 0xFFFFFFE0  # correct 32-bit result
    print(f"  AND with both inversions:")
    print(f"    src_a: {bin(src_a)} ({src_a})")
    print(f"    src_b: {bin(src_b)} ({src_b})")
    print(f"    result: {hex(result)} ({result})")
    print(f"    expected: {hex(expected)} ({expected})")
    
    if result == expected:
        print("    PASS")
    else:
        print("    FAIL")
    
    # Test 6: Zero flag test
    print("\nTest 6: Zero flag test")
    src_a = 0b10101
    src_b = 0b01010
    result = alu.operate(src_a, src_b, "AND", False, False)
    print(f"  {bin(src_a)} AND {bin(src_b)} = {bin(result)}")
    print(f"  Zero flag: {alu.get_zero_flag()}")
    if alu.get_zero_flag():
        print("  PASS")
    else:
        print("  FAIL")
    
    # Test 7: 32-bit hex values
    print("\nTest 7: 32-bit hex values")
    src_a = 0x12345678
    src_b = 0x00FF00FF
    result = alu.operate(src_a, src_b, "AND", False, False)
    expected = 0x00340078
    print(f"  {hex(src_a)} AND {hex(src_b)}")
    print(f"  Result: {hex(result)}")
    print(f"  Expected: {hex(expected)}")
    if result == expected:
        print("  PASS")
    else:
        print("  FAIL")
    
    # Test 8: Using mask_hex_string for display
    print("\nTest 8: Using mask_hex_string for clean output")
    src_a = 0x12345678
    src_b = 0x00FF00FF
    result = alu.operate(src_a, src_b, "AND", False, False)
    print(f"  Result before masked as hex: {hex(result)}")
    print(f"  Result as hex: {mask_hex_string(hex(result))}")
    
    print("\n" + "=" * 60)
    print("ALU Tests Complete")
    print("=" * 60)