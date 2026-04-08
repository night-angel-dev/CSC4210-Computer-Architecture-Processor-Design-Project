"""
memory_display_utils.py - Display utilities for memory hierarchy simulation.
Leverages NumberSystemConverter from Task 1 for consistent output formatting.
"""

import sys
import os

# Get the directory of current file 
current_dir = os.path.dirname(os.path.abspath(__file__))

# Goes up one level and into Task 1 folder
task1_path = os.path.join(current_dir, "..", "Task1_Data_Systems")

# Add to path
if task1_path not in sys.path:
    sys.path.insert(0, task1_path)

try:
    from NumberSystemConverter import NumberSystemConverter
    # print("Import is a success")
    
except ImportError as e:
    print(f"Import from Task1 failed: {e}")



class MemoryDisplayUtils:
    """
    Utility class for formatting memory addresses and contents.
    Uses the 32-bit conversion logic from Task 1.
    """
    
    def __init__(self):
        self.converter = NumberSystemConverter()
    
    def format_address(self, address_int, format_type = "HEX"):
        """
        Format a memory address for display.
        
        Addresses are typically shown in hex.
        
        @param address_int - Integer address (0 to 0xFFFFFFFF)
        @param format_type - "DEC", "BIN", or "HEX"
        @return - Formatted address string
        """
        if format_type == "HEX":
            # Convert to 32-bit binary first, then to hex
            binary = self.converter.decimal_to_padded_binary(address_int)
            return self.converter.binary_to_hexadecimal(binary)
        
        elif format_type == "BIN":
            return self.converter.decimal_to_padded_binary(address_int)
        
        else:
            return str(address_int)
    
    def format_instruction(self, instruction_int, format_type = "HEX"):
        """
        Format a 32-bit instruction for display.
        
        @param instruction_int - 32-bit instruction value (0 to 0xFFFFFFFF)
        @param format_type - "DEC", "BIN", or "HEX"
        @return - Formatted instruction string
        """
        return self.format_address(instruction_int, format_type)
    
    def format_cache_line(self, tag, index, offset, format_type = "HEX"):
        """
        Format cache line components for educational output.
        
        @param tag - Cache tag bits
        @param index - Cache index bits
        @param offset - Offset within cache line
        @param format_type - Output format ("DEC", "BIN", or "HEX")
        @return - Formatted cache line identifier
        """
        combined = (tag << 16) | (index << 4) | offset # Simplified
        return self.format_address(combined, format_type)
    
    def print_memory_snapshot(self, level_name, storage_dict, max_items = 20):
        """
        Print a snapshot of memory contents at a specific level.
        
        @param level_name - Name of memory level (L1, L2, DRAM, etc.)
        @param storage_dict - Dictionary of address -> data
        @param max_items - Maximum number of items to display
        @return - None
        """
        print(f"\n{level_name} Contents ({len(storage_dict)} instructions):")
        
        items = list(storage_dict.items())
        if len(items) > max_items:
            items = items[:max_items]
            print(f"  (showing first {max_items} of {len(storage_dict)})")
        
        for addr, data in items:
            addr_str = self.format_address(addr, "HEX")
            data_str = self.format_instruction(data, "HEX")
            print(f"  {addr_str}: {data_str}")
    
    def print_transfer_log(self, from_level, to_level, address, cycle, latency):
        """
        Print a formatted data transfer log entry.
        
        @param from_level - Source memory level name
        @param to_level - Destination memory level name
        @param address - Address being transferred
        @param cycle - Current clock cycle
        @param latency - Transfer latency in cycles
        @return - None
        """
        addr_str = self.format_address(address, "HEX")
        print(f"Cycle {cycle:4d}: {from_level:4s} -> {to_level:4s} (address {addr_str}, latency {latency} cycles)")
    
    def print_hit_miss_log(self, level_name, address, is_hit, cycle):
        """
        Print a formatted cache hit/miss log entry.
        
        @param level_name - Memory level name (L1, L2, L3)
        @param address - Address being accessed
        @param is_hit - True if hit, False if miss
        @param cycle - Current clock cycle
        @return - None
        """
        addr_str = self.format_address(address, "HEX")
        result = "HIT" if is_hit else "MISS"
        print(f"Cycle {cycle:4d}: {level_name:4s} access at {addr_str} -> {result}")
    
    def print_config_summary(self, config_dict):
        """
        Print a summary of memory hierarchy configuration.
        
        @param config_dict - Dictionary containing configuration parameters
        @return - None
        """
        print("\n" + "=" * 58)
        print("MEMORY HIERARCHY CONFIGURATION")
        print("=" * 58)
        print(f"SSD:      {config_dict['SSD_SIZE']:4d} instructions, Latency: {config_dict['SSD_TO_DRAM_LATENCY']:3d} cycles")
        print(f"DRAM:     {config_dict['DRAM_SIZE']:4d} instructions, Latency: {config_dict['DRAM_TO_L3_LATENCY']:3d} cycles")
        print(f"L3 Cache: {config_dict['L3_SIZE']:4d} instructions, Latency: {config_dict['L3_TO_L2_LATENCY']:3d} cycles")
        print(f"L2 Cache: {config_dict['L2_SIZE']:4d} instructions, Latency: {config_dict['L2_TO_L1_LATENCY']:3d} cycles")
        print(f"L1 Cache: {config_dict['L1_SIZE']:4d} instructions, Latency: {config_dict['L1_ACCESS_LATENCY']:3d} cycle")
        print(f"\nBandwidth:        {config_dict['BANDWIDTH'] if config_dict['BANDWIDTH'] else 'Unlimited'} instruction(s)/cycle")
        print(f"Replacement Policy: {config_dict['REPLACEMENT_POLICY']}")
        print(f"Write Policy:       {config_dict['WRITE_POLICY']}")
        print("=" * 58 + "\n")
    
    def hex_to_int(self, hex_str):
        """
        Convert a hexadecimal string to a 32-bit integer.
        
        @param hex_str - Hexadecimal string (with or without 0x prefix)
        @return - Integer representation
        """
        # Remove 0x prefix if present
        clean_hex = hex_str.replace('0x', '').replace('0X', '')
        return int(clean_hex, 16)
    
    def int_to_hex(self, value, pad_to=8):
        """
        Convert a 32-bit integer to a hexadecimal string.
        
        @param value - Integer value
        @param pad_to - Number of hex digits to pad to (default 8 for 32-bit)
        @return - Hexadecimal string with 0x prefix
        """
        return f"0x{value & 0xFFFFFFFF:0{pad_to}X}"


