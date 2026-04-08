# Memory Hierarchy Simulation

## Overview
This project simulates a 32-bit memory hierarchy from SSD up to L1 cache. It models how instructions travel through SSD -> DRAM -> L3 -> L2 -> L1 before reaching the CPU.

## Requirements
- Python 3.7 or higher
- No external dependencies (uses only standard library)

## Setup
1. Clone the repository
2. Ensure all .py files are in the same directory
3. Run `python main.py` to start the simulation

## Configuration
Edit `config.py` to change:
- Memory sizes (SSD_SIZE, DRAM_SIZE, L1_SIZE, etc.)
- Transfer latencies (in clock cycles)
- Cache replacement policy (LRU, FIFO, or Random)

## Usage

`python main.py`



## Example Output
==========================================================
32-BIT MEMORY HIERARCHY SIMULATOR
==========================================================
Architecture: 32-bit (4-byte instructions)
Hierarchy: SSD -> DRAM -> L3 -> L2 -> L1 -> CPU
==========================================================
SSD: Loaded 1000 instructions (byte addresses 0 to 3996)
==========================================================
MEMORY HIERARCHY SIMULATION
==========================================================

==========================================================
MEMORY HIERARCHY CONFIGURATION
==========================================================
SSD:      1000 instructions, Latency: 100 cycles
DRAM:      256 instructions, Latency:  50 cycles
L3 Cache:   64 instructions, Latency:  10 cycles
L2 Cache:   32 instructions, Latency:   5 cycles
L1 Cache:   16 instructions, Latency:   1 cycle

Bandwidth:        1 instruction(s)/cycle
Replacement Policy: LRU
Write Policy:       write_back
==========================================================

INSTRUCTION ACCESS TRACE
----------------------------------------------------------

Trace (50 accesses):
  Access   1: 0x00000000
  Access   2: 0x00000004
  Access   3: 0x00000008
  Access   4: 0x0000000C
  Access   5: 0x00000010
  Access   6: 0x00000014
  Access   7: 0x00000018
  Access   8: 0x0000001C
  Access   9: 0x00000020
  Access  10: 0x00000024
  Access  11: 0x00000028
  Access  12: 0x0000002C
  Access  13: 0x00000030
  Access  14: 0x00000034
  Access  15: 0x00000038
  Access  16: 0x0000003C
  Access  17: 0x00000040
  Access  18: 0x00000044
  Access  19: 0x00000048
  Access  20: 0x0000004C
  ... and 30 more accesses

==========================================================
EXECUTING ACCESSES
==========================================================

Access 1: READ address 0x00000000
  Retrieved instruction: 0x10000000

Access 2: READ address 0x00000004
  Retrieved instruction: 0x10000004

Access 3: READ address 0x00000008
  Retrieved instruction: 0x10000008

Access 4: READ address 0x0000000C
  Retrieved instruction: 0x1000000C

Access 5: READ address 0x00000010
  Retrieved instruction: 0x10000010

Access 6: READ address 0x00000014
  Retrieved instruction: 0x10000014

Access 7: READ address 0x00000018
  Retrieved instruction: 0x10000018

Access 8: READ address 0x0000001C
  Retrieved instruction: 0x1000001C

Access 9: READ address 0x00000020
  Retrieved instruction: 0x10000020

Access 10: READ address 0x00000024
  Retrieved instruction: 0x10000024

Access 11: READ address 0x00000028
  Retrieved instruction: 0x10000028

Access 12: READ address 0x0000002C
  Retrieved instruction: 0x1000002C

Access 13: READ address 0x00000030
  Retrieved instruction: 0x10000030

Access 14: READ address 0x00000034
  Retrieved instruction: 0x10000034

Access 15: READ address 0x00000038
  Retrieved instruction: 0x10000038

Access 16: READ address 0x0000003C
  Retrieved instruction: 0x1000003C

Access 17: READ address 0x00000040
  Retrieved instruction: 0x10000040

Access 18: READ address 0x00000044
  Retrieved instruction: 0x10000044

Access 19: READ address 0x00000048
  Retrieved instruction: 0x10000048

Access 20: READ address 0x0000004C
  Retrieved instruction: 0x1000004C

Access 21: READ address 0x00000050
  Retrieved instruction: 0x10000050

Access 22: READ address 0x00000054
  Retrieved instruction: 0x10000054

Access 23: READ address 0x00000058
  Retrieved instruction: 0x10000058

Access 24: READ address 0x0000005C
  Retrieved instruction: 0x1000005C

Access 25: READ address 0x00000060
  Retrieved instruction: 0x10000060

Access 26: READ address 0x00000064
  Retrieved instruction: 0x10000064

Access 27: READ address 0x00000068
  Retrieved instruction: 0x10000068

Access 28: READ address 0x0000006C
  Retrieved instruction: 0x1000006C

Access 29: READ address 0x00000070
  Retrieved instruction: 0x10000070

Access 30: READ address 0x00000074
  Retrieved instruction: 0x10000074

