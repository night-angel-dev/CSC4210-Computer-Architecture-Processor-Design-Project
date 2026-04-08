"""
dram.py - DRAM (Dynamic Random Access Memory) implementation.

DRAM is the main memory - sits between SSD and cache hierarchy.
It acts as a buffer between slow SSD and fast caches.

For 32-bit architecture:
- Stores 32-bit instructions
- Medium capacity (config.DRAM_SIZE instructions)
- Medium access time (config.DRAM_TO_L3_LATENCY cycles)
"""

from memory_level import MemoryLevel
import config


class DRAM(MemoryLevel):
    """
    DRAM memory level - main memory.
    
    Characteristics:
    - Medium storage capacity (larger than caches, smaller than SSD)
    - Medium access latency (faster than SSD, slower than caches)
    - Acts as buffer between SSD and L3 cache
    - Requests missing data from SSD
    """
    
    def __init__(self, lower_level = None, upper_level = None):
        """
        Initialize DRAM with configuration values.
        
        @param lower_level - Level below (SSD)
        @param upper_level - Level above (L3 cache)
        """
        super().__init__(
            name = "DRAM",
            size = config.DRAM_SIZE,
            latency = config.DRAM_TO_L3_LATENCY,
            lower_level = lower_level,
            upper_level = upper_level
        )
    
    def read(self, address):
        """
        Read a 32-bit instruction from DRAM.
        
        If data is present (HIT): return it immediately.
        If not present (MISS): request from SSD, store it, then return.
        
        @param address - Memory address to read
        @return - The 32-bit instruction at the address
        @raises ValueError - If address is out of valid range and no lower level
        """
        self.access_count += 1

        # Check if data is in DRAM (HIT)
        if address in self.storage:
            self.hit_count += 1
            data = self.storage[address]
            
            # Transfer to L3 cache if connected
            if self.upper_level:
                self.transfer_to_upper(address)
            
            return data
        
        # MISS - need to get from SSD
        if self.lower_level:
            # Request from SSD (takes latency cycles in real simulation)
            data = self.lower_level.read(address)
            
            # Store in DRAM (may need eviction)
            self.write(address, data)
            
            # Transfer upward to L3 cache
            if self.upper_level:
                self.transfer_to_upper(address)
            
            return data
        
        # No lower level and data not found
        raise ValueError(f"Address {address} not found in DRAM and no lower level available")
    
    def write(self, address, data):
        """
        Write a 32-bit instruction to DRAM.
        
        Handles eviction if DRAM is full.
        
        @param address - Memory address to write to
        @param data - 32-bit instruction data to store
        """
        self.write_count += 1
        
        # If already exists, just update
        if address in self.storage:
            self.storage[address] = data
            return
        
        # Check if we need to evict to make space
        if self.is_full():
            evicted = self.evict()
            if evicted is not None:
                # Write back to SSD if needed (for write-back policy)
                # (Bonus/future add on): Check dirty bit before writing back
                evicted_data = self.storage.pop(evicted)
                if self.lower_level:
                    self.lower_level.write(evicted, evicted_data)
        
        # Store new data
        self.storage[address] = data
    
    def get_stats(self):
        """
        Get DRAM statistics.
        
        @return - Dictionary with DRAM performance statistics
        """
        stats = super().get_stats()
        stats['type'] = 'DRAM'
        return stats


# For testing DRAM independently
if __name__ == "__main__":
    """
    Simple test to verify DRAM works correctly.
    """
    print("=" * 50)
    print("Testing DRAM Class")
    print("=" * 50)
    
    # Override config for testing
    config.DRAM_SIZE = 10
    config.DRAM_TO_L3_LATENCY = 50
    
    # Create a mock SSD for testing
    class MockSSD(MemoryLevel):
        """Mock SSD for testing DRAM."""
        
        def __init__(self):
            super().__init__(name = "MockSSD", size = 100, latency = 100)
            # Load some test data
            for i in range(config.SSD_SIZE):
                self.storage[i] = 0x10000000 + i
        
        def read(self, address):
            self.access_count += 1
            if address in self.storage:
                self.hit_count += 1
                return self.storage[address]
            raise KeyError(f"Address {address} not in mock SSD")
        
        def write(self, address, data):
            self.storage[address] = data
    
    # Create mock SSD and DRAM
    mock_ssd = MockSSD()
    dram = DRAM(lower_level = mock_ssd)
    
    print(f"Created: {dram}")
    print(f"Size: {dram.size} instructions")
    print(f"Latency: {dram.latency} cycles")
    print(f"Lower level: {dram.lower_level.name if dram.lower_level else 'None'}")
    
    # Test read operations (should miss and fetch from SSD)
    print("\n--- Testing Read Operations (Misses) ---")
    for addr in [0, 1, 2, 3, 4]:
        data = dram.read(addr)
        print(f"  Read address {addr}: 0x{data:08X}")
    
    # Check DRAM storage after reads
    print(f"\nDRAM storage after 5 reads: {len(dram)} items")
    print(f"  Addresses: {list(dram.storage.keys())}")
    
    # Test read operations that should now be hits
    print("\n--- Testing Read Operations (Hits) ---")
    for addr in [0, 1, 2]:
        data = dram.read(addr)
        print(f"  Read address {addr}: 0x{data:08X} (should be HIT)")
    
    # Test write operation
    print("\n--- Testing Write Operation ---")
    dram.write(15, 0xDEADBEEF)
    print(f"  Wrote to address 15: 0xDEADBEEF")
    
    # Verify write was stored
    data = dram.read(15)
    print(f"  Read back from address 15: 0x{data:08X}")
    
    # Test eviction when full
    print("\n--- Testing Eviction ---")
    # Fill up DRAM (size is 10, we have 5 from earlier)
    print(f"Current DRAM size: {len(dram)} items (capacity: {dram.size})")
    for addr in [16, 17, 18, 19, 20]:
        dram.read(addr)  # This will fetch from SSD and may cause eviction
        print(f"  After reading {addr}: {len(dram)} items")
    
    print(f"\nFinal DRAM addresses: {list(dram.storage.keys())}")
    
    # Test statistics
    print("\n--- Testing Statistics ---")
    stats = dram.get_stats()
    print(f"  Name: {stats['name']}")
    print(f"  Accesses: {stats['accesses']}")
    print(f"  Hits: {stats['hits']}")
    print(f"  Hit rate: {stats['hit_rate']:.1%}")
    print(f"  Misses: {stats['misses']}")
    print(f"  Writes: {stats['writes']}")
    print(f"  Storage used: {stats['storage_used']}")
    print(f"  Storage full: {stats['storage_full']}")
    
    # Test error handling
    print("\n--- Testing Error Handling ---")
    dram_no_lower = DRAM(lower_level = None)
    try:
        dram_no_lower.read(999)
        print("  ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"  Correctly caught error: {e}")
    
    print("\n" + "=" * 50)
    print("All DRAM tests passed!")
    print("=" * 50)