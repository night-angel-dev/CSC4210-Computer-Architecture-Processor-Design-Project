"""
instruction.py - Outputs instruction fetched. A 32 bit instruction, RD 32 bit returns instruction read .

Defines instruction format (opcode, funct field, registers, immediate, etc.). Inversion encoded in function field (not opcode). Fetches and decodes instructions.

Possible connections:
6:0 to control unit for opcode
14:12 to control unit for funct3
31:25 to control unit for funct7

19:15 to A1 in Register File
24:20 to A2 in Register File
11:7 to A3 in Register File

31:7 depends on type of instruction (on where the bits for immediate are in the 32 bit instruction), for Immediate value to extend

Extend outputs ImmExt which connects to ALUSrc Mux as SignImm and an adder component that takes in PC too. Output of that adder would be Branch Target Address


"""

import sys
import os

# Get directory from current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Goes up one level and into Task 3 folder
task3_path = os.path.join(current_dir, "..", "Task3_Memory_Hierarchy_Simulation")

# add to path
if task3_path not in sys.path:
    sys.path.insert(0, task3_path)

try:
    from memory_display_utils import MemoryDisplayUtils
except ImportError as e:
    print(f"Import from Task3 failed: {e}")



class Instruction:
    """
    Instruction fetch/decode component.

    Supports two standard RISC-V formats used in this project:

    R-type (opcode 0x33) — register-register operations:
    - funct7[31:25] | rs2[24:20] | rs1[19:15] | funct3[14:12] | rd[11:7] | opcode[6:0]
    - Used for: AND, OR

    I-type (opcode 0x13) — register-immediate operations:
    - imm[31:20] | rs1[19:15] | funct3[14:12] | rd[11:7] | opcode[6:0]
    - Used for: XORI (XOR with -1 to compute NOT)
      
    NOT is achieved with the standard RISC-V format:
    - xori rd, rs1, -1 -> rd = rs1 XOR 0xFFFFFFFF = bitwise NOT rs1
    """

    # Opcodes
    OPCODE_R_TYPE = 0x33 # 011 0011  register-register (AND, OR)
    OPCODE_I_TYPE_ALU = 0x13 # 001 0011 register-immediate (XORI)

    # funct3 values
    FUNCT3_AND = 0x7 # 111
    FUNCT3_OR  = 0x6 # 110
    FUNCT3_XOR = 0x4 # 100 (used by both XOR and XORI)

    # Standard funct7
    FUNCT7_NORMAL = 0x00 # 000 0000 standard operations (AND, OR, XOR)


    def __init__(self, instruction_bits):
        """
        Initialize instruction decoder.

        @param instruction_bits - 32 bit instruction word
        """
        self.raw = instruction_bits
        self.display = MemoryDisplayUtils()

        # Extract each field by shifting and masking to its bit width.
        self.opcode = instruction_bits & 0x7F # bits [6:0]
        self.rd = (instruction_bits >> 7)  & 0x1F # bits [11:7]
        self.funct3 = (instruction_bits >> 12) & 0x7 # bits [14:12]
        self.rs1 = (instruction_bits >> 15) & 0x1F # bits [19:15]

        # R-type only fields
        self.rs2 = (instruction_bits >> 20) & 0x1F # bits [24:20]
        self.funct7 = (instruction_bits >> 25) & 0x7F # bits [31:25]

        # I-type immediate: bits [31:20] as a raw 12-bit unsigned value.
        # Sign extension to 32 bits is handled by the SignExtend component (extend.py).
        self.imm_i = (instruction_bits >> 20) & 0xFFF # bits [31:20]

    # Type checks 

    def is_r_type(self):
        """
        Check if instruction is R-type (AND, OR).

        @return - True if opcode is 0x33
        """
        return self.opcode == self.OPCODE_R_TYPE

    def is_i_type(self):
        """
        Check if instruction is I-type ALU (XORI).

        @return - True if opcode is 0x13
        """
        return self.opcode == self.OPCODE_I_TYPE_ALU

    # Field accessors

    def get_alu_op(self):
        """
        Determine ALU operation from opcode and funct3.

        @return - "AND", "OR", "XOR", or "UNKNOWN"
        """
        if self.funct3 == self.FUNCT3_AND and self.is_r_type():
            return "AND"
        elif self.funct3 == self.FUNCT3_OR and self.is_r_type():
            return "OR"
        elif self.funct3 == self.FUNCT3_XOR:
            # funct3 0x4 covers both R-type XOR and I-type XORI
            return "XOR"
        else:
            return "UNKNOWN"

    def get_imm_i(self):
        """
        Get raw 12-bit I-type immediate (bits [31:20]).
        Pass this to SignExtend.extend_i_type() to get the 32-bit sign-extended value.

        @return - 12-bit unsigned immediate value
        """
        return self.imm_i

    def get_rs1_value(self, register_file):
        """
        Read value from rs1 register.

        @param register_file - RegisterFile instance
        @return - 32-bit value from register rs1
        """
        # A1 port of register file maps to rs1 field
        rd1, _ = register_file.read(self.rs1, 0)
        return rd1

    def get_rs2_value(self, register_file):
        """
        Read value from rs2 register (R-type only).

        @param register_file - RegisterFile instance
        @return - 32-bit value from register rs2
        """
        # A2 port of register file maps to rs2 field
        _, rd2 = register_file.read(0, self.rs2)
        return rd2

    def get_destination(self):
        """
        Get destination register address (rd).

        @return - 5-bit register address (A3 port of register file)
        """
        return self.rd

    def get_instruction_name(self):
        """
        Get human-readable instruction name.

        @return - String like "AND", "OR", "XORI"
        """
        if self.is_i_type() and self.funct3 == self.FUNCT3_XOR:
            return "XORI"
        return self.get_alu_op()

    def print_fields(self):
        """
        Print instruction fields for debugging.
        Uses MemoryDisplayUtils from Task 3 for hex formatting.
        """
        raw_hex = self.display.int_to_hex(self.raw)
        fmt = "R-type" if self.is_r_type() else ("I-type" if self.is_i_type() else "other")
        print(f"  Instruction : {raw_hex}")
        print(f"  opcode      : {self.opcode:#04x}  ({fmt})")
        print(f"  funct3      : {self.funct3:#03x}   ({self.get_alu_op()})")
        print(f"  rs1         : x{self.rs1}")
        if self.is_r_type():
            print(f"  funct7      : {self.funct7:#04x}")
            print(f"  rs2         : x{self.rs2}")
        else:
            # I-type: show the immediate instead of rs2/funct7
            print(f"  imm[11:0]   : {self.imm_i:#05x}  ({self.imm_i})  -> sign-extend via extend.py")
        print(f"  rd  (dest)  : x{self.rd}")
        print(f"  name        : {self.get_instruction_name()}")


