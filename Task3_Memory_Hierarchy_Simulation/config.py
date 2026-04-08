"""
config.py - A central place to store all configurable parameters.
"""


# MEMORY SIZES (in number of instructions)
# Hierarchy rule: SSD_SIZE > DRAM_SIZE > L3_SIZE > L2_SIZE > L1_SIZE
# Ratios represent real systems where each level is 2-10 times largers than the level above 
SSD_SIZE = 1000 # Largest storage - holds all instructions (4KB)
DRAM_SIZE = 256 # Main memory - intermediate size (4 * L3 = 1KB)
L3_SIZE = 64    # L3 cache - shared cache (2 * L2 = 256 bytes)
L2_SIZE = 32    # L2 cache - per-core cache (2 * L1 = 128 bytes)
L1_SIZE = 16    # L1 cache - closest to CPU, smallest (64 bytes) 


# LATENCIES (in clock cycles)
# Time taken for data to move between adjacent levels
SSD_TO_DRAM_LATENCY = 100 # Slowest - SSD to DRAM transfer (100,000+ cycles, simplified to 100 for ease of simulation)
DRAM_TO_L3_LATENCY = 50   # DRAM to L3 cache transfer (50-100 cycles)
L3_TO_L2_LATENCY = 10     # L3 to L2 cache transfer (10-20 cycles)
L2_TO_L1_LATENCY = 5      # L2 to L1 cache transfer (5-15 cycles)
L1_ACCESS_LATENCY = 1     # L1 cache access time (CPU to L1) (1-3 cycles)


# BANDWIDTH LIMITS
# Maximum number of instructions that can be transferred per clock cycle
# Set to None for unlimited bandwidth, or a positive integer to limit
BANDWIDTH = 1  # 1 instruction per cycle 


# CACHE REPLACEMENT POLICY
# Options: "LRU" (Least Recently Used), "FIFO" (First In First Out), "Random"
REPLACEMENT_POLICY = "LRU" # Default policy for all cache levels

# SIMULATION SETTINGS
VERBOSE = True            # Print detailed logs during simulation
SHOW_DATA_MOVEMENT = True # Log data transfers between levels
SHOW_CACHE_STATS = True   # Display cache hit/miss statistics

# ADDRESS SPACE
MIN_ADDRESS = 0
MAX_ADDRESS = SSD_SIZE - 1 # Valid addresses: 0 to SSD_SIZE-1

# TRACE GENERATION DEFAULTS
DEFAULT_TRACE_TYPE = "sequential" # Options: "sequential", "random", "loop"
DEFAULT_NUM_ACCESSES = 50         # Number of memory accesses to simulate
DEFAULT_SEQUENTIAL_START = 0      # Starting address for sequential trace

# For random trace generation
RANDOM_ADDRESS_MIN = 0
RANDOM_ADDRESS_MAX = SSD_SIZE - 1

# For loop trace generation
LOOP_START = 0
LOOP_END = 10
LOOP_ITERATIONS = 5


# WRITE POLICY (for future expansion)

# "write_through": Write to cache AND lower level immediately
# "write_back": Write only to cache, mark dirty, write back on eviction
WRITE_POLICY = "write_back" # More efficient, realistic for modern CPUs


# VALIDATION FUNCTION
def validate_config():
    """
    Validate that configuration parameters follow hierarchy rules.
    Returns True if valid, raises ValueError if invalid.
    """
    errors = []
    
    # Check hierarchy size rule: SSD > DRAM > L3 > L2 > L1
    if not (SSD_SIZE > DRAM_SIZE > L3_SIZE > L2_SIZE > L1_SIZE):
        errors.append(
            f"Size hierarchy violation: "
            f"SSD({SSD_SIZE}) > DRAM({DRAM_SIZE}) > L3({L3_SIZE}) > "
            f"L2({L2_SIZE}) > L1({L1_SIZE}) must be True"
        )
    
    # Check all sizes are positive
    if SSD_SIZE <= 0:
        errors.append(f"SSD_SIZE must be positive, got {SSD_SIZE}")
    if DRAM_SIZE <= 0:
        errors.append(f"DRAM_SIZE must be positive, got {DRAM_SIZE}")
    if L3_SIZE <= 0:
        errors.append(f"L3_SIZE must be positive, got {L3_SIZE}")
    if L2_SIZE <= 0:
        errors.append(f"L2_SIZE must be positive, got {L2_SIZE}")
    if L1_SIZE <= 0:
        errors.append(f"L1_SIZE must be positive, got {L1_SIZE}")
    
    # Check latencies are non-negative
    latencies = [
        ("SSD_TO_DRAM_LATENCY", SSD_TO_DRAM_LATENCY),
        ("DRAM_TO_L3_LATENCY", DRAM_TO_L3_LATENCY),
        ("L3_TO_L2_LATENCY", L3_TO_L2_LATENCY),
        ("L2_TO_L1_LATENCY", L2_TO_L1_LATENCY),
    ]
    for name, value in latencies:
        if value < 0:
            errors.append(f"{name} must be >= 0, got {value}")
    
    # Check bandwidth
    if BANDWIDTH is not None and BANDWIDTH <= 0:
        errors.append(f"BANDWIDTH must be > 0 or None, got {BANDWIDTH}")
    
    # Check replacement policy
    valid_policies = ["LRU", "FIFO", "Random"]
    if REPLACEMENT_POLICY not in valid_policies:
        errors.append(
            f"REPLACEMENT_POLICY must be one of {valid_policies}, "
            f"got {REPLACEMENT_POLICY}"
        )
    
    if errors:
        raise ValueError("Configuration validation failed:\n  - " + "\n  - ".join(errors))
    
    return True


# CONFIGURATION DISPLAY FUNCTION
def print_config():
    """Print current configuration in a formatted way."""
    print("\n" + "=" * 58)
    print("MEMORY HIERARCHY CONFIGURATION")
    print("=" * 58)
    print(f"SSD:      {SSD_SIZE:4d} instructions, Latency: {SSD_TO_DRAM_LATENCY:3d} cycles")
    print(f"DRAM:     {DRAM_SIZE:4d} instructions, Latency: {DRAM_TO_L3_LATENCY:3d} cycles")
    print(f"L3 Cache: {L3_SIZE:4d} instructions, Latency: {L3_TO_L2_LATENCY:3d} cycles")
    print(f"L2 Cache: {L2_SIZE:4d} instructions, Latency: {L2_TO_L1_LATENCY:3d} cycles")
    print(f"L1 Cache: {L1_SIZE:4d} instructions, Latency: {L1_ACCESS_LATENCY:3d} cycle")
    print(f"\nBandwidth:        {BANDWIDTH if BANDWIDTH else 'Unlimited'} instruction(s)/cycle")
    print(f"Replacement Policy: {REPLACEMENT_POLICY}")
    print(f"Write Policy:       {WRITE_POLICY}")
    print("=" * 58 + "\n")


# Auto-validate when module is imported
if __name__ == "__main__":
    # Test the configuration
    try:
        validate_config()
        print("Configuration validation PASSED")
        print_config()
    except ValueError as e:
        print(f"Configuration validation FAILED")
        print(e)