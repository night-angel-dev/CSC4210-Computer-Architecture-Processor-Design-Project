# Task 1: Data Systems - 32-Bit Signed Integer Converter

**Name:** Armando Galvan
**Course:** CSC 4210/6210 Computer Architecture
**Semester:** Spring 2026
**Due Date:** February 20, 2026

## Overview

This project implements a 32-bit signed integer converter for an IoT processor prototype. It handles decimal input and converts to binary (two's complement) and hexadecimal with overflow detection and saturation.

## Functional Requirements Implemented

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


### **Potential Improvements**
- **Modular Architecture**: NumberSystemConverter.py currently has ~400+ lines, which 
  could be split into specialized files (e.g., binary_operations.py for two's complement 
  and binary addition, similarly if needed hex_ops.py for hexadecimal conversions, etc.)

- **Additional Bit-widths**: Support for 8-bit, 16-bit, and 64-bit modes

- **Extended Operations**: ADD, SUB, MUL, DIV, AND, OR, XOR, shift operations


## Repository Structure

### **NumberSystemConverter.py** - Core conversion logic
- `class NumberSystemConverter`
  - `__init__()` - Initializes constants and status flags
  - `decimal_to_signed_32bit()` - Parses/validates decimal input (FR1)
  - `decimal_to_binary()` - Decimal → 32-bit binary (FR3)
  - `twos_complement()` - Positive binary → negative using two's complement
  - `binary_addition()` - Adds two binary strings bit by bit
  - `binary_to_hexadecimal()` - Binary → hex using 4-bit groups (FR3)
  - `binary_to_decimal()` - Binary → decimal (FR3)
  - `detect_overflow()` - Checks if value exceeds 32-bit range (FR4)
  - `apply_saturation()` - Clamps values to 32-bit min/max (FR5)
  - `format_output()` - Formats results as DEC/BIN/HEX (FR6)
  - `convert()` - Main conversion method (FR7)

### **main.py** - Interactive command-line interface
- `main()` - Menu-driven CLI interface
- `if __name__ == "__main__"` - Runs when file executed directly

### **test.py** - Unit test suite (FR8 coverage)
- `run_all_tests()` - Executes all FR8 test cases
- `if __name__ == "__main__"` - Runs tests when file executed directly

### **README.md** - Project documentation

## How to Run

### Prerequisites
- Python 3.6 or higher


### Running the Interactive Interface
```bash
python main.py
```



