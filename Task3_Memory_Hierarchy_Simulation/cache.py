"""
cache.py - Cache implementation (L1, L2, L3).

Small, fast memory with configurable replacement policies.
Supports L1, L2, and L3 cache levels.

For 32-bit architecture:
- Stores 32-bit instructions
- Smallest capacity but fastest access
- L1 is smallest/fastest, L3 is largest/slowest among caches
"""

from memory_level import MemoryLevel
import config
import random



class Cache(MemoryLevel):
    """
    Cache memory level with configurable replacement policies.
    
    Characteristics:
    - Small storage capacity
    - Fast access latency
    - Supports LRU, FIFO, and Random replacement policies
    - Automatically requests from lower level on miss
    """
    
    def __init__(self, name, size, latency, lower_level = None, upper_level = None, policy = None):
        """
        Initialize cache with specified policy.
        
        @param name - Cache level name (L1, L2, L3)
        @param size - Number of instructions cache can hold
        @param latency - Access latency in cycles
        @param lower_level - Level below (closer to DRAM)
        @param upper_level - Level above (closer to CPU)
        @param policy - Replacement policy (LRU, FIFO, Random)
        """
        super().__init__(name, size, latency, lower_level, upper_level)
        
        self.policy = policy
        if self.policy is None:
            self.policy = config.REPLACEMENT_POLICY
        
        # For tracking replacement policy state
        self.access_order = [] # For FIFO (order of insertion)
        self.lru_order = []    # For LRU (order of recent use)
        self.miss_count = 0    # Tracks cache misses seperately
    
    def read(self, address):
        # print(f"DEBUG Cache {self.name}: read({address}) called")
        
        self.access_count += 1

        # Check if data is in cache (HIT)
        if address in self.storage:
            print(f"DEBUG Cache {self.name}: HIT at {address}")
            self.hit_count += 1
            self._update_replacement_state(address)
            return self.storage[address]
        
        # MISS - need to get from lower level
        # print(f"DEBUG Cache {self.name}: MISS at {address}")
        self.miss_count += 1
        
        # Check if we have a lower level
        lower = self.lower_level
        # print(f"DEBUG Cache {self.name}: lower_level = {lower}")
        
        if lower is not None:
            # print(f"DEBUG Cache {self.name}: Has lower_level, calling read")
            data = lower.read(address)
            # print(f"DEBUG Cache {self.name}: Got data, writing to cache")
            self.write(address, data)
            return data
        
        # print(f"DEBUG Cache {self.name}: No lower_level available!")
        raise ValueError(f"Address {address} not found and no lower level available")
    
    
    def write(self, address, data):
        """
        Write a 32-bit instruction to cache.
        
        Handles eviction if cache is full.
        
        @param address - Memory address to write to
        @param data - 32-bit instruction data to store
        """
        self.write_count += 1
        
        # If already exists, just update
        if address in self.storage:
            self.storage[address] = data
            self._update_replacement_state(address)
            return
        
        # Check if we need to evict to make space
        if self.is_full():
            evicted = self.evict()
            if evicted is not None:
                del self.storage[evicted]
                self._remove_from_replacement_state(evicted)
        
        # Store new data
        self.storage[address] = data
        self._add_to_replacement_state(address)
    
    def evict(self):
        """
        Choose data to evict when cache is full.
        
        Uses the configured replacement policy.
        
        (Bonus/future add on): Implemented policies:
        - FIFO: Evict the oldest inserted item
        - LRU: Evict the least recently used item
        - Random: Evict a random item
        
        @return - Address of evicted item, or None if no eviction needed
        """
        if not self.is_full():
            return None
        
        if not self.storage:
            return None
        
        if self.policy == "FIFO":
            return self._evict_fifo()
        elif self.policy == "LRU":
            return self._evict_lru()
        elif self.policy == "Random":
            return self._evict_random()
        else:
            # Default to FIFO
            return self._evict_fifo()
    
    def _evict_fifo(self):
        """
        FIFO eviction: remove the oldest inserted item.
        
        @return - Address of evicted item
        """
        if self.access_order:
            return self.access_order[0]
        return next(iter(self.storage.keys()))
    
    def _evict_lru(self):
        """
        LRU eviction: remove the least recently used item.
        
        @return - Address of evicted item
        """
        if self.lru_order:
            return self.lru_order[0]
        return next(iter(self.storage.keys()))
    
    def _evict_random(self):
        """
        Random eviction: remove a random item.
        
        (Bonus/future add on): Requires import random at top of file.
        
        @return - Address of evicted item
        """
        return random.choice(list(self.storage.keys()))
    
    def _update_replacement_state(self, address):
        """
        Update replacement state on a cache hit.
        
        For LRU: move address to end (most recently used)
        For FIFO: no change on hit
        
        @param address - Address that was accessed
        """
        if self.policy == "LRU":
            if address in self.lru_order:
                self.lru_order.remove(address)
            self.lru_order.append(address)
    
    def _add_to_replacement_state(self, address):
        """
        Add address to replacement state on new insertion.
        
        @param address - Address being added
        """
        if self.policy == "FIFO":
            self.access_order.append(address)
        elif self.policy == "LRU":
            self.lru_order.append(address)
    
    def _remove_from_replacement_state(self, address):
        """
        Remove address from replacement state on eviction.
        
        @param address - Address being removed
        """
        if self.policy == "FIFO":
            if address in self.access_order:
                self.access_order.remove(address)
        elif self.policy == "LRU":
            if address in self.lru_order:
                self.lru_order.remove(address)
    
    def get_stats(self):
        """
        Get cache statistics.
        
        @return - Dictionary with cache performance statistics
        """
        stats = super().get_stats()
        stats['type'] = 'Cache'
        stats['policy'] = self.policy
        return stats


