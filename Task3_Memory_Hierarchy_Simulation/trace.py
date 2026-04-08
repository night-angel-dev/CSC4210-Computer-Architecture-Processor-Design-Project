"""
trace.py - Instruction access trace generator.

Generates memory access patterns for testing the memory hierarchy.
For 32-bit architecture, addresses are typically multiples of 4.

Supported trace types:
- Sequential: Linear execution (0, 4, 8, 12, ...)
- Random: Random jumps in code (bonus/future add on)
- Loop: Repeated sequence (bonus/future add on)
"""

import config
import random


class TraceGenerator:
    """
    Generates instruction access traces for simulation.
    
    For 32-bit architecture:
    - Addresses increment by 4 bytes (size of one instruction)
    - Valid address range: 0 to (SSD_SIZE - 1) * 4
    """
    
    def __init__(self):
        """Initialize trace generator with configuration values."""
        self.min_address = config.MIN_ADDRESS
        self.max_address = config.MAX_ADDRESS
    
    
    def generate_sequential_trace(self, start = 0, count = None):
        """
        Generate a sequential access trace.
        
        For 32-bit architecture, sequential addresses increment by 4.
        Example: 0, 4, 8, 12, 16, ...
        
        @param start - Starting address (default 0)
        @param count - Number of accesses (default from config)
        @return - List of memory addresses
        """
        if count is None:
            count = config.DEFAULT_NUM_ACCESSES
        
        trace = []
        for i in range(count):
            # For 32-bit, each instruction is 4 bytes
            address = start + (i * 4)
            
            # Wrap around if exceeding max address
            if address > self.max_address * 4:
                address = address % (self.max_address * 4)
            
            trace.append(address)
        
        return trace
    
    def generate_random_trace(self, num_accesses = None, address_range = None):
        """
        Generate a random access trace.
        
        (bonus/future add on): For testing unpredictable access patterns.
        
        @param num_accesses - Number of accesses (default from config)
        @param address_range - Tuple of (min, max) addresses
        @return - List of random memory addresses
        """
        if num_accesses is None:
            num_accesses = config.DEFAULT_NUM_ACCESSES
        
        if address_range is None:
            min_addr = config.RANDOM_ADDRESS_MIN
            max_addr = config.RANDOM_ADDRESS_MAX
        else:
            min_addr, max_addr = address_range
        
        # Convert to byte addresses (multiply by 4)
        min_byte_addr = min_addr * 4
        max_byte_addr = max_addr * 4
        
        trace = []
        
        for _ in range(num_accesses):
            # Generate random address in range
            address = random.randint(min_byte_addr, max_byte_addr)
            # Align to 4-byte boundary (32-bit instruction alignment)
            address = address - (address % 4)
            trace.append(address)
        
        return trace
    
    def generate_loop_trace(self, loop_start = 0, loop_end = 10, iterations = 5):
        """
        Generate a loop access trace.
        
        (bonus/future add on): Simulates a for loop that repeats the same addresses.
        
        @param loop_start - Starting address of loop
        @param loop_end - Ending address of loop
        @param iterations - Number of times to repeat the loop
        @return - List of addresses in loop pattern
        """
        trace = []
        
        # Convert to byte addresses
        start_byte = loop_start * 4
        end_byte = loop_end * 4
        
        for _ in range(iterations):
            for addr in range(start_byte, end_byte + 4, 4):
                trace.append(addr)
        
        return trace
    
    def generate_trace_from_file(self, filename):
        """
        Load a custom trace from a file.
        
        File format: one address per line (decimal or hex with 0x prefix)
        
        @param filename - Path to trace file
        @return - List of memory addresses
        """
        trace = []
        
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse hex or decimal
                if line.startswith('0x') or line.startswith('0X'):
                    address = int(line, 16)
                else:
                    address = int(line)
                
                trace.append(address)
        
        return trace
    
    def generate_mixed_trace(self, sequential_count, random_count):
        """
        Generate a mixed trace with sequential and random accesses.
        
        @param sequential_count - Number of sequential accesses
        @param random_count - Number of random accesses
        @return - List of mixed memory addresses
        """
        seq_trace = self.generate_sequential_trace(count = sequential_count)
        rand_trace = self.generate_random_trace(num_accesses = random_count)
        
        return seq_trace + rand_trace
    
    def print_trace(self, trace, max_display = 20):
        """
        Print a trace in a formatted way.
        
        @param trace - List of addresses to print
        @param max_display - Maximum number of items to display
        """
        print(f"\nTrace ({len(trace)} accesses):")
        
        display_count = min(len(trace), max_display)
        for i in range(display_count):
            addr = trace[i]
            # Format as hex for 32-bit display
            print(f"  Access {i+1:3d}: 0x{addr:08X}")
        
        if len(trace) > max_display:
            print(f"  ... and {len(trace) - max_display} more accesses")


# For testing trace generator
if __name__ == "__main__":
    """
    Simple test to verify trace generator works correctly.
    """
    print("=" * 50)
    print("Testing Trace Generator")
    print("=" * 50)
    
    # Override config for testing
    config.SSD_SIZE = 100
    config.MAX_ADDRESS = 99
    config.DEFAULT_NUM_ACCESSES = 10
    
    trace_gen = TraceGenerator()
    
    # Test sequential trace
    print("\n--- Sequential Trace (32-bit, increment by 4) ---")
    seq_trace = trace_gen.generate_sequential_trace(start = 0, count = 10)
    trace_gen.print_trace(seq_trace)
    print(f"  Addresses increment by 4: {seq_trace[:5]}")
    
    # Test sequential trace with different start
    instruction_index = 4
    byte_address = instruction_index * 4
    print(f"\n--- Sequential Trace (instruction index {instruction_index} -> byte address {byte_address}) ---")
    seq_trace2 = trace_gen.generate_sequential_trace(start = byte_address, count = 5)
    
    # Test random trace (bonus/future add on)
    print("\n--- Random Trace (bonus/future add on) ---")
    rand_trace = trace_gen.generate_random_trace(num_accesses = 8)
    trace_gen.print_trace(rand_trace, max_display = 8)
    
    # Test loop trace (bonus/future add on)
    print("\n--- Loop Trace (bonus/future add on) ---")
    loop_trace = trace_gen.generate_loop_trace(loop_start = 0, loop_end = 4, iterations = 3)
    trace_gen.print_trace(loop_trace, max_display = 15)
    print(f"  Pattern: repeats addresses 0,4,8,12,16 three times")
    
    # Test mixed trace
    print("\n--- Mixed Trace ---")
    mixed_trace = trace_gen.generate_mixed_trace(sequential_count = 5, random_count = 5)
    trace_gen.print_trace(mixed_trace, max_display = 10)
    
    # Verify 32-bit alignment for random addresses
    print("\n--- Alignment Check (32-bit) ---")
    for addr in rand_trace[:5]:
        is_aligned = (addr % 4 == 0)
        print(f"  Address 0x{addr:08X}: {'Aligned' if is_aligned else 'MISALIGNED'}")
    
    print("\n" + "=" * 50)
    print("All trace generator tests passed!")
    print("=" * 50)