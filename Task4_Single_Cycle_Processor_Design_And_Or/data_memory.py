"""
data_memory.py - Represents the Data Memory component of a processor design.
One read port (32 bit A1, 32 bit RD),
one write enable port (WE).
Write data port WD 32 bit.
"""

import sys
import os

# Get directory from current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Goes up one level and into Task 3 folder
task3_path = os.path.join(current_dir, "..", "Task3_Memory_Hierarchy_Simulation")

# add to path
if task3_path not in sys.path:
    sys.path.insert(0, task3_path)

try:
    from memory_display_utils import MemoryDisplayUtils
    
except ImportError as e:
    print(f"Import from Task3 failed: {e}")


class DataMemory:
    """
    Data Memory component.
    Uses sparse storage (dict) so only written addresses consume space.

    Ports:
    - A (32 bits): Read/Write byte address (word-aligned)
    - WD (32 bits): Write data
    - WE (1 bit) : Write enable (1 = write, 0 = read-only)
    - RD (32 bits): Read data output
    """

    def __init__(self, size_words = 256):
        """
        Initialize data memory.

        @param size_words - capacity in 32-bit words (default 256 = 1 KB)
        """
        self.size_words = size_words
        # Sparse storage: word_address -> 32-bit value
        self.memory = {}
        self.display = MemoryDisplayUtils()

    def read(self, address):
        """
        Read 32-bit word from byte address.
        Returns 0 for unwritten addresses.

        @param address - byte address (must be word-aligned, i.e. divisible by 4)
        @return - 32-bit value at that address
        """
        # Convert byte address to word index
        word_addr = (address >> 2) & 0xFFFFFFFF
        return self.memory.get(word_addr, 0)

    def write(self, address, data, we = 1):
        """
        Write 32-bit word to byte address if write-enabled.

        @param address - byte address (word-aligned)
        @param data - 32-bit value to store
        @param we - write enable signal (1 = write, 0 = no-op)
        """
        if we == 1:
            word_addr = (address >> 2) & 0xFFFFFFFF
            self.memory[word_addr] = data & 0xFFFFFFFF

    def load_program(self, initial_data):
        """
        Pre-load values into data memory (for testing)

        @param initial_data - list of 32-bit values, loaded starting at word address 0
        """
        self.memory = {}
        for i, value in enumerate(initial_data):
            self.memory[i] = value & 0xFFFFFFFF

    def get_memory_content(self, start_word = 0, num_words = 10):
        """
        Return a slice of memory as a dict of {byte_address: value}

        @param start_word - starting word index
        @param num_words  - number of words to return
        @return - dict {byte_addr: value} for non-zero entries in range
        """
        result = {}
        for i in range(start_word, start_word + num_words):
            if i in self.memory:
                result[i * 4] = self.memory[i]
        return result

    def print_memory_content(self, num_words = 20):
        """
        Print non-zero memory contents for debugging
        Uses MemoryDisplayUtils from Task 3 for hex formatting

        @param num_words - maximum number of words to display
        """
        if not self.memory:
            print("  (data memory empty)")
            return

        shown = 0
        for word_addr in sorted(self.memory.keys()):
            if shown >= num_words:
                break
            byte_addr = word_addr * 4
            addr_str = self.display.int_to_hex(byte_addr)
            val_str  = self.display.int_to_hex(self.memory[word_addr])
            print(f"  {addr_str}: {val_str}")
            shown += 1

    def reset(self):
        """
        Clear all memory contents
        """
        self.memory = {}

    def get_stats(self):
        """
        Return memory statistics

        @return - dict with size and usage info
        """
        return {
            'size_words': self.size_words,
            'used_words': len(self.memory),
        }


# Independent file testing
if __name__ == "__main__":
    print("=" * 50)
    print("Testing DataMemory")
    print("=" * 50)

    dm = DataMemory(size_words = 64)

    print("\nWrite and read back:")
    dm.write(0x00, 0xDEADBEEF)
    dm.write(0x04, 0x12345678)
    dm.write(0x08, 0xFFFFFFFF)

    assert dm.read(0x00) == 0xDEADBEEF, "FAIL addr 0x00"
    assert dm.read(0x04) == 0x12345678, "FAIL addr 0x04"
    assert dm.read(0x08) == 0xFFFFFFFF, "FAIL addr 0x08"
    assert dm.read(0x0C) == 0,          "FAIL unwritten should be 0"
    print("  Read/write: PASS")

    print("\nWE = 0 should not write:")
    dm.write(0x10, 0xABCDABCD, we = 0)
    assert dm.read(0x10) == 0, "FAIL WE = 0 wrote anyway"
    print("  WE = 0: PASS")

    print("\nMemory content:")
    dm.print_memory_content()

    print("\nReset:")
    dm.reset()
    assert dm.read(0x00) == 0, "FAIL after reset"
    print("  Reset: PASS")

    print("\n" + "=" * 50)
    print("DataMemory Tests Complete")
    print("=" * 50)
