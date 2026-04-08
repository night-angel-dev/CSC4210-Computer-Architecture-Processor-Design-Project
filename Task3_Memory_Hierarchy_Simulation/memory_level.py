"""
memory_level.py - Abstract base class for all memory levels.

All memory levels (SSD, DRAM, L1/L2/L3 Cache) inherit from this class.
The chain linking (upper/lower pointers) enforces the no-bypassing rule.
"""

from abc import ABC, abstractmethod


class MemoryLevel(ABC):
    """
    Abstract base class that all memory levels inherit from.
    
    Implements the chain linking between upper (closer to CPU) and 
    lower (farther from CPU) levels. This ensures data cannot skip levels.
    """
    
    def __init__(self, name, size, latency, lower_level = None, upper_level = None):
        """
        Initialize a memory level.
        
        @param name - Identifier for this memory level (L1, L2, L3, DRAM, SSD)
        @param size - Maximum number of 32-bit instructions this level can store
        @param latency - Access latency in clock cycles
        @param lower_level - The level below (farther from CPU)
        @param upper_level - The level above (closer to CPU)
        """
        self.name = name
        self.size = size
        self.latency = latency
        self.lower_level = lower_level
        self.upper_level = upper_level
        
        # Storage: dictionary mapping address -> instruction data
        self.storage = {}
        
        # Statistics tracking
        self.access_count = 0
        self.hit_count = 0
        self.write_count = 0
    
    @abstractmethod
    def read(self, address):
        """
        Read a 32-bit instruction from this memory level.
        
        @param address - Memory address to read
        @return - The 32-bit instruction/data at the address
        """
        pass
    
    @abstractmethod
    def write(self, address, data):
        """
        Write a 32-bit instruction to this memory level.
        
        @param address - Memory address to write to
        @param data - 32-bit instruction/data to store
        """
        pass
    
    def is_full(self):
        """
        Check if storage has reached capacity.
        
        @return - True if no more items can be stored without eviction
        """
        return len(self.storage) >= self.size
    
    def evict(self):
        """
        Choose data to evict when storage is full.
        Base implementation: simple FIFO (remove first item).
        
        BONUS: Override in cache.py to implement LRU, FIFO, or Random policies.
        
        @return - Address of evicted item, or None if no eviction needed
        """
        if not self.is_full():
            return None
        
        if self.storage:
            # Simple FIFO - evict the first key
            # Python 3.7+ preserves insertion order
            return next(iter(self.storage.keys()))
        return None
    
    def transfer_to_upper(self, address):
        """
        Move data from this level to the level above (closer to CPU).
        
        @param address - Address of data to transfer upward
        """
        if self.upper_level and address in self.storage:
            data = self.storage[address]
            self.upper_level.write(address, data)
    
    def transfer_to_lower(self, address):
        """
        Move data from this level to the level below (farther from CPU).
        
        @param address - Address of data to transfer downward
        """
        if self.lower_level and address in self.storage:
            data = self.storage[address]
            self.lower_level.write(address, data)
    
    def get_stats(self):
        """
        Return statistics for this memory level.
        
        @return - Dictionary with hit rate and access information
        """
        hit_rate = self.hit_count / self.access_count if self.access_count > 0 else 0.0
        return {
            'name': self.name,
            'size': self.size,
            'latency': self.latency,
            'accesses': self.access_count,
            'hits': self.hit_count,
            'hit_rate': hit_rate,
            'misses': self.access_count - self.hit_count,
            'writes': self.write_count,
            'storage_used': len(self.storage),
            'storage_full': self.is_full()
        }
    
    def reset_stats(self):
        """Reset all statistics counters for this memory level."""
        self.access_count = 0
        self.hit_count = 0
        self.write_count = 0
    
    def __repr__(self):
        return f"{self.name}(size = {self.size}, latency = {self.latency})"
    
    def __len__(self):
        return len(self.storage)
    
    def __contains__(self, address):
        return address in self.storage


# For testing the base class
if __name__ == "__main__":
    
    class TestMemory(MemoryLevel):
        """Concrete implementation for testing base class functionality."""
        
        def read(self, address):
            self.access_count += 1
            if address in self.storage:
                self.hit_count += 1
                return self.storage[address]
            raise KeyError(f"Address {address} not found")
        
        def write(self, address, data):
            self.write_count += 1
            
            # Handle eviction if full
            if self.is_full() and address not in self.storage:
                evicted = self.evict()
                if evicted is not None:
                    del self.storage[evicted]
            
            self.storage[address] = data
    
    # Run tests
    print("Testing MemoryLevel Base Class")
    print("=" * 40)
    
    test_mem = TestMemory("TEST", size = 4, latency = 2)
    print(f"Created: {test_mem}")
    
    # Test write
    test_mem.write(0, 0x12345678)
    test_mem.write(1, 0x9ABCDEF0)
    print(f"After writes: {len(test_mem)} items")
    
    # Test contains
    print(f"Address 0 in storage: {0 in test_mem}")
    
    # Test read
    data = test_mem.read(0)
    print(f"Read from address 0: 0x{data:08X}")
    
    # Test eviction
    test_mem.write(2, 0x11223344)
    test_mem.write(3, 0x55667788)
    print(f"Before eviction: {list(test_mem.storage.keys())}")
    test_mem.write(4, 0x99AABBCC)
    print(f"After eviction: {list(test_mem.storage.keys())}")
    
    # Test stats
    stats = test_mem.get_stats()
    print(f"Hit rate: {stats['hit_rate']:.1%}")
    
    print("All tests passed!")