# For testing the display utilities
if __name__ == "__main__":
    """
    Simple test to verify the display utilities work correctly.
    """
    display = MemoryDisplayUtils()
    
    # Test format_address
    print("Testing format_address:")
    print(f"  Address 0 in HEX: {display.format_address(0, 'HEX')}")
    print(f"  Address 42 in HEX: {display.format_address(42, 'HEX')}")
    print(f"  Address 0xFFFFFFFF in HEX: {display.format_address(0xFFFFFFFF, 'HEX')}")
    print(f"  Address 42 in BIN: {display.format_address(42, 'BIN')}")
    print(f"  Address 42 in DEC: {display.format_address(42, 'DEC')}")
    
    # Test format_instruction
    print("\nTesting format_instruction:")
    print(f"  Instruction 0x12345678: {display.format_instruction(0x12345678, 'HEX')}")
    
    # Test hex conversion
    print("\nTesting hex conversion:")
    print(f"  hex_to_int('0x100'): {display.hex_to_int('0x100')}")
    print(f"  int_to_hex(256): {display.int_to_hex(256)}")
    
    # Test print_transfer_log
    print("\nTesting print_transfer_log:")
    display.print_transfer_log("SSD", "DRAM", 42, 0, 100)
    
    # Test print_hit_miss_log
    print("\nTesting print_hit_miss_log:")
    display.print_hit_miss_log("L1", 42, True, 116)
    display.print_hit_miss_log("L1", 100, False, 117)