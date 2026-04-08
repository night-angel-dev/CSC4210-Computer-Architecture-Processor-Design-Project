"""
main.py - Entry point for the memory hierarchy simulation.

Parses command line arguments, creates simulator, runs simulation,
and displays results.

For 32-bit architecture:
- Simulates memory hierarchy (SSD -> DRAM -> L3 -> L2 -> L1 -> CPU)
- Tracks cache hits/misses and data movement
- Outputs statistics and final memory state
"""

import sys
import argparse
from simulator import Simulator
from trace import TraceGenerator
from memory_display_utils import MemoryDisplayUtils
import config


def parse_arguments():
    """
    Parse command line arguments.
    
    @return - Parsed arguments object
    """
    parser = argparse.ArgumentParser(
        description = "Memory Hierarchy Simulation for 32-bit Architecture"
    )
    
    parser.add_argument(
        "-t", "--trace",
        type = str,
        choices = ["sequential", "random", "loop"],
        default = "sequential",
        help = "Type of memory access trace to simulate (default: sequential)"
    )
    
    parser.add_argument(
        "-n", "--num_accesses",
        type = int,
        default = config.DEFAULT_NUM_ACCESSES,
        help = f"Number of memory accesses to simulate (default: {config.DEFAULT_NUM_ACCESSES})"
    )
    
    parser.add_argument(
        "-f", "--file",
        type = str,
        default = None,
        help = "Load trace from file (one address per line, hex or decimal)"
    )
    
    parser.add_argument(
        "-s", "--start",
        type = int,
        default = 0,
        help = "Starting address for sequential trace (default: 0)"
    )
    
    parser.add_argument(
        "--random_min",
        type = int,
        default = config.RANDOM_ADDRESS_MIN,
        help = f"Minimum address for random trace (default: {config.RANDOM_ADDRESS_MIN})"
    )
    
    parser.add_argument(
        "--random_max",
        type = int,
        default = config.RANDOM_ADDRESS_MAX,
        help = f"Maximum address for random trace (default: {config.RANDOM_ADDRESS_MAX})"
    )
    
    parser.add_argument(
        "--loop_start",
        type = int,
        default = config.LOOP_START,
        help = f"Loop start address (default: {config.LOOP_START})"
    )
    
    parser.add_argument(
        "--loop_end",
        type = int,
        default = config.LOOP_END,
        help = f"Loop end address (default: {config.LOOP_END})"
    )
    
    parser.add_argument(
        "--loop_iterations",
        type = int,
        default = config.LOOP_ITERATIONS,
        help = f"Number of loop iterations (default: {config.LOOP_ITERATIONS})"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action = "store_true",
        help = "Suppress detailed output (only show statistics)"
    )
    
    return parser.parse_args()


def generate_trace(args):
    """
    Generate trace based on command line arguments.
    
    @param args - Parsed command line arguments
    @return - List of memory addresses (byte addresses, multiples of 4)
    """
    trace_gen = TraceGenerator()
    trace = None
    
    # Load from file if specified
    if args.file:
        print(f"Loading trace from file: {args.file}")
        trace = trace_gen.generate_trace_from_file(args.file)
    
    # Generate based on trace type
    elif args.trace == "sequential":
        trace = trace_gen.generate_sequential_trace(
            start = args.start,
            count = args.num_accesses
        )
    
    elif args.trace == "random":
        trace = trace_gen.generate_random_trace(
            num_accesses = args.num_accesses,
            address_range = (args.random_min, args.random_max)
        )
    
    elif args.trace == "loop":
        trace = trace_gen.generate_loop_trace(
            loop_start = args.loop_start,
            loop_end = args.loop_end,
            iterations = args.loop_iterations
        )
    
    return trace


def main():
    """
    Main entry point for the memory hierarchy simulation.
    """
    print("=" * 58)
    print("32-BIT MEMORY HIERARCHY SIMULATOR")
    print("=" * 58)
    print("Architecture: 32-bit (4-byte instructions)")
    print("Hierarchy: SSD -> DRAM -> L3 -> L2 -> L1 -> CPU")
    print("=" * 58)
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Generate trace
    trace = generate_trace(args)
    
    if not trace:
        print("Error: No trace generated. Please check your inputs.")
        sys.exit(1)
    
    # Override config quiet mode if specified
    if args.quiet:
        config.VERBOSE = False
        config.SHOW_DATA_MOVEMENT = False
    
    # Create and run simulator
    sim = Simulator(trace = trace)
    
    # Override config print in simulator if quiet mode
    if args.quiet:
        # Temporarily redirect or just let it run
        pass
    
    sim.run()
    
    # Print summary
    print("\n" + "=" * 58)
    print("SIMULATION SUMMARY")
    print("=" * 58)
    print(f"Trace Type:      {args.trace}")
    print(f"Total Accesses:  {len(trace)}")
    print(f"Total Cycles:    {sim.get_total_cycles()}")
    print(f"L1 Hit Rate:     {sim.get_hit_rate('L1'):.1%}")
    print(f"L2 Hit Rate:     {sim.get_hit_rate('L2'):.1%}")
    print(f"L3 Hit Rate:     {sim.get_hit_rate('L3'):.1%}")
    print("=" * 58)


if __name__ == "__main__":
    main()