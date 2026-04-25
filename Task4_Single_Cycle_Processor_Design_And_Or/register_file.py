"""
register_file.py - Two read ports(5 bits A1, 5 bits A2, 32 bits RD1, 32 bitsRD2), one write port WD3 32 bits, 
write enabled port WE3, destination port (where data is being written to) A3 5bits. CLK port included.



"""

# Import for clock and MemoryDisplayUtils from task 3

import sys
import os

# Get the directory of current file 
current_dir = os.path.dirname(os.path.abspath(__file__))

# Goes up one level and into Task 3 folder
task3_path = os.path.join(current_dir, "..", "Task3_Memory_Hierarchy_Simulation")

# Add to path
if task3_path not in sys.path:
    sys.path.insert(0, task3_path)

try:
    from clock import Clock
    from memory_display_utils import MemoryDisplayUtils
    # print("Import is a success")
    
except ImportError as e:
    print(f"Import from Task3 failed: {e}")
    



class RegisterFile:
    """
    32X32 bit register file. 
    
    Ports:
    - A1 (5bits): Read address 1
    - A2 (5 bits): Read address 2
    - RD1 (32 bits): Read date 1 output
    - RD2 (32 bits): Read data 2 output
    - A3 (5 bits): Write address
    - WD3 (32 bits): write data
    - WE3 (1 bit): Write enable signal
    - CLK: Clock signal
    """
    
    def __init__(self):
        """
        Initialise 32 registers, set to 0
        """
        self.registers = [0] * 32
        self.clock = Clock()
        self.display = MemoryDisplayUtils()
        
        
        pass
    
    
    def read(self, a1, a2):
        """
        Read from two reigsters.
        
        @param a1 - 5 bit register address for RD1
        @param a2 - 5 bit register address for RD2
        @return - Tuple (rd1, rd2) containing 32 bit values
        """
        
        # Register x0 is reserved for 0 and should always return 0
        
        # Set rd values
        if a1 == 0:
            rd1 = 0
        else:
            rd1 = self.registers[a1]
            
        if a2 == 0:
            rd2 = 0
            
        else:
            rd2 = self.registers[a2]
            
        return rd1, rd2
    
    def write(self, a3, wd3, we3):
        """
        Write to register on clock edge if enabled
        
        @param a3 - 5 bit register address
        @param wd3 - 32 bit data to write
        @param we3 - write enabled (1 write, 0 no write)
        """
        
        # only write if enabled and not write to register x0
        if we3 == 1 and a3 != 0:
            hex_masked = self.display.int_to_hex(wd3)
            masked_value = self.display.hex_to_int(hex_masked)
            self.registers[a3] = masked_value
            
    def get_register(self, addr):
        """
        Get value of a specific register (for debugging)
        
        @param addr - Register address
        @return - 32 bit value
        """ 
        if addr == 0:
            return 0
        
        return self.registers[addr]
    
    
    def set_register(self, addr, value):
        """
        Set a register directly for testing
        
        @param addr - Register address
        @param value - 32 bit value to set
        """
        if addr != 0:
            hex_masked = self.display.int_to_hex(value)
            masked_value = self.display.hex_to_int(hex_masked)
            self.registers[addr] = masked_value
            
         
        
    
    def dump_registers(self):
        """
        Print all non-zero registers for testing/debugging
        
        @return dictionary of register values
        """
        result = {}
        
        for i in range(32):
            if self.registers[i] != 0:
                result[f"x{i}"] = self.registers[i]
                
        return result

    def reset(self):
        """
        Reset all registers to 0
        """
        self.registers = [0] * 32
        self.clock.reset()
        
    def get_stats(self):
        """
        Get register file stats
        
        @return - dictionary with stats
        """
        non_zero = sum(1 for r in self.registers if r != 0)
        return {
        'total_registers': 32,
        'non_zero_registers': non_zero,
        'clock_cycle': self.clock.get_current_cycle()
    }

# Testing independently
if __name__ == "__main__":
    print("=" * 50)
    print("Testing Register File")
    print("=" * 50)
    
    rf = RegisterFile()

    # Test 1: Value larger than 32 bits
    print("\nTest 1: Writing 33-bit value (0x1FFFFFFFF)")
    rf.write(5, 0x1FFFFFFFF, 1)
    result = rf.get_register(5)
    print(f"  Expected: 0xFFFFFFFF")
    print(f"  Got:      0x{result:X}")
    if result == 0xFFFFFFFF:
        print("  PASS: Masking works!")
    else:
        print(f"  FAIL: Masking not working - got 0x{result:X}")

    # Test 2: Check for values exceeding 32 bits
    print("\nTest 2: Checking 32-bit bound")
    if result > 0xFFFFFFFF:
        print(f"  FAIL: Register contains {result} which exceeds 32 bits!")
    else:
        print(f"  PASS: Value within 32-bit range")

    # Test 3: Write and read with no masking needed
    print("\nTest 3: Writing 32-bit value (0x12345678)")
    rf.write(6, 0x12345678, 1)
    result = rf.get_register(6)
    print(f"  Expected: 0x12345678")
    print(f"  Got:      0x{result:X}")
    if result == 0x12345678:
        print("  PASS: Value unchanged")
    else:
        print("  FAIL: Value changed")

    # Test 4: Small value
    print("\nTest 4: Writing small value (0xFF)")
    rf.write(7, 0xFF, 1)
    result = rf.get_register(7)
    print(f"  Expected: 0xFF")
    print(f"  Got:      0x{result:X}")
    if result == 0xFF:
        print("  PASS: Small value preserved")
    else:
        print("  FAIL: Small value changed")

    # Test 5: Maximum 32-bit value
    print("\nTest 5: Writing max 32-bit value (0xFFFFFFFF)")
    rf.write(8, 0xFFFFFFFF, 1)
    result = rf.get_register(8)
    print(f"  Expected: 0xFFFFFFFF")
    print(f"  Got:      0x{result:X}")
    if result == 0xFFFFFFFF:
        print("  PASS: Max value stored")
    else:
        print("  FAIL: Max value not stored")
        
        
    # Test 6: x0 is read-only
    print("\nTest 6: x0 is read-only")
    rf.write(0, 0xFFFFFFFF, 1) # Try to write to x0
    rd1, _ = rf.read(0, 0)
    print(f"x0 = {rd1} (should be 0)")
    
    
    # Test 7: multiple registers
    print("\nTest 7: multiple registers")
    test_values = [
        (2, 0xAAAAAAAA),
        (3, 0x55555555),
        (4, 0x12345678),
        (5, 0x87654321)
    ]
    
    for addr, value in test_values:
        rf.write(addr, value, 1)
    
    for addr, _ in test_values:
        rd1, _ = rf.read(addr, 0)
        print(f"x{addr} = 0x{rd1:X}")
    
    
    # Test 8: register dump
    print("\nTest 8: register dump")
    dump = rf.dump_registers()
    for name, value in dump.items():
        print(f"  {name} = 0x{value:X}")
    
    
    # Test 9: reset
    print("\nTest 9: reset")
    rf.reset()
    rd1, _ = rf.read(1, 0)
    print(f"After reset, x1 = {rd1}")
    
    # Test 10: statistics
    print("\nTest 10: statistics")
    stats = rf.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
