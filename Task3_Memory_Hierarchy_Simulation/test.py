"""
test.py - Unit tests for memory hierarchy simulation.
"""

import unittest
import config
from memory_level import MemoryLevel
from ssd import SSD
from dram import DRAM
from cache import Cache
from cpu import CPU
from clock import Clock
from trace import TraceGenerator
from simulator import Simulator


class TestMemoryLevel(unittest.TestCase):
    """Test base class functionality."""
    
    def setUp(self):
        class ConcreteMemory(MemoryLevel):
            def read(self, address):
                self.access_count += 1
                if address in self.storage:
                    self.hit_count += 1
                    return self.storage[address]
                raise KeyError("Not found")
            
            def write(self, address, data):
                self.write_count += 1
                if self.is_full() and address not in self.storage:
                    evicted = self.evict()
                    if evicted is not None:
                        del self.storage[evicted]
                self.storage[address] = data
        
        self.mem = ConcreteMemory("TEST", size=4, latency=2)
    
    def test_write_and_read(self):
        self.mem.write(10, 0x12345678)
        self.assertTrue(self.mem.has_data(10))
        self.assertEqual(self.mem.write_count, 1)
    
    def test_eviction(self):
        for i in range(4):
            self.mem.write(i, i)
        self.mem.write(4, 4)
        self.assertNotIn(0, self.mem.storage)
        self.assertIn(4, self.mem.storage)


class TestSSD(unittest.TestCase):
    """Test SSD operations."""
    
    def setUp(self):
        self.ssd = SSD()
        # Load instructions at byte addresses 0, 4, 8
        self.ssd.load_instructions({0: 0x12345678, 4: 0x9ABCDEF0, 8: 0xDEADBEEF})
    
    def test_read(self):
        self.assertEqual(self.ssd.read(0), 0x12345678)
        self.assertEqual(self.ssd.read(4), 0x9ABCDEF0)
        self.assertEqual(self.ssd.read(8), 0xDEADBEEF)
    
    def test_write(self):
        # Write to address 12 (new location)
        self.ssd.write(12, 0xCAFEBABE)
        self.assertEqual(self.ssd.read(12), 0xCAFEBABE)
        
        # Overwrite existing address
        self.ssd.write(4, 0x55555555)
        self.assertEqual(self.ssd.read(4), 0x55555555)


class TestCache(unittest.TestCase):
    """Test cache with LRU eviction."""
    
    def setUp(self):
        class MockLower(MemoryLevel):
            def __init__(self):
                super().__init__("Mock", 100, 50)
                for i in range(50):
                    self.storage[i] = 0xA0000000 + i
            def read(self, address):
                return self.storage[address]
            def write(self, address, data):
                self.storage[address] = data
        
        self.mock_lower = MockLower()
        self.cache = Cache("L1", size=3, latency=1, lower_level=self.mock_lower, policy="LRU")
    
    def test_miss_then_hit(self):
        data = self.cache.read(0)
        self.assertEqual(data, 0xA0000000)
        self.assertEqual(self.cache.read(0), 0xA0000000)
        self.assertEqual(self.cache.hit_count, 1)
    
    def test_lru_eviction(self):
        self.cache.read(10)
        self.cache.read(11)
        self.cache.read(12)
        self.cache.read(10)  # Make 10 most recent
        self.cache.read(13)  # Should evict 11
        self.assertIn(10, self.cache.storage)
        self.assertNotIn(11, self.cache.storage)


class TestCPU(unittest.TestCase):
    """Test CPU fetch and execute."""
    
    def setUp(self):
        class MockL1(MemoryLevel):
            def __init__(self):
                super().__init__("MockL1", 16, 1)
                for i in range(0, 64, 4):
                    self.storage[i] = 0x10000000 + i
            def read(self, address):
                return self.storage.get(address, 0xFFFFFFFF)
            def write(self, address, data):
                self.storage[address] = data
        
        self.cpu = CPU(MockL1())
    
    def test_fetch(self):
        self.assertEqual(self.cpu.fetch_instruction(0), 0x10000000)
    
    def test_execute_cycle(self):
        inst = self.cpu.execute_cycle()
        self.assertEqual(inst, 0x10000000)
        self.assertEqual(self.cpu.program_counter, 4)


class TestClock(unittest.TestCase):
    """Test clock."""
    
    def setUp(self):
        self.clock = Clock()  # Change from SimpleClock to Clock
    
    def test_tick(self):
        self.assertEqual(self.clock.get_current_cycle(), 0)
        self.clock.tick()
        self.assertEqual(self.clock.get_current_cycle(), 1)
    
    def test_reset(self):
        self.clock.tick()
        self.clock.tick()
        self.clock.reset()
        self.assertEqual(self.clock.get_current_cycle(), 0)


class TestTraceGenerator(unittest.TestCase):
    """Test trace generation."""
    
    def setUp(self):
        config.SSD_SIZE = 100
        self.trace_gen = TraceGenerator()
    
    def test_sequential(self):
        trace = self.trace_gen.generate_sequential_trace(start=0, count=5)
        self.assertEqual(trace, [0, 4, 8, 12, 16])
    
    def test_random_alignment(self):
        trace = self.trace_gen.generate_random_trace(num_accesses=10)
        for addr in trace:
            self.assertEqual(addr % 4, 0)


class TestSimulator(unittest.TestCase):
    """Test simulator integration."""
    
    def setUp(self):
        config.SSD_SIZE = 50
        config.DRAM_SIZE = 20
        config.L3_SIZE = 8
        config.L2_SIZE = 6
        config.L1_SIZE = 4
        trace_gen = TraceGenerator()
        trace = trace_gen.generate_sequential_trace(count=5)
        self.sim = Simulator(trace=trace)
    
    def test_hierarchy_chain(self):
        self.assertEqual(self.sim.l1.lower_level, self.sim.l2)
        self.assertEqual(self.sim.l2.lower_level, self.sim.l3)
        self.assertEqual(self.sim.l3.lower_level, self.sim.dram)
    
    def test_read(self):
        instruction = self.sim.process_read(0)
        self.assertEqual(instruction, 0x10000000)
    
    def test_run(self):
        try:
            self.sim.run()
        except Exception as e:
            self.fail(f"Run failed: {e}")


if __name__ == "__main__":
    # Override config for testing
    config.SSD_SIZE = 100
    config.DRAM_SIZE = 50
    config.L3_SIZE = 16
    config.L2_SIZE = 8
    config.L1_SIZE = 4
    config.REPLACEMENT_POLICY = "LRU"
    
    unittest.main()