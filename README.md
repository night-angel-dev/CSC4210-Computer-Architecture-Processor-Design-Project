# CSC 4210/6210 Computer Architecture - Processor Design Project

**Author:** Armando Galvan
**Course:** CSC 4210/6210 Computer Architecture
**Semester:** Spring 2026
**Instructor:** Professor Mohammed Alser


## Project Summary

This repository contains four interconnected tasks that build toward a complete processor design:

| Task | Topic                  | Deliverable                                             |
| ---- | ---------------------- | ------------------------------------------------------- |
| 1    | Data Systems           | 32-bit signed number converter with overflow/saturation |
| 2    | Boolean Logic          | Truth table to K-map simplification (SOP/POS)           |
| 3    | Memory Hierarchy       | SSD → DRAM → L3 → L2 → L1 cache simulation              |
| 4    | Single-Cycle Processor | AND/OR processor for Y = A·B + C·D                      |

The tasks reuse utilities across each other: Task 1's binary conversions are imported by Tasks 3 and 4; Task 3's clock and display utilities are reused in Task 4.

## Repository Structure

Processor Design Project/
- docs/
  - ProcessDesign - Task1.pdf
  - ProcessDesign - Task2.pdf  
  - ProcessorDesign - Task3.pdf
  - ProcessorDesign - Task4.pdf
- Task1_Data_Systems/
  - binary_utils.py
  - main.py
  - NumberSystemConverter.py
  - README.md
  - test.py
- Task2_Boolean_Logic/
  - boolean_expression.py
  - evaluator.py
  - input_handler.py
  - karnaugh_map.py
  - main.py
  - output_formatter.py
  - test.py
  - truth_table.py
- Task3_Memory_Hierarchy_Simulation/
  - cache.py
  - clock.py
  - config.py
  - cpu.py
  - dram.py
  - main.py
  - memory_display_utils.py
  - memory_level.py
  - README.md
  - simulator.py
  - ssd.py
  - test.py
  - trace.py
- Task4_Single_Cycle_Processor_Design_And_Or/
  - alu.py
  - clock.py
  - control_unit.py
  - data_memory.py
  - extend.py
  - instruction.py
  - main.py
  - mux.py
  - README.md
  - register_file.py
  - test.py
- README.md


--- 

## Task 1: Data Systems

### Overview 
Implement conversion logic and data constraints for 32-bit signed integer processor. This task established the fundamental number representation for the entired project.


### Features
 - 32-bit signed decimal input parser