Access 31: READ address 0x00000078
  Retrieved instruction: 0x10000078

Access 32: READ address 0x0000007C
  Retrieved instruction: 0x1000007C

Access 33: READ address 0x00000080
  Retrieved instruction: 0x10000080

Access 34: READ address 0x00000084
  Retrieved instruction: 0x10000084

Access 35: READ address 0x00000088
  Retrieved instruction: 0x10000088

Access 36: READ address 0x0000008C
  Retrieved instruction: 0x1000008C

Access 37: READ address 0x00000090
  Retrieved instruction: 0x10000090

Access 38: READ address 0x00000094
  Retrieved instruction: 0x10000094

Access 39: READ address 0x00000098
  Retrieved instruction: 0x10000098

Access 40: READ address 0x0000009C
  Retrieved instruction: 0x1000009C

Access 41: READ address 0x000000A0
  Retrieved instruction: 0x100000A0

Access 42: READ address 0x000000A4
  Retrieved instruction: 0x100000A4

Access 43: READ address 0x000000A8
  Retrieved instruction: 0x100000A8

Access 44: READ address 0x000000AC
  Retrieved instruction: 0x100000AC

Access 45: READ address 0x000000B0
  Retrieved instruction: 0x100000B0

Access 46: READ address 0x000000B4
  Retrieved instruction: 0x100000B4

Access 47: READ address 0x000000B8
  Retrieved instruction: 0x100000B8

Access 48: READ address 0x000000BC
  Retrieved instruction: 0x100000BC

Access 49: READ address 0x000000C0
  Retrieved instruction: 0x100000C0

Access 50: READ address 0x000000C4
  Retrieved instruction: 0x100000C4

==========================================================
SIMULATION RESULTS
==========================================================

CACHE STATISTICS
----------------------------------------------------------
L1: Hits=0, Misses=50, Hit Rate=0.0%
L2: Hits=0, Misses=50, Hit Rate=0.0%
L3: Hits=0, Misses=50, Hit Rate=0.0%

DRAM STATISTICS
----------------------------------------------------------
DRAM: Accesses=50, Hits=0, Hit Rate=0.0%

SSD STATISTICS
----------------------------------------------------------
SSD: Accesses=50, Hit Rate=100.0%

CPU STATISTICS
----------------------------------------------------------
Instructions Executed: 0
Total Reads: 50
Total Writes: 0
Total Cycles: 50

==========================================================
FINAL MEMORY STATE
==========================================================

L1 Cache Contents (16 instructions):
  (showing first 10 of 16)
  0x00000088: 0x10000088
  0x0000008C: 0x1000008C
  0x00000090: 0x10000090
  0x00000094: 0x10000094
  0x00000098: 0x10000098
  0x0000009C: 0x1000009C
  0x000000A0: 0x100000A0
  0x000000A4: 0x100000A4
  0x000000A8: 0x100000A8
  0x000000AC: 0x100000AC

L2 Cache Contents (32 instructions):
  (showing first 10 of 32)
  0x00000048: 0x10000048
  0x0000004C: 0x1000004C
  0x00000050: 0x10000050
  0x00000054: 0x10000054
  0x00000058: 0x10000058
  0x0000005C: 0x1000005C
  0x00000060: 0x10000060
  0x00000064: 0x10000064
  0x00000068: 0x10000068
  0x0000006C: 0x1000006C

L3 Cache Contents (50 instructions):
  (showing first 10 of 50)
  0x00000000: 0x10000000
  0x00000004: 0x10000004
  0x00000008: 0x10000008
  0x0000000C: 0x1000000C
  0x00000010: 0x10000010
  0x00000014: 0x10000014
  0x00000018: 0x10000018
  0x0000001C: 0x1000001C
  0x00000020: 0x10000020
  0x00000024: 0x10000024

DRAM Contents (50 instructions):
  (showing first 10 of 50)
  0x00000000: 0x10000000
  0x00000004: 0x10000004
  0x00000008: 0x10000008
  0x0000000C: 0x1000000C
  0x00000010: 0x10000010
  0x00000014: 0x10000014
  0x00000018: 0x10000018
  0x0000001C: 0x1000001C
  0x00000020: 0x10000020
  0x00000024: 0x10000024

SSD Contents (1000 instructions):
  (showing first 10 of 1000)
  0x00000000: 0x10000000
  0x00000001: 0x10000004
  0x00000002: 0x10000008
  0x00000003: 0x1000000C
  0x00000004: 0x10000010
  0x00000005: 0x10000014
  0x00000006: 0x10000018
  0x00000007: 0x1000001C
  0x00000008: 0x10000020
  0x00000009: 0x10000024

==========================================================
SIMULATION SUMMARY
==========================================================
Trace Type:      sequential
Total Accesses:  50
Total Cycles:    50
L1 Hit Rate:     0.0%
L2 Hit Rate:     0.0%
L3 Hit Rate:     0.0%
==========================================================
