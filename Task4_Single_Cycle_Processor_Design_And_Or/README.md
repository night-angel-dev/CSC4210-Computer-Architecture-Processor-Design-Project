# Task 4 — Single-Cycle Processor Design (AND / OR)

**Name:** Armando Galvan
**Course:** CSC 4210/6210 Computer Architecture
**Semester:** Spring 2026
**Due Date:** April 24, 2026
---

## Overview

This project implements a single-cycle 32-bit processor simulation in Python that evaluates the Boolean expression **Y = A·B + C'·D** (AND, OR, and NOT operations). The processor simulates a full datapath - instruction fetch, decode, execute, and write-back - in a single logical cycle. It builds directly on utilities developed in Tasks 1 through 3: binary manipulation functions from Task 1, and the Clock and memory display utilities from Task 3. The NOT operation is achieved using the standard RISC-V idiom `xori rd, rs1, -1`, which XORs a register with `0xFFFFFFFF` to produce the bitwise complement.

---

## Functional Requirements

| Requirement        | Description                                                                             | Status      |
| ------------------ | --------------------------------------------------------------------------------------- | ----------- |
| AND instruction    | R-type, opcode 0x33, funct3 0x7                                                         | Implemented |
| OR instruction     | R-type, opcode 0x33, funct3 0x6                                                         | Implemented |
| NOT via XORI       | I-type, opcode 0x13, funct3 0x4, imm=-1                                                 | Implemented |
| Register file      | 32x32-bit registers, two read ports, one write port, x0 hardwired to 0                  | Implemented |
| ALU                | Supports AND, OR, XOR (32-bit, with masking)                                            | Implemented |
| Control unit       | Decodes opcode/funct3, generates RegWrite, ALUSrc, MemWrite, Branch, ALUControl, ImmSrc | Implemented |
| Sign extend        | I-type (12-bit), S-type (12-bit assembled), U-type (20-bit shift)                       | Implemented |
| Multiplexers       | ALUSrcMux, MemtoRegMux, PCSrcMux                                                        | Implemented |
| Data memory        | Sparse 32-bit word-addressed read/write                                                 | Implemented |
| Clock              | Re-exports Task 3 Clock via importlib                                                   | Implemented |
| Instruction memory | Sparse dict, byte-addressed, PC increments by 4                                         | Implemented |
| Program trace      | Per-instruction: fields, control signals, register state                                | Implemented |
| Verification       | Result compared to Python reference formula                                             | Implemented |
| Test suite         | 16 boolean truth table + 8 32-bit integer cases, all pass                               | Implemented |


---

## Program Executed

The processor runs the following 4-instruction program to evaluate Y = A·B + C'·D:

```
xori x6, x3, -1     ; x6 = NOT C           (I-type: x3 XOR 0xFFFFFFFF)
and  x5, x1, x2     ; x5 = A AND B         (R-type)
and  x6, x6, x4     ; x6 = (NOT C) AND D   (R-type)
or   x7, x5, x6     ; x7 = Y               (R-type)
```