class InstructionMemory:
    """
    Instruction memory that holds the program.
    PC is a byte address; instructions are word-aligned (4 bytes each).
    """

    def __init__(self):
        """
        Initialize instruction memory.
        """
        # Word-addressed storage: key = byte address, value = 32-bit instruction
        self.memory = {}
        self.pc = 0
        self.display = MemoryDisplayUtils()

    def load_program(self, instructions):
        """
        Load program into instruction memory.

        @param instructions - List of 32-bit instruction words
        """
        self.memory = {}
        # Each instruction is 4 bytes/32 bits 
        for i, instr in enumerate(instructions):
            self.memory[i * 4] = instr

    def fetch(self, pc):
        """
        Fetch instruction at given PC.

        @param pc - Program counter (byte address, must be word-aligned)
        @return - Instruction object, or None if PC is out of range
        """
        raw = self.memory.get(pc, None)
        if raw is None:
            return None
        return Instruction(raw)

    def get_pc(self):
        """
        Get current program counter.

        @return - Current PC value
        """
        return self.pc

    def set_pc(self, pc):
        """
        Set program counter.

        @param pc - New PC value
        """
        self.pc = pc

    def increment_pc(self):
        """
        Increment PC by 4 (next instruction).
        """
        # Instructions are 4 bytes wide so PC always advances by 4
        self.pc += 4

    def reset(self):
        """Reset program counter to 0."""
        self.pc = 0

    def get_program_size(self):
        """
        Get number of instructions in program.

        @return - Instruction count
        """
        return len(self.memory)



