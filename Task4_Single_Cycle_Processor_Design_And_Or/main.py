"""
main.py - Runs programs, prompts user for input , Shows trace, control signals, register values, final Y value.

"""
import sys
import os

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import processor components
from instruction import Instruction, InstructionMemory
from register_file import RegisterFile
from alu import ALU
from control_unit import ControlUnit
from extend import SignExtend
from mux import ALUSrcMux, MemtoRegMux, PCSrcMux
from data_memory import DataMemory
from clock import Clock
from memory_display_utils import MemoryDisplayUtils


class SingleCycleProcessor:
    """
    Single-cycle processor that executes one instruction per clock cycle.
    
    Components:
    - Instruction Memory (IMem)
    - Register File (RegFile)
    - ALU
    - Control Unit
    - Sign Extend
    - Data Memory (DMem)
    - Multiplexers (ALUSrc, MemtoReg, PCSrc)
    - Clock
    """
    
    # Program instruction encodings for Y = A*B + C'*D
    # Using x1 = A, x2 = B, x3 = C, x4 = D, x5 = temp, x6 = temp, x7 = result
    # xori x6, x3, -1 (I-type: XOR with -1 = NOT C)
    # and  x5, x1, x2 (R-type: A AND B)
    # and  x6, x6, x4 (R-type: (NOT C) AND D)
    # or   x7, x5, x6 (R-type: final OR)
    
    # xori x6, x3, -1
    # imm = 0xFFF (12-bit -1), rs1 = x3(3), funct3 = 0x4(XOR), rd = x6(6), opcode = 0x13
    XORI_NOT_C = 0xFFF1C313
    
    # and x5, x1, x2
    # funct7 = 0, rs2 = x2(2), rs1 = x1(1), funct3 = 0x7(AND), rd = x5(5), opcode = 0x33
    AND_A_B = 0x0020F2B3
    
    # and x6, x6, x4
    # funct7 = 0, rs2 = x4(4), rs1 = x6(6), funct3 = 0x7(AND), rd = x6(6), opcode = 0x33
    AND_NOT_C_D = 0x00437333
    
    # or x7, x5, x6
    # funct7 = 0, rs2 = x6(6), rs1 = x5(5), funct3 = 0x6(OR), rd = x7(7), opcode = 0x33
    OR_RESULT = 0x0062E3B3
    
    PROGRAM = [XORI_NOT_C, AND_A_B, AND_NOT_C_D, OR_RESULT]
    
    def __init__(self, A=1, B=1, C=1, D=1):
        """
        Initialize the single-cycle processor.
        
        @param A - Input value for register x1
        @param B - Input value for register x2
        @param C - Input value for register x3
        @param D - Input value for register x4
        """
        # Create components
        self.imem = InstructionMemory()
        self.reg_file = RegisterFile()
        self.alu = ALU()
        self.control = ControlUnit()
        self.extend = SignExtend()
        self.dmem = DataMemory(size_words=64)
        self.clock = Clock()
        self.display = MemoryDisplayUtils()
        
        # Create multiplexers
        self.alu_src_mux = ALUSrcMux()
        self.memto_reg_mux = MemtoRegMux()
        self.pc_src_mux = PCSrcMux()
        
        # Load program into instruction memory
        self.imem.load_program(self.PROGRAM)
        
        # Initialize registers with input values
        self.reg_file.set_register(1, A & 0xFFFFFFFF) # x1 = A
        self.reg_file.set_register(2, B & 0xFFFFFFFF) # x2 = B
        self.reg_file.set_register(3, C & 0xFFFFFFFF) # x3 = C
        self.reg_file.set_register(4, D & 0xFFFFFFFF) # x4 = D
        
        # Reset state
        self.pc = 0
        self.instruction_count = 0
        self.trace = []
    
    def fetch(self):
        """
        Fetch instruction from instruction memory at current PC.
        
        @return - Instruction object or None if out of range
        """
        instr = self.imem.fetch(self.pc)
        if instr is None:
            return None
        
        # Format address for display
        pc_str = self.display.format_address(self.pc)
        print(f"\n  Fetch: PC = {pc_str}")
        
        return instr
    
    def decode(self, instruction):
        """
        Decode instruction and generate control signals.
        
        @param instruction - Instruction object
        """
        self.control.decode(instruction)
        
        # Read register values
        rd1, rd2 = self.reg_file.read(instruction.rs1, instruction.rs2)
        
        # Sign extend immediate if needed
        if instruction.is_i_type():
            imm_extended = self.extend.extend_i_type(instruction.get_imm_i())
        else:
            imm_extended = 0
        
        return rd1, rd2, imm_extended
    
    def execute(self, rd1, rd2, imm_extended, alu_src, alu_control_code):
        """
        Execute ALU operation.
        
        @param rd1 - First register value (SrcA)
        @param rd2 - Second register value (for ALUSrc=0)
        @param imm_extended - Sign-extended immediate (for ALUSrc=1)
        @param alu_src - Select signal (0=RD2, 1=imm)
        @param alu_control_code - ALU operation code (3 bits)
        @return - ALU result and zero flag
        """
        # Select SrcB using ALUSrc MUX
        src_b = self.alu_src_mux.select_src_b(rd2, imm_extended, alu_src)
        
        # Get ALU operation string from control unit
        alu_op = self.control.get_alu_op_string()
        
        # For I-type XORI (NOT), we don't need inversion since XOR with -1 gives NOT
        # For R-type, use standard operation
        invert_a = 0
        invert_b = 0
        
        # Perform ALU operation
        result = self.alu.operate(rd1, src_b, alu_op, invert_a, invert_b)
        zero_flag = self.alu.get_zero_flag()
        
        return result, zero_flag
    
    def memory_access(self, alu_result, mem_write, mem_to_reg, we_from_control):
        """
        Access data memory if needed.
        
        @param alu_result - ALU result (used as address for load/store)
        @param mem_write - Control signal for memory write
        @param mem_to_reg - Control signal for write-back selection
        @param we_from_control - Write enable from control unit
        @return - Memory read data (if load), otherwise 0
        """
        mem_read_data = 0
        
        # For store instructions
        if mem_write == 1:
            # Would write to data memory here
            pass
        
        # For load instructions
        if mem_to_reg == 1:
            mem_read_data = self.dmem.read(alu_result)
        
        return mem_read_data
    
    def write_back(self, alu_result, mem_read_data, mem_to_reg, dest_reg, reg_write):
        """
        Write back to register file.
        
        @param alu_result - Result from ALU
        @param mem_read_data - Data read from memory
        @param mem_to_reg - Select signal (0=ALU, 1=Memory)
        @param dest_reg - Destination register address
        @param reg_write - Write enable signal
        """
        # Select write-back data using MemtoReg MUX
        write_data = self.memto_reg_mux.select_write_back(alu_result, mem_read_data, mem_to_reg)
        
        # Write to register file if enabled
        if reg_write == 1:
            self.reg_file.write(dest_reg, write_data, 1)
    
    def update_pc(self, alu_zero):
        """
        Update program counter.
        
        @param alu_zero - Zero flag from ALU (for BEQ)
        """
        # Compute next PC (PC + 4)
        pc_plus_4 = self.pc + 4
        
        # Compute branch target (simplified: PC + immediate)
        branch_target = pc_plus_4
        
        # Compute PCSrc: Branch AND ALU.zero
        pc_src = self.control.compute_pc_src(alu_zero)
        
        # Select next PC
        next_pc = self.pc_src_mux.select_next_pc(pc_plus_4, branch_target, pc_src)
        
        # Update PC
        self.pc = next_pc
    
    def run_instruction(self, instruction):
        """
        Execute a single instruction.
        
        @param instruction - Instruction object
        @return - Dictionary with execution trace information
        """
        # Decode phase
        rd1, rd2, imm_extended = self.decode(instruction)
        
        # Get control signals
        signals = self.control.get_control_signals()
        
        # Execute phase
        alu_result, zero_flag = self.execute(
            rd1, rd2, imm_extended,
            signals['ALUSrc'],
            signals['ALUControl']
        )
        
        # Memory access phase (not used for R-type)
        mem_read_data = self.memory_access(
            alu_result,
            signals['MemWrite'],
            signals['MemtoReg'],
            signals['RegWrite']
        )
        
        # Write back phase
        self.write_back(
            alu_result, mem_read_data,
            signals['MemtoReg'],
            instruction.get_destination(),
            signals['RegWrite']
        )
        
        # Update PC
        self.update_pc(zero_flag)
        
        # Return trace information
        trace_entry = {
            'pc': self.pc - 4, # PC before update
            'instruction': instruction.get_instruction_name(),
            'rd1_value': rd1,
            'rd2_value': rd2,
            'alu_result': alu_result,
            'zero_flag': zero_flag,
            'dest_reg': instruction.get_destination(),
            'control_signals': signals.copy()
        }
        
        return trace_entry
    
    def run(self, verbose=True):
        """
        Run the program.
        
        @param verbose - If True, print detailed trace
        """
        print("=" * 60)
        print("SINGLE-CYCLE PROCESSOR SIMULATION")
        print("=" * 60)
        print("Computing: Y = A*B + C'*D (where *=AND, '=NOT, +=OR)")
        print("-" * 60)
        
        # Print input values
        A = self.reg_file.get_register(1)
        B = self.reg_file.get_register(2)
        C = self.reg_file.get_register(3)
        D = self.reg_file.get_register(4)
        
        print(f"Input values:")
        print(f"  A (x1) = 0x{A:08X} ({A})")
        print(f"  B (x2) = 0x{B:08X} ({B})")
        print(f"  C (x3) = 0x{C:08X} ({C})")
        print(f"  D (x4) = 0x{D:08X} ({D})")
        print("-" * 60)
        
        # Reset state
        self.pc = 0
        self.instruction_count = 0
        self.trace = []
        
        # Execute each instruction
        program_size = self.imem.get_program_size()
        
        for step in range(program_size):
            # Fetch instruction
            instruction = self.fetch()
            if instruction is None:
                break
            
            # Print instruction header
            pc_str = self.display.format_address(self.pc)
            print(f"\nStep {step + 1}: PC={pc_str}")
            instruction.print_fields()
            
            # Execute instruction
            trace_entry = self.run_instruction(instruction)
            self.trace.append(trace_entry)
            self.instruction_count += 1
            
            # Print register values after instruction
            if verbose:
                print(f"\n  After {instruction.get_instruction_name()}:")
                print(f"    x5 (t0) = 0x{self.reg_file.get_register(5):08X}")
                print(f"    x6 (t1) = 0x{self.reg_file.get_register(6):08X}")
                print(f"    x7 (t2) = 0x{self.reg_file.get_register(7):08X}")
        
        # Print final results
        print("\n" + "=" * 60)
        print("SIMULATION RESULTS")
        print("=" * 60)
        
        final_result = self.reg_file.get_register(7) # x7 = final result
        
        print(f"\nIntermediate results:")
        print(f"  t4 (x5) = A & B = 0x{self.reg_file.get_register(5):08X}")
        print(f"  t6 (x6) = C' & D = 0x{self.reg_file.get_register(6):08X}")
        print(f"\nFinal result:")
        print(f"  Y (x7) = t4 | t6 = 0x{final_result:08X} ({final_result})")
        
        # Verify against expected formula
        expected = (A & B) | ((~C & 0xFFFFFFFF) & D)
        print(f"\nVerification:")
        print(f"  Expected: (A & B) | (C' & D) = {expected}")
        
        if final_result == expected:
            print("  PASS: Result matches expected value!")
        else:
            print("  FAIL: Result does not match expected value!")
        
        print("\n" + "=" * 60)
        print(f"Instructions executed: {self.instruction_count}")
        print("=" * 60)
        
        return final_result
    
    def print_trace(self):
        """
        Print execution trace.
        """
        print("\n" + "=" * 60)
        print("EXECUTION TRACE")
        print("=" * 60)
        
        for i, entry in enumerate(self.trace):
            pc_str = self.display.format_address(entry['pc'])
            print(f"\n{i + 1}: PC={pc_str} - {entry['instruction']}")
            print(f"    ALU result: 0x{entry['alu_result']:08X}")
            print(f"    Zero flag: {entry['zero_flag']}")
            print(f"    Destination: x{entry['dest_reg']}")
    
    def get_final_result(self):
        """
        Get final result from register x7.
        
        @return - Final Y value
        """
        return self.reg_file.get_register(7)


