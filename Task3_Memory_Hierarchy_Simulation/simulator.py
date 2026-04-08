"""
simulator.py - Main simulation logic tying everything together.

Builds the hierarchy chain (SSD -> DRAM -> L3 -> L2 -> L1)
Processes each access in the trace and tracks data movement.

For 32-bit architecture:
- Addresses are byte addresses (increment by 4)
- Each instruction is 32 bits (4 bytes)
- Hierarchy rule: SSD > DRAM > L3 > L2 > L1
"""

import config
from memory_level import MemoryLevel
from ssd import SSD
from dram import DRAM
from cache import Cache
from cpu import CPU
from clock import Clock
from trace import TraceGenerator
from memory_display_utils import MemoryDisplayUtils


class Simulator:
    """
    Main simulation class that orchestrates the memory hierarchy.
    
    Responsibilities:
    1. Build the hierarchy chain (SSD -> DRAM -> L3 -> L2 -> L1)
    2. Load initial instructions into SSD
    3. Process each access in the trace
    4. Track statistics and log data movement
    """
    
    def __init__(self, trace = None):
        """
        Initialize the simulator with configuration and trace.
        
        @param trace - List of memory addresses to simulate (optional)
        """
        # Build the memory hierarchy
        self.ssd = None
        self.dram = None
        self.l3 = None
        self.l2 = None
        self.l1 = None
        self.cpu = None
        self.clock = None
        self.display = MemoryDisplayUtils()
        
        self.build_hierarchy()
        
        # Load default instructions into SSD
        self.load_default_instructions()
        
        # Set up trace
        self.trace = trace
        if self.trace is None:
            # Generate default sequential trace
            trace_gen = TraceGenerator()
            self.trace = trace_gen.generate_sequential_trace(count = config.DEFAULT_NUM_ACCESSES)
        
        # Statistics tracking
        self.total_cycles = 0
        self.transfer_log = []
    
    def build_hierarchy(self):
        """
        Build the memory hierarchy chain.
        
        Chain: SSD -> DRAM -> L3 -> L2 -> L1 -> CPU
        Data cannot skip levels.
        """
        # Create clock
        self.clock = Clock()
        
        # Create SSD (bottom of hierarchy)
        self.ssd = SSD()
        
        # Create DRAM with SSD as lower level
        self.dram = DRAM(lower_level = self.ssd)
        
        # Create L3 cache with DRAM as lower level
        self.l3 = Cache(name = "L3", size = config.L3_SIZE, 
                        latency = config.L3_TO_L2_LATENCY,
                        lower_level = self.dram)

        # Create L2 cache with L3 as lower level
        self.l2 = Cache(name = "L2", size = config.L2_SIZE,
                        latency = config.L2_TO_L1_LATENCY,
                        lower_level = self.l3)

        # Create L1 cache with L2 as lower level
        self.l1 = Cache(name = "L1", size = config.L1_SIZE,
                        latency = config.L1_ACCESS_LATENCY,
                        lower_level = self.l2)

        # DEBUG: Print to verify connections
        # print(f"DEBUG: self.l2 = {self.l2}")
        # print(f"DEBUG: self.l1 = {self.l1}")
        # print(f"DEBUG: self.l1.lower_level = {self.l1.lower_level}")
        # print(f"DEBUG: self.l1.upper_level = {self.l1.upper_level}")
        # print(f"DEBUG: Type of self.l1.lower_level = {type(self.l1.lower_level)}")
        
        # Connect upper levels (closer to CPU)
        self.ssd.upper_level = self.dram
        self.dram.upper_level = self.l3
        self.l3.upper_level = self.l2
        self.l2.upper_level = self.l1
        
        # Create CPU with L1 cache
        self.cpu = CPU(l1_cache = self.l1)
    
    def load_default_instructions(self):
        """
        Load default instructions into SSD.
        
        For simulation, we load instructions at addresses 0, 4, 8, ...
        Each instruction is a unique 32-bit value (0x10000000 + address).
        """
        instructions = {}
        
        for i in range(config.SSD_SIZE):
            # Byte address (each instruction is 4 bytes)
            byte_addr = i * 4
            # Create a unique instruction value (32-bit)
            instructions[byte_addr] = 0x10000000 + byte_addr
        
        self.ssd.load_instructions(instructions)
    
    def process_read(self, address):
        """
        Process a read request through the memory hierarchy.
        
        @param address - Memory address to read
        @return - The 32-bit instruction at the address
        """
        # Simulate clock cycles for L1 access
        self.clock.tick()
        self.total_cycles += 1
        
        # CPU requests from L1
        instruction = self.cpu.fetch_instruction(address)
        
        return instruction
    
    def process_write(self, address, data):
        """
        Process a write request through the memory hierarchy.
        
        @param address - Memory address to write to
        @param data - 32-bit data to write
        """
        # Simulate clock cycles
        self.clock.tick()
        self.total_cycles += 1
        
        # CPU writes to L1
        self.cpu.write_back(address, data)
    
    def log_movement(self, from_level, to_level, address, latency):
        """
        Record a data movement between levels.
        
        @param from_level - Source memory level name
        @param to_level - Destination memory level name
        @param address - Address being transferred
        @param latency - Transfer latency in cycles
        """
        self.transfer_log.append({
            'cycle': self.clock.get_current_cycle(),
            'from': from_level,
            'to': to_level,
            'address': address,
            'latency': latency
        })
    
    def run(self):
        """
        Run the full simulation.
        
        Processes each address in the trace and collects statistics.
        """
        print("=" * 58)
        print("MEMORY HIERARCHY SIMULATION")
        print("=" * 58)
        
        # Print configuration
        config_dict = {
            'SSD_SIZE': config.SSD_SIZE,
            'DRAM_SIZE': config.DRAM_SIZE,
            'L3_SIZE': config.L3_SIZE,
            'L2_SIZE': config.L2_SIZE,
            'L1_SIZE': config.L1_SIZE,
            'SSD_TO_DRAM_LATENCY': config.SSD_TO_DRAM_LATENCY,
            'DRAM_TO_L3_LATENCY': config.DRAM_TO_L3_LATENCY,
            'L3_TO_L2_LATENCY': config.L3_TO_L2_LATENCY,
            'L2_TO_L1_LATENCY': config.L2_TO_L1_LATENCY,
            'L1_ACCESS_LATENCY': config.L1_ACCESS_LATENCY,
            'BANDWIDTH': config.BANDWIDTH,
            'REPLACEMENT_POLICY': config.REPLACEMENT_POLICY,
            'WRITE_POLICY': config.WRITE_POLICY
        }
        self.display.print_config_summary(config_dict)
        
        # Print trace
        print("INSTRUCTION ACCESS TRACE")
        print("-" * 58)
        trace_gen = TraceGenerator()
        trace_gen.print_trace(self.trace)
        
        # Process each access
        print("\n" + "=" * 58)
        print("EXECUTING ACCESSES")
        print("=" * 58)
        
        for i, address in enumerate(self.trace):
            print(f"\nAccess {i+1}: READ address {self.display.format_address(address)}")
            instruction = self.process_read(address)
            print(f"  Retrieved instruction: {self.display.format_instruction(instruction)}")
        
        # Print results
        self.print_results()
    
    def print_results(self):
        """
        Print simulation results including statistics and final memory state.
        """
        print("\n" + "=" * 58)
        print("SIMULATION RESULTS")
        print("=" * 58)
        
        # Print cache statistics
        print("\nCACHE STATISTICS")
        print("-" * 58)
        
        for cache in [self.l1, self.l2, self.l3]:
            stats = cache.get_stats()
            print(f"{stats['name']}: Hits={stats['hits']}, Misses={stats['misses']}, Hit Rate={stats['hit_rate']:.1%}")
        
        # Print DRAM statistics
        print("\nDRAM STATISTICS")
        print("-" * 58)
        dram_stats = self.dram.get_stats()
        print(f"DRAM: Accesses={dram_stats['accesses']}, Hits={dram_stats['hits']}, Hit Rate={dram_stats['hit_rate']:.1%}")
        
        # Print SSD statistics
        print("\nSSD STATISTICS")
        print("-" * 58)
        ssd_stats = self.ssd.get_stats()
        print(f"SSD: Accesses={ssd_stats['accesses']}, Hit Rate={ssd_stats['hit_rate']:.1%}")
        
        # Print CPU statistics
        print("\nCPU STATISTICS")
        print("-" * 58)
        cpu_stats = self.cpu.get_stats()
        print(f"Instructions Executed: {cpu_stats['instructions_executed']}")
        print(f"Total Reads: {cpu_stats['read_count']}")
        print(f"Total Writes: {cpu_stats['write_count']}")
        print(f"Total Cycles: {self.total_cycles}")
        
        # Print final memory state
        print("\n" + "=" * 58)
        print("FINAL MEMORY STATE")
        print("=" * 58)
        
        self.display.print_memory_snapshot("L1 Cache", self.l1.storage, max_items = 10)
        self.display.print_memory_snapshot("L2 Cache", self.l2.storage, max_items = 10)
        self.display.print_memory_snapshot("L3 Cache", self.l3.storage, max_items = 10)
        self.display.print_memory_snapshot("DRAM", self.dram.storage, max_items = 10)
        self.display.print_memory_snapshot("SSD", self.ssd.storage, max_items = 10)
    
    def get_hit_rate(self, level):
        """
        Calculate hit rate for a specific cache level.
        
        @param level - String indicating which cache ("L1", "L2", or "L3")
        @return - Hit rate as a float between 0 and 1
        """
        if level == "L1":
            stats = self.l1.get_stats()
        elif level == "L2":
            stats = self.l2.get_stats()
        elif level == "L3":
            stats = self.l3.get_stats()
        else:
            return 0.0
        
        return stats['hit_rate']
    
    def get_total_cycles(self):
        """
        Return total simulation cycles.
        
        @return - Total cycle count
        """
        return self.total_cycles
    
    def reset_stats(self):
        """
        Reset all statistics between runs.
        """
        self.ssd.reset_stats()
        self.dram.reset_stats()
        self.l3.reset_stats()
        self.l2.reset_stats()
        self.l1.reset_stats()
        self.cpu.reset_stats()
        self.clock.reset()
        self.total_cycles = 0
        self.transfer_log.clear()


# For testing the simulator independently
if __name__ == "__main__":
    """
    Simple test to verify simulator works correctly.
    """
    print("=" * 58)
    print("TESTING SIMULATOR")
    print("=" * 58)
    
    # Override config for testing
    config.SSD_SIZE = 50
    config.DRAM_SIZE = 20
    config.L3_SIZE = 8
    config.L2_SIZE = 6
    config.L1_SIZE = 4
    config.DEFAULT_NUM_ACCESSES = 15
    
    # Create a simple trace
    trace_gen = TraceGenerator()
    test_trace = trace_gen.generate_sequential_trace(start = 0, count = 10)
    
    # Create and run simulator
    sim = Simulator(trace = test_trace)
    sim.run()
    
    print("\n" + "=" * 58)
    print("SIMULATOR TEST COMPLETE")
    print("=" * 58)