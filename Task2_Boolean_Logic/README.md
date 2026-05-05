# Task 2: Boolean Logic & K-Map Simplification

**Name:** Armando Galvan
**Course:** CSC 4210/6210 Computer Architecture
**Semester:** Spring 2026
**Due Date:** March 20, 2026

## Overview

This project implements a combinational logic design tool that converts truth tables into Boolean equations and simplifies them using Karnaugh Maps (K-Maps). It supports 2 to 4 input variables and produces both canonical SOP and POS forms, K-map groupings, a simplified Boolean expression, and a validation result confirming the simplification is correct. This task builds on Task 1 by importing `binary_utils.py` for binary conversion utilities used during minterm and expression generation.

## Functional Requirements Implemented

| FR  | Description                                              | Status |
| --- | -------------------------------------------------------- | ------ |
| FR1 | Input system: n variables (2–4), truth table, validation | X      |
| FR2 | Canonical SOP equation from minterms                     | X      |
| FR3 | Canonical POS equation from maxterms                     | X      |
| FR4 | Minterm and maxterm list generation                      | X      |
| FR5 | K-Map construction and grouping (2–4 variables)          | X      |
| FR6 | Simplified Boolean expression from K-Map                 | X      |
| FR7 | Expression validation against original truth table       | X      |
| FR8 | All required program output in specified order           | X      |


### **Potential Improvements**
- **Don't-care conditions**: Adding support for don't-care entries (X) in truth tables would allow further K-map simplification in incomplete specifications.
- **More than 4 variables**: The Quine-McCluskey algorithm could extend support beyond 4 variables where K-maps are not practical.
- **POS simplification via K-Map**: Currently K-map grouping targets SOP (1-groupings); grouping 0-cells for direct POS simplification would add completeness.
- **File-based input**: Truth tables are currently entered interactively via console. A CSV or JSON file input option would allow batch processing.

## Repository Structure

### **truth_table.py** - Truth table data structure
- `class TruthTable`
  - `__init__(num_vars, rows)` - Stores rows as `(inputs_tuple, output)` pairs; triggers `_process_terms()`
  - `_process_terms()` - Iterates rows to populate `self.minterms` (output=1) and `self.maxterms` (output=0) by row index

### **input_handler.py** - Console-based truth table input
- `class InputHandler`
  - `get_truth_table()` - Prompts for number of variables (2–4); auto-generates all 2^n input combinations in Gray-code order; collects output values one row at a time; returns `(num_vars, rows)`

### **boolean_expression.py** - Canonical SOP/POS generation
- Imports `decimal_to_padded_binary` and `decimal_to_binary` from Task 1's `binary_utils.py`
- `class BooleanExpression`
  - `__init__(truth_table)` - Initializes with a TruthTable; sets variable names A, B, C, D
  - `get_canonical_sop()` - Builds SOP from minterms (e.g., `A'B'C + A'BC'`); returns `"0"` if no minterms
  - `get_canonical_pos()` - Builds POS from maxterms (e.g., `(A+B'+C)`); returns `"1"` if no maxterms
  - `get_minterm_list()` - Returns formatted string `m(0,1,3,...)`
  - `get_maxterm_list()` - Returns formatted string `M(2,4,5,...)`
  - `get_minterms_binary()` - Returns list of binary strings for each minterm (used by K-map)
  - `get_maxterms_binary()` - Returns list of binary strings for each maxterm

### **karnaugh_map.py** - K-Map construction and simplification
- `class KarnaughMap`
  - `__init__(truth_table)` - Builds the K-map grid on initialization via `_build_kmap()`
  - `_build_kmap()` - Dispatches to the correct builder based on `num_vars`
  - `_build_2var_kmap()` - Builds 2×2 grid (rows: A; cols: B)
  - `_build_3var_kmap()` - Builds 2×4 grid (rows: A; cols: BC in Gray code order 00,01,11,10)
  - `_build_4var_kmap()` - Builds 4×4 grid (rows: AB; cols: CD in Gray code order)
  - `get_simplified_expression()` - Groups adjacent 1-cells using prime implicant logic; returns simplified SOP string

### **evaluator.py** - Expression validation
- `class ExpressionEvaluator`
  - `evaluate_expression(expression, inputs, num_vars)` - Evaluates an SOP string for a single input combination; handles complemented literals (e.g., `A'`) and special cases `"0"` / `"1"`
  - `validate(truth_table, simplified_expression)` - Runs `evaluate_expression` for every row in the truth table; prints per-row PASS/FAIL; returns `"PASS"` if all rows match, `"FAIL"` otherwise

### **output_formatter.py** - Formatted program output
- `class OutputFormatter`
  - `__init__(truth_table, boolean_expr, karnaugh_map, evaluator_result)` - Stores all components
  - `print_all()` - Calls all print methods in the required output order
  - `print_truth_table()` - Prints the full truth table with column headers
  - `print_canonical_equations()` - Prints both SOP and POS canonical forms
  - `print_minterms_maxterms()` - Prints minterm and maxterm lists
  - `print_kmap()` - Prints the K-map grid and identified groupings
  - `print_simplified_expression()` - Prints the final simplified Boolean expression
  - `print_validation()` - Prints the PASS/FAIL validation result

### **main.py** - Program entry point
- `main()` - Orchestrates the full pipeline: input → TruthTable → BooleanExpression → KarnaughMap → ExpressionEvaluator → OutputFormatter; loops until user exits

### **test.py** - Unit test suite
- Tests canonical SOP and POS generation for AND, OR, XOR-like functions
- Tests K-map simplification for 2-, 3-, and 4-variable functions
- Tests boundary cases: all-zeros output, all-ones output
- Tests validation with both correct and incorrect simplified expressions

### **README.md** - Project documentation

## How to Run

### Prerequisites
- Python 3.6 or higher
- No external packages required
- `Task1_Data_Systems/binary_utils.py` must be present (used for binary conversion)

### Running the Interactive Interface
```bash
cd Task2_Boolean_Logic
python main.py
```

You will be prompted to enter the number of input variables (2–4). The program then auto-generates all input combinations and asks you to enter the output value (0 or 1) for each row. After completing the truth table, the program outputs the canonical SOP and POS equations, minterm/maxterm lists, K-map with groupings, simplified Boolean expression, and a PASS/FAIL validation result.

**Example session (2-variable AND gate):**
```
Enter number of input variables (2-4): 2

Row 1 | A=0, B=0 | Output: 0
Row 2 | A=0, B=1 | Output: 0
Row 3 | A=1, B=0 | Output: 0
Row 4 | A=1, B=1 | Output: 1
```

Expected simplified expression: `AB`

### Running the Tests
```bash
cd Task2_Boolean_Logic
python test.py
```