def get_user_input():
    """
    Prompt user for input values A, B, C, D.
    
    @return - Tuple (A, B, C, D)
    """
    print("\nEnter input values for Y = A*B + C'*D")
    print("(Values can be 0 or 1, or any 32-bit integer)")
    print("-" * 40)
    
    try:
        A = int(input("Enter A (x1): ") or "1")
        B = int(input("Enter B (x2): ") or "1")
        C = int(input("Enter C (x3): ") or "1")
        D = int(input("Enter D (x4): ") or "1")
    except ValueError:
        print("Invalid input. Using default values (1,1,1,1)")
        A, B, C, D = 1, 1, 1, 1
    
    return A, B, C, D


def main():
    """
    Main entry point.
    """
    print("=" * 60)
    print("SINGLE-CYCLE PROCESSOR DESIGN")
    print("=" * 60)
    print("Target Expression: Y = A*B + C'*D")
    print("Instructions: XORI, AND, AND, OR")
    print("=" * 60)
    
    # Get user input for A, B, C, D
    A, B, C, D = get_user_input()
    
    # Create and run processor
    processor = SingleCycleProcessor(A = A, B = B, C = C, D = D)
    result = processor.run(verbose = True)
    
    # Print register summary
    print("\n" + "=" * 60)
    print("FINAL REGISTER STATE")
    print("=" * 60)
    
    registers = [1, 2, 3, 4, 5, 6, 7]
    names = {1: "A", 2: "B", 3: "C", 4: "D", 5: "t4", 6: "t6", 7: "Y"}
    
    for reg in registers:
        value = processor.reg_file.get_register(reg)
        print(f"  x{reg} ({names[reg]}): 0x{value:08X} ({value})")
    
    print("\nThank you for using the Single-Cycle Processor Simulator.")


if __name__ == "__main__":
    main()