Register assignments: x1 = A, x2 = B, x3 = C, x4 = D, x5 = t0 (A·B), x6 = t1 (C'·D), x7 = Y (final result).

---

## How to Run

### Prerequisites

- Python 3.8 or higher
- No external packages required

### Running the Processor Simulation

```bash
cd Task4_Single_Cycle_Processor_Design_And_Or
python main.py
```

You will be prompted to enter integer values for A, B, C, and D (press Enter to use the default value of 1). The simulation will print an instruction execution trace, control signals for each instruction, register values after each step, and the final result Y with a pass/fail verification against the expected formula.

**Example:**

```
Enter A (x1): 1
Enter B (x2): 1
Enter C (x3): 1
Enter D (x4): 0
```

Expected: Y = (1 AND 1) OR (NOT 1 AND 0) = 1 OR 0 = 1

### Running the Test Suite

```bash
cd Task4_Single_Cycle_Processor_Design_And_Or
python test.py
```

This runs all 24 test cases silently (simulation trace suppressed) and prints only PASS/FAIL results. It covers all 16 boolean input combinations (the full truth table for A, B, C, D in {0, 1}) and 8 additional 32-bit integer edge cases including all-zeros, all-ones, alternating bit patterns, and masking scenarios.

---

## Program Description

### Summary

This Task 4 implementation simulates a single-cycle 32-bit RISC-V-style processor in Python. Each component of the processor datapath is implemented as a separate file, and the simulation wires them together in `main.py` to evaluate the Boolean expression Y = A·B + C'·D using four machine instructions per computation. The processor correctly handles all 32-bit input combinations and integrates binary utilities from Task 1 and memory/clock infrastructure from Task 3.

### Instruction Set and NOT Operation

The processor supports AND and OR as standard R-type instructions (opcode `0x33`) differentiated by `funct3`: `0x7` for AND and `0x6` for OR. The NOT operation, required for computing C', is implemented using the standard RISC-V `XORI` instruction (I-type, opcode `0x13`, funct3 `0x4`). `xori rd, rs1, -1` XORs the source register with the 12-bit immediate value -1, which sign-extends to `0xFFFFFFFF`, flipping all 32 bits. This produces a bitwise complement without needing a dedicated NOT opcode. The `extend.py` component, which draws on Task 1's `decimal_to_padded_binary` and `binary_to_decimal` functions, handles sign-extending the 12-bit immediate field to 32 bits before it reaches the ALU.

### Datapath Components

The datapath follows the standard single-cycle model. On each cycle, `main.py`'s `SingleCycleProcessor` orchestrates: (1) **Fetch** — `InstructionMemory.fetch(pc)` retrieves the 32-bit instruction word at the current PC; (2) **Decode** — `ControlUnit.decode(instruction)` reads the opcode and funct3 fields to generate control signals, `RegisterFile.read(rs1, rs2)` returns the two source operand values, and `SignExtend.extend_i_type()` sign-extends the immediate for I-type instructions; (3) **Execute** — `ALUSrcMux.select_src_b()` selects between the register value and the sign-extended immediate as the second ALU input, then `ALU.operate()` performs AND, OR, or XOR; (4) **Write-back** - `MemtoRegMux.select_write_back()` selects the write-back source and `RegisterFile.write(rd, result, we)` commits the result. The PC is then incremented by 4 for the next sequential instruction.

### Control Unit and Signal Generation

The `ControlUnit` decodes the instruction opcode and funct3 to produce a set of 1-bit and multi-bit control signals. `ALUControl` is a 3-bit internal code (ADD=000, SUB=001, AND=010, OR=011, XOR=100) that is translated to the string-based interface `alu.py` expects via `get_alu_op_string()`. `ALUSrc` selects between register file output RD2 and the sign-extended immediate as the second ALU operand, this is 1 for I-type instructions, and 0 for R-type. `RegWrite` enables the register file write port. The `Branch` signal represents branch intent; the actual next-PC decision `PCSrc = Branch AND ALU.zero` is computed by `compute_pc_src(alu_zero)`, modeling the AND gate that lives in the datapath rather than the control unit. For the current program (no branch instructions), Branch is always 0.

### Cross-Task Integration

Task 4 is explicitly connected to the earlier tasks. `alu.py` and `extend.py` both import from Task 1's `binary_utils.py`, `invert_bits`, `mask_to_32bits`, `decimal_to_padded_binary`, and `binary_to_decimal`, to perform bit-level operations consistently across the project. `register_file.py`, `instruction.py`, `control_unit.py`, and `data_memory.py` all import `MemoryDisplayUtils` from Task 3 for uniform hex formatting of addresses and values. The `Clock` component in Task 4 is Task 3's `Clock` class, loaded by absolute file path via Python's `importlib.util` to avoid a naming conflict (both files are called `clock.py`). This architectural layering ensures that numerical representation, memory formatting, and timing all use shared, tested infrastructure rather than duplicated code.

---

## Repository Structure

### **clock.py** - Re-exports Task 3 Clock
- Loads `Task3_Memory_Hierarchy_Simulation/clock.py` by absolute path via `importlib.util` to avoid a module naming conflict
- `Clock` — re-exported class; tracks cycle count and elapsed time

### **register_file.py** - 32x32-bit register file
- `class RegisterFile`
  - `__init__()` - Initializes 32 registers to 0; x0 permanently hardwired to 0
  - `read(a1, a2)` - Returns (RD1, RD2) from ports A1 and A2
  - `write(a3, wd3, we3)` - Writes WD3 to register A3 when WE3=1; ignores writes to x0
  - `get_register(addr)` - Returns value of a single register by address
  - `set_register(addr, value)` - Directly sets a register (used to load A, B, C, D inputs)
  - `dump_registers()` - Prints all non-zero register values for debugging
  - `reset()` - Clears all registers back to 0

### **alu.py** - Arithmetic Logic Unit
- `class ALU`
  - `__init__()` - Initializes result and zero flag to 0
  - `operate(src_a, src_b, alu_op, invert_a, invert_b)` - Performs AND, OR, or XOR on 32-bit inputs; masks result to 32 bits; sets zero flag
  - `get_result()` - Returns the last computed ALUResult
  - `get_zero_flag()` - Returns 1 if last result was 0, else 0
  - `reset()` - Clears result and zero flag

### **extend.py** - Sign Extension Unit
- `class SignExtend`
  - `__init__()` - Initializes extended value to 0
  - `extend_i_type(imm12)` - Sign-extends 12-bit I-type immediate to 32 bits using Task 1 binary_utils
  - `extend_s_type(imm12)` - Sign-extends 12-bit S-type immediate (assembled from rd and imm fields) to 32 bits
  - `extend_u_type(imm20)` - Zero-extends 20-bit U-type immediate shifted left 12 to 32 bits
  - `extend(imm, imm_type)` - Dispatcher: routes to the correct extend method by ImmSrc code
  - `get_extend()` - Returns the last sign-extended value
  - `reset()` - Clears extended value

### **instruction.py** - Instruction Fetch and Decode
- `class Instruction`
  - `__init__(instruction_bits)` - Extracts opcode, rd, funct3, rs1, rs2, funct7, imm_i from a 32-bit word
  - `is_r_type()` - Returns True if opcode is 0x33 (AND, OR)
  - `is_i_type()` - Returns True if opcode is 0x13 (XORI)
  - `get_alu_op()` - Returns "AND", "OR", or "XOR" based on funct3
  - `get_imm_i()` - Returns the raw 12-bit I-type immediate for sign extension
  - `get_rs1_value(register_file)` - Reads RD1 from the register file via rs1
  - `get_rs2_value(register_file)` - Reads RD2 from the register file via rs2
  - `get_destination()` - Returns rd (destination register address)
  - `get_instruction_name()` - Returns human-readable name: "AND", "OR", "XORI"
  - `print_fields()` - Prints all decoded fields for trace output
- `class InstructionMemory`
  - `__init__()` - Initializes sparse dict storage and PC to 0
  - `load_program(instructions)` - Stores list of 32-bit words at byte addresses 0, 4, 8, ... so on
  - `fetch(pc)` - Returns an Instruction object at the given byte address, or None if out of range
  - `get_pc()` / `set_pc(pc)` / `increment_pc()` / `reset()` - PC management
  - `get_program_size()` - Returns number of loaded instructions

### **control_unit.py** - Control Signal Generator
- `class ControlUnit`
  - `__init__()` - Resets all signals to 0
  - `decode(instruction)` - Dispatches to the correct decoder based on opcode
  - `_decode_r_type(instruction)` - Sets RegWrite = 1, ALUSrc = 0; maps funct3 to ALUControl (AND = 010, OR = 011, XOR = 100)
  - `_decode_i_type(instruction)` - Sets RegWrite = 1, ALUSrc = 1; maps funct3 to ALUControl (XORI -> XOR = 100)
  - `_decode_load(instruction)` - Sets MemtoReg = 1, ALUSrc = 1, ALUControl = ADD
  - `_decode_store(instruction)` - Sets MemWrite = 1, ALUSrc = 1, ALUControl = ADD
  - `_decode_branch(_instruction)` - Sets Branch = 1, ALUSrc = 0, ALUControl = SUB
  - `get_alu_op_string()` - Translates numeric ALUControl code to the string ALU.operate() expects
  - `compute_pc_src(alu_zero)` - Models the AND gate: returns Branch AND ALU.zero
  - `get_control_signals()` - Returns all signals as a dict
  - `print_signals(pc, instruction)` - Prints control signals for trace output
  - `reset()` - Clears all signals to 0

### **mux.py** - Multiplexers
- `class Mux` - Base 2-to-1 multiplexer
  - `select(input0, input1, sel)` - Returns input0 if sel = 0, input1 if sel = 1
- `class ALUSrcMux` - Selects SrcB for the ALU
  - `select_src_b(rd2, sign_imm, alu_src)` - Returns RD2 (ALUSrc = 0) or sign-extended immediate (ALUSrc = 1)
- `class MemtoRegMux` - Selects write-back data
  - `select_write_back(alu_result, mem_read_data, mem_to_reg)` - Returns ALU result (0) or memory read data (1)
- `class PCSrcMux` - Selects next PC
  - `select_next_pc(pc_plus_4, branch_target, pc_src)` - Returns PC+4 (0) or branch target (1)

### **data_memory.py** - Data Memory
- `class DataMemory`
  - `__init__(size_words)` - Initializes sparse dict; default capacity 256 words (1 KB)
  - `read(address)` - Returns 32-bit word at byte address; returns 0 for unwritten addresses
  - `write(address, data, we)` - Writes data if WE = 1; converts byte address to word index
  - `load_program(initial_data)` - Pre-loads values for testing
  - `get_memory_content(start_word, num_words)` - Returns a slice as {byte_addr: value}
  - `print_memory_content(num_words)` - Prints non-zero entries for debugging
  - `reset()` - Clears all memory
  - `get_stats()` - Returns size and usage info

### **main.py** - Processor Simulation Driver
- `class SingleCycleProcessor`
  - `__init__(A, B, C, D)` - Instantiates all components; loads 4-instruction program; sets x1-x4 to A, B, C, D
  - `fetch()` - Fetches instruction at current PC from InstructionMemory
  - `decode(instruction)` - Runs ControlUnit and RegisterFile read; sign-extends immediate if I-type
  - `execute(rd1, rd2, imm_extended, alu_src, alu_control_code)` - Runs ALUSrcMux then ALU
  - `memory_access(alu_result, mem_write, mem_to_reg, we_from_control)` - Reads/writes DataMemory if needed
  - `write_back(alu_result, mem_read_data, mem_to_reg, dest_reg, reg_write)` - Runs MemtoRegMux then RegisterFile write
  - `update_pc(alu_zero)` - Computes PCSrc and advances PC via PCSrcMux
  - `run_instruction(instruction)` - Runs the full decode-execute-writeback-PC pipeline for one instruction
  - `run(verbose)` - Executes all 4 instructions; prints trace and final result; verifies against reference formula
  - `print_trace()` - Prints stored execution trace
  - `get_final_result()` - Returns register x7 (Y)
- `get_user_input()` - Prompts for A, B, C, D with defaults
- `main()` - Entry point: gets input, runs processor, prints register summary

### **test.py** - Test Suite
- `expected(A, B, C, D)` - Python reference formula: `((A & B) | (~C & 0xFFFFFFFF) & D) & 0xFFFFFFFF`
- `run_test(A, B, C, D)` - Instantiates processor, suppresses stdout via contextlib, returns (result, passed, expected)
- `test_boolean_inputs()` - Runs all 16 combinations of A, B, C, D in {0, 1}
- `test_32bit_inputs()` - Runs 8 32-bit integer edge cases (all-zeros, all-ones, alternating bits, masking)
- `if __name__ == "__main__"` - Runs both suites and prints overall PASS/FAIL

### **README.md** - Project documentation

---

## Potential Improvements

| Improvement | Description |
|---|---|
| Restore custom inversion encoding | The assignment specification requires NOT via ALU input inversion flag encoded in funct7 (not a separate XORI instruction). The current implementation uses standard RISC-V XORI (4 instructions). Reverting to the custom funct7 approach (3 instructions) would satisfy Section 1.2 and 1.4 of the assignment rubric exactly. |
| Bounds checking in DataMemory | `size_words` is stored but never enforced. Adding a check in `write()` would prevent accidental out-of-range writes in more complex programs. |
| B-type immediate in extend.py | `extend.py` supports I, S, and U types but not B-type (branch) or J-type (jump) immediates. These would be needed if BEQ or JAL instructions are added. |
| Clock-driven register write | `RegisterFile.write()` currently updates synchronously. A true single-cycle model would latch the write at the clock edge via `Clock.tick()`. |
| Instruction memory from Task 3 cache | Currently `InstructionMemory` uses a plain Python dict. Connecting it to Task 3's L1 cache and memory hierarchy would model realistic instruction fetch latency. |
| Expanded test.py | `test.py` currently tests the full pipeline only. Dedicated unit tests for individual components (ALU, extend, control unit, register file) using the existing `__main__` test blocks would give finer-grained failure isolation. |
| README for Tasks 1-3 | Each task has working code but no README. Consistent documentation across all four tasks would improve project completeness for the submission. |
