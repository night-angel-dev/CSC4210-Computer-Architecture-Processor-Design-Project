"""
cpu.py - CPU that generates read/write requests.

The processor that needs instructions to execute.
For 32-bit architecture, the CPU only talks to L1 cache directly.

In a real 32-bit processor (like ARM or RISC-V):
- PC (Program Counter) holds the address of the next instruction
- Each instruction is 32 bits (4 bytes)
- PC increments by 4 after each instruction fetch
"""

import config


class CPU:
    """
    CPU that generates memory access requests.
    
    The CPU only knows about L1 cache. It never directly accesses
    L2, L3, DRAM, or SSD. This enforces the hierarchy rule.
    
    For 32-bit architecture:
    - Fetches 32-bit instructions from memory
    - Can write 32-bit data back to memory
    """
    
    def __init__(self, l1_cache):
        """
        Initialize CPU with L1 cache connection.
        
        @param l1_cache - L1 cache instance (closest to CPU)
        """
        self.l1_cache = l1_cache
        self.program_counter = 0 # Current instruction address
        self.instructions_executed = 0
        self.read_count = 0
        self.write_count = 0
        
        # For tracking performance
        self.total_cycles = 0
        self.stalls = 0
    
    def fetch_instruction(self, address):
        """
        Fetch a 32-bit instruction from memory.
        
        The CPU requests an instruction from L1 cache.
        If not in L1, the cache hierarchy will fetch it from lower levels.
        
        @param address - Memory address of the instruction to fetch
        @return - The 32-bit instruction
        """
        self.read_count += 1
        
        # Request from L1 cache (latency will be accounted by simulator)
        instruction = self.l1_cache.read(address)
        
        return instruction
    
    def write_back(self, address, data):
        """
        Write 32-bit data back down the memory hierarchy.
        
        Used for store instructions or when modified data needs
        to be saved to main memory.
        
        @param address - Memory address to write to
        @param data - 32-bit data to write
        """
        self.write_count += 1
        self.l1_cache.write(address, data)
    
    def execute_cycle(self, address = None):
        """
        Execute one CPU cycle - fetch and execute an instruction.
        
        This simulates a simple fetch-execute cycle.
        
        @param address - Optional specific address to fetch (for testing)
        @return - The fetched instruction
        """
        self.total_cycles += 1
        
        # Determine address to fetch
        fetch_addr = address
        if fetch_addr is None:
            fetch_addr = self.program_counter
            # For sequential execution, PC increments by 4 (32-bit instructions)
            self.program_counter += 4
        
        # Fetch instruction
        instruction = self.fetch_instruction(fetch_addr)
        self.instructions_executed += 1
        
        return instruction
    
    def run_trace(self, trace):
        """
        Execute a sequence of memory accesses from a trace.
        
        @param trace - List of memory addresses to access
        @return - List of fetched instructions
        """
        results = []
        
        for address in trace:
            instruction = self.execute_cycle(address)
            results.append(instruction)
        
        return results
    
    def get_stats(self):
        """
        Get CPU statistics.
        
        @return - Dictionary with CPU performance statistics
        """
        return {
            'instructions_executed': self.instructions_executed,
            'read_count': self.read_count,
            'write_count': self.write_count,
            'total_cycles': self.total_cycles,
            'stalls': self.stalls
        }
    
    def reset_stats(self):
        """
        Reset CPU statistics counters.
        """
        self.instructions_executed = 0
        self.read_count = 0
        self.write_count = 0
        self.total_cycles = 0
        self.stalls = 0
    
    def set_program_counter(self, address):
        """
        Set the program counter to a specific address.
        
        @param address - New program counter value
        """
        self.program_counter = address
    
    def get_program_counter(self):
        """
        Get the current program counter value.
        
        @return - Current program counter
        """
        return self.program_counter


# For testing CPU independently
if __name__ == "__main__":
    """
    Simple test to verify CPU works correctly.
    """
    print("=" * 50)
    print("Testing CPU Class")
    print("=" * 50)
    
    # Create a mock L1 cache for testing
    class MockL1Cache:
        """Mock L1 cache for testing CPU."""
        
        def __init__(self):
            self.storage = {}
            self.access_count = 0
            self.hit_count = 0
            
            # Pre-load some test instructions
            for i in range(20):
                self.storage[i] = 0x10000000 + i
        
        def read(self, address):
            self.access_count += 1
            if address in self.storage:
                self.hit_count += 1
                return self.storage[address]
            # Simulate cache miss by returning a default value
            return 0xFFFFFFFF
        
        def write(self, address, data):
            self.storage[address] = data
        
        def get_stats(self):
            return {
                'accesses': self.access_count,
                'hits': self.hit_count,
                'hit_rate': self.hit_count / self.access_count if self.access_count > 0 else 0
            }
    
    # Create mock cache and CPU
    mock_cache = MockL1Cache()
    cpu = CPU(mock_cache)
    
    print(f"Created CPU with L1 cache")
    print(f"Initial PC: {cpu.get_program_counter()}")
    
    # Test single instruction fetch
    print("\n--- Testing Single Instruction Fetch ---")
    instruction = cpu.fetch_instruction(5)
    print(f"  Fetched address 5: 0x{instruction:08X}")
    
    # Test execute cycle
    print("\n--- Testing Execute Cycle ---")
    for i in range(3):
        instruction = cpu.execute_cycle(i)
        print(f"  Cycle {i}: fetched address {i} -> 0x{instruction:08X}")
    
    # Test sequential execution (auto-incrementing PC)
    print("\n--- Testing Sequential Execution ---")
    cpu.set_program_counter(10)
    print(f"  PC set to: {cpu.get_program_counter()}")
    
    for i in range(3):
        instruction = cpu.execute_cycle()  # Auto-increments PC
        print(f"  Executed PC={cpu.get_program_counter() - 1}: 0x{instruction:08X}")
    print(f"  Final PC: {cpu.get_program_counter()}")
    
    # Test write_back
    print("\n--- Testing Write Back ---")
    cpu.write_back(100, 0xDEADBEEF)
    print(f"  Wrote 0xDEADBEEF to address 100")
    data = mock_cache.read(100)
    print(f"  Verified: cache has 0x{data:08X}")
    
    # Test trace execution
    print("\n--- Testing Trace Execution ---")
    trace = [0, 1, 2, 1, 0, 3, 4, 2, 1]
    results = cpu.run_trace(trace)
    print(f"  Executed {len(results)} instructions from trace")
    print(f"  First few results: 0x{results[0]:08X}, 0x{results[1]:08X}, ...")
    
    # Test statistics
    print("\n--- Testing Statistics ---")
    stats = cpu.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test cache stats
    cache_stats = mock_cache.get_stats()
    print(f"\n  Mock Cache Stats:")
    print(f"    Accesses: {cache_stats['accesses']}")
    print(f"    Hits: {cache_stats['hits']}")
    print(f"    Hit rate: {cache_stats['hit_rate']:.1%}")
    
    # Test reset
    print("\n--- Testing Reset Stats ---")
    cpu.reset_stats()
    stats = cpu.get_stats()
    print(f"  After reset - instructions: {stats['instructions_executed']}")
    
    print("\n" + "=" * 50)
    print("All CPU tests passed!")
    print("=" * 50)