"""
control_unit.py - Decodes opcode 6:0 , functions (funct3 14:12, funct7 31:25) this should probably be dependent on opcode since opcode determines instruction types.

Outputs/generates signals
PCSrc (Connects to PCSrc MUX) To select next PC (PC + 4 or branch target)

ResultSrc (Connects to ResultSrc MUX) Select write-back data for ALU or memory

MemWrite (connects to Data Memory WE) Enable data memory write

ALUControl 2:0 (Connects to ALU) Tell ALU what to do (AND/OR/XOR)

ALUSrc (Connects to ALUSrc MUX) Select SrcB (register or immediate)

ImmSrc 1:0 (Connects to Extend component) Tell extend what type of immediate

RegWrite (Connects to Register File WE3) Enable register write

Branch (AND-ed with ALU Zero flag externally to produce PCSrc)

PCSrc = Branch AND ALU.zero
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
    

# Based on the resources I used, its conflicting from what I see on the slide from one of our lectures.
# Like in the site from cornell.edu funct3 for and/ANDI is 111, I assumed this is what is 
# passed down to the ALU but in a slide from the course I see theres a value of 010 for and
# I might just go with whats on the cornell website https://www.cs.cornell.edu/courses/cs3410/2025fa/rsrc/riscv-instructions-2.html
# Dam this really does have my head spinning

class ControlUnit:
    """
    Control unit for single cycle processor.

    Generates control signals based on instruction opcode and funct fields.

    Control Signals:
    - RegWrite  (1 bit): Write Enable for register file
    - ALUSrc    (1 bit): Select ALU SrcB (0 = RD2, 1 = immediate)
    - MemToReg  (1 bit): Select write back data (0 = ALU result, 1 = Data Memory)
    - MemWrite  (1 bit): Enable data memory write
    - Branch    (1 bit): Branch intent; PCSrc = Branch AND ALU.zero (computed externally)
    - ALUControl (3 bits): Internal code for ALU operation; translate with get_alu_op_string()
    - ImmSrc    (2 bits): Immediate type for sign extend (00=I, 01=S, 10=U)
    """

    # ALU Control Codes (3 bits) - internal identifiers, not funct3 values.
    ALU_ADD = 0b000 # 0
    ALU_SUB = 0b001 # 1
    ALU_AND = 0b010 # 2 
    ALU_OR  = 0b011 # 3
    ALU_XOR = 0b100 # 4 covers both XOR (R-type) and XORI (I-type)

    # Maps ALUControl code -> string that alu.py's operate() expects.
    # This bridges the numeric control signal to the ALU's string-based interface.
    ALU_CONTROL_NAMES = {
        0b000: "ADD",
        0b001: "SUB",
        0b010: "AND",
        0b011: "OR",
        0b100: "XOR",
    }
    
    # Opcodes 
    OPCODE_R_TYPE = 0x33 # 011 0011 (AND, OR, XOR)
    OPCODE_I_TYPE = 0x13 # 001 0011 (ADDI, XORI, ORI, ANDI)
    OPCODE_LOAD = 0x03 # 000 0011 (LW)
    OPCODE_STORE = 0x23 # 010 0011 (SW)
    OPCODE_BRANCH = 0x63 # 110 0011 (BEQ)
    
    # funct3 vlaues (14:12)
    FUNCT3_XOR = 0x4 # 100 (XOR/XORI)
    FUNCT3_OR = 0x6 # 110 (OR/ORI)
    FUNCT3_AND = 0x7 # 111 (AND/ANDI)
    
    def __init__(self):
        """
        Initialize control unit with default signal values
        """
        self.reset()
        self.display = MemoryDisplayUtils()
        pass
    
    def decode(self, instruction):
        """
        Decode instruction and generate control signals
        
        @param instruction - Insturction object from instruction.py
        """
        
        opcode = instruction.opcode
        
        # Default all signals to 0 before decoding
        self.reg_write = 0
        self.alu_src = 0
        self.mem_to_reg = 0
        self.mem_write = 0
        self.branch = 0 # branch intent; PCSrc = branch AND alu.zero, computed externally
        self.alu_control = 0
        self.imm_src = 0b00

        # Decode based on opcode
        if opcode == self.OPCODE_R_TYPE:
            self._decode_r_type(instruction)
        elif opcode == self.OPCODE_I_TYPE:
            self._decode_i_type(instruction)
        elif opcode == self.OPCODE_LOAD:
            self._decode_load(instruction)
        elif opcode == self.OPCODE_STORE:
            self._decode_store(instruction)
        elif opcode == self.OPCODE_BRANCH:
            self._decode_branch(instruction)
        
    def _decode_r_type(self, instruction):
        """
        Decode R type instruction AND OR
        
        @param instruction - Instruction object
        """
        self.reg_write = 1
        self.alu_src = 0 # Use RD2 from register file
        self.mem_to_reg = 0 # Write ALU result to register
        self.mem_write = 0
        self.imm_src = 0b00 # Not used for R-type
        
        # Set ALUControl based on funct3
        funct3 = instruction.funct3
        
        if funct3 == self.FUNCT3_AND:
            self.alu_control = self.ALU_AND
        elif funct3 == self.FUNCT3_OR:
            self.alu_control = self.ALU_OR
        elif funct3 == self.FUNCT3_XOR:
            self.alu_control = self.ALU_XOR
        
    def _decode_i_type(self, instruction):
        """
        Decode I type instruction (XORI for NOT)
        
        @param instruction - Instruction object
        """
        self.reg_write = 1
        self.alu_src = 1 # Use immediate from sign extend
        self.mem_to_reg = 0 # Write ALU result to register
        self.mem_write = 0
        self.imm_src = 0b00 # I-type immediate
        
        # Set ALUControl based on funct3
        funct3 = instruction.funct3
        
        if funct3 == self.FUNCT3_AND:
            self.alu_control = self.ALU_AND
        elif funct3 == self.FUNCT3_OR:
            self.alu_control = self.ALU_OR
        elif funct3 == self.FUNCT3_XOR:
            self.alu_control = self.ALU_XOR # XORI uses the same ALU code
            
    def _decode_load(self, instruction):
        """
        Decode load instruction LW
        """
        self.reg_write = 1
        self.alu_src = 1 # Use immediate for address calculation
        self.mem_to_reg = 1 # Write memory data to register
        self.mem_write = 0
        self.alu_control = self.ALU_ADD # LW uses ADD for address
        self.imm_src = 0b00 # I-type immediate
    
    def _decode_store(self, instruction):
        """
        Decode store instruction SW
        """
        self.reg_write = 0
        self.alu_src = 1 # Use immediate for address calculation
        self.mem_to_reg = 0
        self.mem_write = 1
        self.alu_control = self.ALU_ADD # SW uses ADD for address
        self.imm_src = 0b01 # S-type immediate
        
    def _decode_branch(self, _instruction):
        """
        Decode branch instruction BEQ.

        The control unit sets Branch=1 to signal branch intent.
        PCSrc is NOT set here — it is computed externally:
            PCSrc = Branch AND ALU.zero
        That AND gate lives in the datapath, not the control unit.
        """
        self.reg_write = 0
        self.alu_src = 0  # Compare RD1 and RD2 directly
        self.mem_to_reg = 0
        self.mem_write = 0
        self.alu_control = self.ALU_SUB # BEQ subtracts to check equality (zero flag)
        self.imm_src = 0b01 # B-type immediate
        self.branch = 1  # signal branch intent; processor AND-s with alu.zero
        
    
    def get_alu_op_string(self):
        """
        Translate the numeric ALUControl code to the string alu.py's operate() expects.
        Call this when passing ALUControl to the ALU.

        @return - "AND", "OR", "XOR", "ADD", "SUB", or "UNKNOWN"
        """
        return self.ALU_CONTROL_NAMES.get(self.alu_control, "UNKNOWN")

    def compute_pc_src(self, alu_zero):
        """
        Compute the final PCSrc signal using the Branch control signal and ALU zero flag.
        This models the AND gate in the datapath between the control unit and PCSrc MUX.

        @param alu_zero - Zero flag from ALU (1 if result == 0, used for BEQ)
        @return - 1 if branch is taken, 0 otherwise
        """
        return 1 if (self.branch and alu_zero) else 0

    def get_control_signals(self):
        """
        Get all control signals as a dictionary.

        @return - Dictionary of control signals
        """
        return {
            'RegWrite':   self.reg_write,
            'ALUSrc':     self.alu_src,
            'MemtoReg':   self.mem_to_reg,
            'MemWrite':   self.mem_write,
            'Branch':     self.branch,
            'ALUControl': self.alu_control,
            'ALUOp':      self.get_alu_op_string(),
            'ImmSrc':     self.imm_src,
        }
        
    def print_signals(self, pc = 0, instruction = None):
        """
        Print control signals for debugging.

        @param pc - Program counter
        @param instruction - Instruction object
        """
        if instruction:
            print(f"\nPC = {pc}  {instruction.get_instruction_name()}")

        signals = self.get_control_signals()
        print(f"  RegWrite:   {signals['RegWrite']}")
        print(f"  ALUSrc:     {signals['ALUSrc']} (0 = RD2, 1 = Imm)")
        print(f"  MemtoReg:   {signals['MemtoReg']}")
        print(f"  MemWrite:   {signals['MemWrite']}")
        print(f"  Branch:     {signals['Branch']}  (PCSrc = Branch AND ALU.zero)")
        print(f"  ALUControl: {signals['ALUControl']:03b} -> {signals['ALUOp']}")
        print(f"  ImmSrc:     {signals['ImmSrc']:02b} (00 = I, 01 = S, 10 = U)")
    
    def reset(self):
        """
        Reset control unit to default state.
        """
        self.reg_write = 0
        self.alu_src = 0
        self.mem_to_reg = 0
        self.mem_write = 0
        self.branch = 0
        self.alu_control = 0
        self.imm_src = 0b00
        
# In file independent testing
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Control Unit")
    print("=" * 60)
    
    # Import Instruction class for testing
    sys.path.insert(0, os.path.join(current_dir, "..", "Task4_Single_Cycle_Processor_Design_And_Or"))
    
    # Dummy instruction class for standalone testing
    class DummyInstruction:
        def __init__(self, opcode, funct3 = 0, funct7 = 0):
            self.opcode = opcode
            self.funct3 = funct3
            self.funct7 = funct7
        def get_instruction_name(self):
            return "TEST"
    
    cu = ControlUnit()
    
    # Test XORI (I-type with XOR funct3)
    print("\n--- Test XORI (I-type, funct3=0x4, XOR) ---")
    instr_xori = DummyInstruction(ControlUnit.OPCODE_I_TYPE, ControlUnit.FUNCT3_XOR)
    cu.decode(instr_xori)
    cu.print_signals(pc = 0, instruction = instr_xori)
    
    # Test ANDI (I-type with AND funct3)
    print("\n--- Test ANDI (I-type, funct3=0x7, AND) ---")
    instr_andi = DummyInstruction(ControlUnit.OPCODE_I_TYPE, ControlUnit.FUNCT3_AND)
    cu.decode(instr_andi)
    cu.print_signals(pc = 4, instruction = instr_andi)
    
    # Test ORI (I-type with OR funct3)
    print("\n--- Test ORI (I-type, funct3=0x6, OR) ---")
    instr_ori = DummyInstruction(ControlUnit.OPCODE_I_TYPE, ControlUnit.FUNCT3_OR)
    cu.decode(instr_ori)
    cu.print_signals(pc = 8, instruction = instr_ori)
    
    # Test R-type AND
    print("\n--- Test AND (R-type, funct3=0x7) ---")
    instr_and = DummyInstruction(ControlUnit.OPCODE_R_TYPE, ControlUnit.FUNCT3_AND)
    cu.decode(instr_and)
    cu.print_signals(pc = 12, instruction = instr_and)
    
    print("\n" + "=" * 60)
    print("Control Unit Tests Complete")
    print("=" * 60)
        
        