"""
ssd.py -  SSD memory level. The “hard drive” or “solid state drive”, the largest, slowest storage.
"""

"""
ssd.py - SSD (Solid State Drive) implementation.

SSD is the largest, slowest storage - the bottom of the hierarchy.
It is the source of truth for all data in the system.

For 32-bit architecture:
- Stores 32-bit instructions
- Largest capacity (config.SSD_SIZE instructions)
- Slowest access time (config.SSD_TO_DRAM_LATENCY cycles)
"""

from memory_level import MemoryLevel
import config


class SSD(MemoryLevel):
    """
    SSD memory level - the source of truth for all data.
    
    Characteristics:
    - Largest storage capacity
    - Slowest access latency
    - Never requests from lower levels (it's the bottom)
    - All instructions are initially loaded here
    """
    
    def __init__(self, upper_level = None):
        """
        Initialize SSD with configuration values.
        
        @param upper_level - Level above (DRAM), will be set by simulator
        """
        super().__init__(
            name = "SSD",
            size = config.SSD_SIZE,
            latency = config.SSD_TO_DRAM_LATENCY,
            lower_level = None,  # No level below SSD
            upper_level = upper_level
        )
    
    def load_instructions(self, instructions):
        """
        Load initial program instructions into SSD.
        
        This is called at simulation start to populate the memory hierarchy.
        
        @param instructions - Dictionary mapping addresses to 32-bit instruction data
        """
        # Convert byte address to instruction indixes
        self.storage = {}
        
        for byte_addr, data in instructions.items():
            instruction_index = byte_addr // 4
            self.storage[instruction_index] = data
        
        print(f"SSD: Loaded {len(instructions)} instructions (byte addresses 0 to {(len(instructions)-1)*4})")
    
    def read(self, address):
        """
        Read a 32-bit instruction from SSD.
        
        SSD always has the data as it is the source of truth.
        If address is not found, it is out of valid range.
        
        @param address - Memory address to read
        @return - The 32-bit instruction at the address
        @raises ValueError - If address exceeds SSD capacity
        """
        self.access_count += 1
        
        # convert byte address to instruction index
        instruction_index = address//4
        
        # Validate address range (convert size to byte address range)
        if instruction_index < 0 or instruction_index >= self.size:
            raise ValueError(f"Address {address} (index {instruction_index}) out of range for SSD (0 to {(self.size - 1) * 4})")
        
        # Check if data exists (using instruction index)
        if instruction_index not in self.storage:
            raise ValueError(f"Address {address} (index {instruction_index}) not found in SSD. Did you load instructions?")
        
        # SSD always "hits" since it has all data
        self.hit_count += 1
        
        # Transfer to DRAM (level above) if connected
        if self.upper_level:
            self.transfer_to_upper(address)
        
        return self.storage[instruction_index]
    
    def write(self, address, data):
        """
        Write a 32-bit instruction to SSD (persistent storage).
        
        @param address - Memory address to write to
        @param data - 32-bit instruction data to store
        @raises ValueError - If address exceeds SSD capacity
        """
        # Convert byte address to instruction index
        instruction_index = address // 4
        
        # Validate address range
        if instruction_index < 0 or instruction_index >= self.size:
            raise ValueError(f"Address {address} (index {instruction_index}) out of range for SSD (0 to {(self.size - 1) * 4})")
        
        self.write_count += 1
        self.storage[instruction_index] = data
        
        # (Future bonus/add on) For write-through policy, propagate to upper level
        # if self.upper_level:
        #     self.transfer_to_upper(address)
    
    def is_full(self):
        """
        Check if SSD is full.
        
        For simulation purposes, SSD is never considered full.
        It can always accept new data even though real SSDs have limits.
        
        @return - Always False (SSD never needs eviction in this simulation)
        """
        return False
    
    def evict(self):
        """
        Eviction not needed for SSD.
        
        (Future bonus/add on) If implementing limited SSD storage, override this method.
        
        @return - None (SSD doesn't evict in this simulation)
        """
        return None
    
    def get_stats(self):
        """
        Get SSD statistics.
        
        @return - Dictionary with SSD performance statistics
        """
        stats = super().get_stats()
        stats['type'] = 'SSD'
        stats['total_instructions'] = len(self.storage)
        return stats


# For testing SSD independently
if __name__ == "__main__":
    """
    Simple test to verify SSD works correctly.
    """
    print("=" * 50)
    print("Testing SSD Class")
    print("=" * 50)
    
    # Override config for testing if needed
    config.SSD_SIZE = 100
    config.SSD_TO_DRAM_LATENCY = 100
    
    # Create SSD
    ssd = SSD()
    print(f"Created: {ssd}")
    print(f"Size: {ssd.size} instructions")
    print(f"Latency: {ssd.latency} cycles")
    
    # Load test instructions
    test_instructions = {
        0: 0x12345678,   # 32-bit instruction 1
        1: 0x9ABCDEF0,   # 32-bit instruction 2
        2: 0x11223344,   # 32-bit instruction 3
        3: 0x55667788,   # 32-bit instruction 4
        4: 0x99AABBCC    # 32-bit instruction 5
    }
    ssd.load_instructions(test_instructions)
    print(f"\nLoaded {len(test_instructions)} instructions")
    
    # Test read operations
    print("\n--- Testing Read Operations ---")
    for addr in [0, 2, 4]:
        data = ssd.read(addr)
        print(f"  Read address {addr}: 0x{data:08X}")
    
    # Test statistics after reads
    print("\n--- Testing Statistics ---")
    stats = ssd.get_stats()
    print(f"  Accesses: {stats['accesses']}")
    print(f"  Hits: {stats['hits']}")
    print(f"  Hit rate: {stats['hit_rate']:.1%}")
    print(f"  Writes: {stats['writes']}")
    
    # Test write operation
    print("\n--- Testing Write Operation ---")
    ssd.write(10, 0xDEADBEEF)
    print(f"  Wrote to address 10: 0xDEADBEEF")
    data = ssd.read(10)
    print(f"  Read back: 0x{data:08X}")
    
    # Test invalid address handling
    print("\n--- Testing Error Handling ---")
    try:
        ssd.read(999)  # Beyond SSD_SIZE
        print("  ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"  Correctly caught error: {e}")
    
    # Test is_full (should always be False)
    print(f"\n--- is_full() returns: {ssd.is_full()} (SSD never full)")
    
    # Print final stats
    print("\n--- Final Statistics ---")
    stats = ssd.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 50)
    print("All SSD tests passed!")
    print("=" * 50)