- Decimal to Binary (Two's Complement) conversion
- Binary to Hexadecimal conversion
- Binary to Decimal conversion
- Overflow detection for out-of-range inputs
- Saturation logic (clamping, not wrap-around)
- Configurable output format (DEC, BIN, HEX)

### Functional Requirements
| FR  | Description                       | Status |
| --- | --------------------------------- | ------ |
| FR1 | Decimal input parser              | X      |
| FR2 | 32-bit signed integer model       | X      |
| FR3 | Internal binary representation    | X      |
| FR4 | Overflow detection                | X      |
| FR5 | Saturation (clamping)             | X      |
| FR6 | Configurable output (DEC/BIN/HEX) | X      |
| FR7 | Status output with flags          | X      |
| FR8 | Required test coverage            | X      |

### How to Run

```bash
cd Task1_Data_Systems
python main.py
```

### Test Coverage
- positive values (123)
- Zero (0)
- Negative values (-123)
- Boundary values (MAX_INT32, MIN_INT32)
- Overflow values (MAX_INT32+1, MIN_INT32-1)


### Key Takeaways
- Number systems: Decimal, Binary, Hexadecimal
- Signed arithmetic: Two's Complement
- Carry vs overflow distinction
- 32-bit bit-width limits


---

## Task 2: Boolean Logic & K Map Simplification


### Overview

Design combination logic by converting truth tables to Boolean equations and simplifying using Karnaugh Maps.


### Features
- User-specified number of input variables (n >= 2)
- Truth table input (console, file, or interactive)
- Truth table validation (2^n rows, all combination exactly once)
- SOP (Sum of Products) or POS (Product of Sums) selection
- Canonical equation generation
- Minterm/Maxterm list generation
- K-Map construction and grouping (2-4 variables)
- Simplified Boolean Expression
- Validation against original truth table

### How to Run

```bash
cd Task2_Boolean_Logic
python main.py
```

### Program Output
1. Truth table
2. Canonical equation (SOP or POS)
3. Minterm/Maxterm list
4. K-Map grouping
5. Simplified Boolean Expression
6. Validation Result (PASS/FAIL)


### Key Takeaways
- Truth table to Boolean equation conversion
- Canonical forms (SOP/POS)
- K-map minimization
- Don't-care conditions
- Logic gate optimization


---

## Task 3: Memory Hierarchy Simulation


### Overview 
Simulate a 32-bit memory hierarchy from SDD up to L1 cache, modeling how instructions travel through SSD -> DRAM -> L3 -> L2 -> L1 before reaching the CPU.


### Components
- **config.py** - Centralized configuration: memory sizes, transfer latencies, replacement policy, write policy
- **clock.py** - Cycle-accurate timer that drives the simulation
- **ssd.py** - SSD storage simulation (largest level, 1000 instructions by default)
- **dram.py** - DRAM simulation (intermediate level, 256 instructions by default)
- **cache.py** - Cache implementation with LRU, FIFO, and Random replacement policies
- **memory_level.py** - Abstract base class shared by all memory levels
- **cpu.py** - CPU interface that issues read/write requests to the hierarchy
- **simulator.py** - Orchestrates all memory levels, enforces SSD→DRAM→L3→L2→L1 flow, tracks hit/miss statistics
- **trace.py** - Generates instruction access traces (sequential, random, or loop patterns)
- **memory_display_utils.py** - Shared hex formatting utilities used across Tasks 3 and 4

### How to Run

```bash
cd Task3_Memory_Hierarchy_Simulation
python main.py
```

### Configuration
Edit `config.py` to change memory sizes (in number of instructions), transfer latencies (in clock cycles), cache replacement policy (LRU, FIFO, or Random), and write policy (write-back or write-through).

### Program Output
1. Memory hierarchy configuration (sizes and latencies)
2. Instruction access trace
3. Data movement across levels
4. Cache hit/miss statistics per level
5. Final state of each memory level

### Key Takeaways
- Memory hierarchy: SSD, DRAM, and multi-level cache
- Cache replacement policies: LRU, FIFO, Random
- Latency modeling and clock-driven simulation
- Cache hit/miss tradeoffs and bandwidth constraints


---

## Task 4: Single-Cycle Processor Design (AND / OR)


### Overview
Simulate a single-cycle 32-bit processor that evaluates the Boolean expression **Y = A · B + C' · D** using AND, OR, and NOT (via XORI) instructions. The processor follows a full Fetch → Decode → Execute → Write-back datapath in one logical cycle. It reuses binary utilities from Task 1 and the Clock and display utilities from Task 3.


### Components
- **register_file.py** - 32 × 32-bit register file with two read ports and one write port; x0 hardwired to 0
- **alu.py** - Arithmetic Logic Unit supporting AND, OR, and XOR (32-bit) with masking; imports Task 1 `binary_utils.py`
- **control_unit.py** - Decodes opcode/funct3 and generates RegWrite, ALUSrc, MemWrite, Branch, ALUControl, ImmSrc signals
- **extend.py** - Sign extension for I-type (12-bit), S-type (12-bit), and U-type (20-bit) immediates; imports Task 1 `binary_utils.py`
- **mux.py** - 2-to-1 multiplexers: ALUSrcMux, MemtoRegMux, PCSrcMux
- **instruction.py** - Instruction fetch and decode; extracts opcode, rd, funct3, rs1, rs2, funct7, and immediate fields
- **data_memory.py** - Sparse 32-bit word-addressed data memory with read/write support
- **clock.py** - Re-exports Task 3 Clock class via `importlib.util` (avoids naming conflict)
- **main.py** - `SingleCycleProcessor` class wiring all components; prompts for A, B, C, D input values

### Program Executed

```
xori x6, x3, -1     ; x6 = NOT C           (I-type: x3 XOR 0xFFFFFFFF)
and  x5, x1, x2     ; x5 = A AND B         (R-type)
and  x6, x6, x4     ; x6 = (NOT C) AND D   (R-type)
or   x7, x5, x6     ; x7 = Y               (R-type)
```

Register assignments: x1 = A, x2 = B, x3 = C, x4 = D, x7 = Y (final result).

### How to Run

```bash
cd Task4_Single_Cycle_Processor_Design_And_Or
python main.py
```

### Program Output
1. Instruction execution trace
2. Control signals per instruction
3. Register values after each instruction
4. Final output Y with pass/fail verification against reference formula

### Key Takeaways
- Single-cycle processor datapath: Fetch, Decode, Execute, Write-back
- RISC-V-style instruction encoding (R-type and I-type)
- Control unit signal generation and ALU operation selection
- NOT via XORI idiom (`xori rd, rs1, -1`)


---

## Potential Improvements

### Cross-Task Integration

The tasks share utilities but stop short of forming a true end-to-end pipeline. Below are the gaps where tighter coupling would have made the project more cohesive.

| Gap                               | What Was Done                                                                                                                                   | What Could Have Been Done                                                                                                                                                        |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task 2 → Task 4                   | Task 2 produces a simplified Boolean expression as a string; Task 4 is given the target expression Y = A·B + C'·D directly                      | Task 2's output could have been parsed to auto-generate the Task 4 instruction sequence, making simplification feed directly into execution                                      |
| Task 3 → Task 4 instruction fetch | Task 4's `InstructionMemory` uses a plain Python `dict`; Task 3's Clock and display utilities are imported but the memory hierarchy is bypassed | Routing Task 4's instruction fetch through Task 3's cache hierarchy (L1 → L2 → L3 → DRAM → SSD) would model realistic fetch latency and exercise the hit/miss logic              |
| Task 1 → Task 3                   | Task 3 treats all instructions as opaque 32-bit values and formats addresses with its own `memory_display_utils.py`                             | Task 1's `binary_to_hexadecimal` and `format_output` could have been the single source for all number formatting across Tasks 3 and 4, keeping representation logic in one place |
| Task 1 → Task 4 ALU               | Task 1 implements overflow detection and saturation clamping; the Task 4 ALU masks results to 32 bits but never raises an overflow flag         | Feeding Task 1's overflow flag out of the ALU would have connected the data constraints designed in Task 1 to actual runtime behavior in the processor                           |
| Task 2 → Task 3                   | The memory hierarchy simulation accesses instructions but never interprets them as Boolean operations                                           | Running the simplified expression from Task 2 as an actual instruction stream through the Task 3 hierarchy would have unified all four tasks into one working demo               |

### Assignment Specification Gaps

A few requirements from the task PDFs were interpreted differently or left partially addressed.

- **Task 4 - NOT encoding**: The specification (Section 1.2 and 1.4) requires NOT to be handled via an ALU input inversion flag encoded in the `funct7` field, not as a separate instruction. The implementation uses `xori rd, rs1, -1` (standard RISC-V) which is functionally correct but uses 4 instructions instead of 3 and does not implement the custom inversion control signal the rubric describes.
- **Task 2 - POS K-Map**: The assignment requires the user to be able to select SOP or POS output. SOP simplification is fully implemented via K-map 1-cell grouping, but POS simplification (grouping 0-cells on the K-map) is not, the POS canonical form is generated from maxterms but is not reduced by the K-map.
- **Task 2 - n > 4 variables**: The specification states `n ≥ 2` with no stated upper bound. The implementation caps at 4 because K-maps are impractical beyond that, but there is no fallback algorithm (e.g., Quine-McCluskey) for larger inputs.
- **Task 3 - bandwidth enforcement**: The configuration exposes a bandwidth limit (instructions per cycle) but the simulator does not enforce it during transfers - all data moves instantly within the defined latency window rather than being rate-limited per cycle.
- **Task 1 → Tasks 2/4 - saturation in computation**: Task 1's saturation logic (clamping on overflow) was designed as a processor-level constraint, but it is never applied when the ALU in Task 4 produces a result — intermediate register values can silently exceed 32-bit range before masking.

### Toward a Real Processor

The current design is a correct logical simulation but several architectural realities are absent.

- **Pipelining**: A real processor overlaps Fetch, Decode, Execute, Memory, and Write-back across multiple instructions simultaneously. Adding a 5-stage pipeline with hazard detection (data hazards, control hazards) and forwarding paths would be the most impactful single improvement.
- **Connected memory hierarchy on instruction fetch**: Instruction fetch in Task 4 reads from a dict in constant time. Routing it through the Task 3 hierarchy would make cache misses visible in the cycle count and give the clock a meaningful role in Task 4.
- **Branch and jump support**: The control unit generates a `Branch` signal and `PCSrcMux` exists, but no branch instructions are loaded. Adding BEQ and JAL would allow loops and make the processor capable of executing real programs.
- **Clock-edge register write**: `RegisterFile.write()` currently updates synchronously in the same Python call as the ALU result. A real clocked design latches writes at the rising clock edge, which matters when pipelining is added.
- **Hardware description language**: The entire project is simulated in Python. Rewriting the datapath components in VHDL or Verilog would allow synthesis to actual logic gates and FPGA deployment, making the "processor prototype" claim from the project brief literal rather than metaphorical.
- **Expanded instruction set**: The processor currently supports three opcodes (AND, OR, XORI). Adding ADD, SUB, LW, SW, and BEQ would form a minimal but complete integer ISA and allow the memory hierarchy from Task 3 to be exercised under a real workload.