# Independent file testing
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Instruction decode for Y = A*B + C'*D")
    print("=" * 60)

    # Program: Y = A*B + C'*D  (standard RISC-V encoding)
    # x1 = A, x2 = B, x3 = C, x4 = D
    #
    # Step 1: xori x6, x3, -1 -> x6 = NOT C (I-type, imm = -1 = 0xFFF)
    # Step 2: and x5, x1, x2 -> x5 = A AND B (R-type)
    # Step 3: and x6, x6, x4 -> x6 = (NOT C) AND D (R-type, rs1 = x6, rs2 = x4)
    # Step 4: or x7, x5, x6 -> x7 = Y (R-type)
    #
    # R-type encoding: funct7[31:25] | rs2[24:20] | rs1[19:15] | funct3[14:12] | rd[11:7] | opcode[6:0]
    # I-type encoding: imm[31:20]   | rs1[19:15]  | funct3[14:12] | rd[11:7]   | opcode[6:0]

    XORI_NOT_C = 0xFFF1C313 # xori x6, x3, -1 (I-type: imm=0xFFF, rs1=x3, funct3=4, rd=x6)
    AND_A_B = 0x0020F2B3 # and  x5, x1, x2 (R-type: funct7=0, rs2=x2, rs1=x1, funct3=7, rd=x5)
    AND_NOTC_D = 0x00437333 # and x6, x6, x4 (R-type: funct7=0, rs2=x4, rs1=x6, funct3=7, rd=x6)
    OR_Y = 0x0062E3B3 # or x7, x5, x6 (R-type: funct7=0, rs2=x6, rs1=x5, funct3=6, rd=x7)

    program = [XORI_NOT_C, AND_A_B, AND_NOTC_D, OR_Y]

    mem = InstructionMemory()
    mem.load_program(program)

    labels = [
        "Step 1: xori x6, x3, -1  (NOT C)",
        "Step 2: and  x5, x1, x2  (A*B)",
        "Step 3: and  x6, x6, x4  (C'*D)",
        "Step 4: or   x7, x5, x6  (Y)",
    ]

    for i, label in enumerate(labels):
        pc = i * 4
        instr = mem.fetch(pc)
        print(f"\n{label}  [PC={pc}]")
        instr.print_fields()

    # Spot-check specific fields
    xori = mem.fetch(0)
    and1 = mem.fetch(4)
    and2 = mem.fetch(8)
    or_y = mem.fetch(12)

    print("\n--- Type checks ---")
    print(f"Step 1 is I-type: {xori.is_i_type()} (expected True)")
    print(f"Step 2 is R-type: {and1.is_r_type()} (expected True)")
    print(f"Step 3 is R-type: {and2.is_r_type()} (expected True)")
    print(f"Step 4 is R-type: {or_y.is_r_type()} (expected True)")

    print("\n--- ALU op checks ---")
    print(f"Step 1 op: {xori.get_alu_op()} (expected XOR)")
    print(f"Step 2 op: {and1.get_alu_op()} (expected AND)")
    print(f"Step 3 op: {and2.get_alu_op()} (expected AND)")
    print(f"Step 4 op: {or_y.get_alu_op()} (expected OR)")

    print("\n--- XORI immediate ---")
    print(f"Step 1 imm: {xori.get_imm_i():#05x} (expected 0xfff = -1 when sign-extended)")

    assert xori.is_i_type()
    assert and1.is_r_type() and and2.is_r_type() and or_y.is_r_type()
    assert xori.get_alu_op() == "XOR"
    assert and1.get_alu_op() == "AND"
    assert or_y.get_alu_op() == "OR"
    assert xori.get_imm_i() == 0xFFF
    print("All checks done")

    print("\n--- PC walk ---")
    mem.reset()
    while mem.get_pc() < mem.get_program_size() * 4:
        instr = mem.fetch(mem.get_pc())
        print(f"  PC={mem.get_pc():2d}  {instr.get_instruction_name()}")
        mem.increment_pc()

    print("\n" + "=" * 60)
    print("Instruction Tests Complete")
    print("=" * 60)
