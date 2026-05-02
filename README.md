# CSC 4210/6210 Computer Architetcure - Processor Design Project

**Author:** Armando Galvan
**Course:** CSC 4210/6210 Computer Architecture
**Semester:** Spring 2026
**Instructor:** Professor Mohammed Alser


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


```bash
cd Task2_Boolean_Logic
python main.py
```

### Program Output
1. Truth table
2. Canonical equation (SOP or POS)
3. Minterm/Maxterm list
4. K-Map grouping
5. Simplified Booelan Equation
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