# For testing Cache independently
if __name__ == "__main__":
    """
    Simple test to verify Cache works correctly.
    """
    print("=" * 50)
    print("Testing Cache Class")
    print("=" * 50)
    
    # Override config for testing
    config.REPLACEMENT_POLICY = "LRU"
    
    # Create a mock lower level (DRAM/SSD simulator)
    class MockLowerLevel(MemoryLevel):
        """Mock lower level for testing cache."""
        
        def __init__(self):
            super().__init__(name = "MockLower", size = 100, latency = 50)
            # Load some test data
            for i in range(50):
                self.storage[i] = 0xA0000000 + i
        
        def read(self, address):
            self.access_count += 1
            if address in self.storage:
                self.hit_count += 1
                return self.storage[address]
            raise KeyError(f"Address {address} not in mock lower level")
        
        def write(self, address, data):
            self.storage[address] = data
    
    # Create mock lower level and cache
    mock_lower = MockLowerLevel()
    cache = Cache(name = "L1", size = 4, latency = 1, lower_level = mock_lower)
    
    print(f"Created: {cache}")
    print(f"Size: {cache.size} instructions")
    print(f"Latency: {cache.latency} cycles")
    print(f"Policy: {cache.policy}")
    
    # Test read operations (should miss and fetch from lower level)
    print("\n--- Testing Read Operations (Misses) ---")
    for addr in [0, 1, 2, 3]:
        data = cache.read(addr)
        print(f"  Read address {addr}: 0x{data:08X}")
    
    print(f"Cache storage after 4 reads: {len(cache)} items")
    print(f"  Addresses: {list(cache.storage.keys())}")
    
    # Test read that should be a hit
    print("\n--- Testing Read Operation (Hit) ---")
    data = cache.read(0)
    print(f"  Read address 0: 0x{data:08X} (should be HIT)")
    
    # Test eviction
    print("\n--- Testing Eviction (adding 5th item) ---")
    print(f"Before eviction: {list(cache.storage.keys())}")
    cache.read(4)
    print(f"After reading address 4: {list(cache.storage.keys())}")
    
    # Test LRU behavior
    print("\n--- Testing LRU Behavior ---")
    print(f"Current LRU order: {cache.lru_order}")
    cache.read(1)  # Access address 1 to make it most recent
    print(f"After accessing address 1: {cache.lru_order}")
    
    # Test write operation
    print("\n--- Testing Write Operation ---")
    cache.write(10, 0xDEADBEEF)
    print(f"  Wrote to address 10: 0xDEADBEEF")
    data = cache.read(10)
    print(f"  Read back: 0x{data:08X}")
    
    # Test statistics
    print("\n--- Testing Statistics ---")
    stats = cache.get_stats()
    print(f"  Name: {stats['name']}")
    print(f"  Accesses: {stats['accesses']}")
    print(f"  Hits: {stats['hits']}")
    print(f"  Hit rate: {stats['hit_rate']:.1%}")
    print(f"  Misses: {stats['misses']}")
    print(f"  Policy: {stats['policy']}")
    
    # Test FIFO policy
    print("\n--- Testing FIFO Policy ---")
    cache_fifo = Cache(name = "L1_FIFO", size = 3, latency = 1, 
                       lower_level = mock_lower, policy = "FIFO")
    for addr in [10, 11, 12]:
        cache_fifo.read(addr)
    print(f"FIFO cache after 10,11,12: {list(cache_fifo.storage.keys())}")
    print(f"FIFO access order: {cache_fifo.access_order}")
    cache_fifo.read(13)  # Should evict 10
    print(f"After reading 13: {list(cache_fifo.storage.keys())}")
    
    print("\n" + "=" * 50)
    print("All Cache tests passed!")
    print("=" * 50)