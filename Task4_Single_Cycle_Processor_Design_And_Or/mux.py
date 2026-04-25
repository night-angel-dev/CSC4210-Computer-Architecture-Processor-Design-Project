"""
mux.py - Multiplexers 
ALUSrc MUX (selects between RD2 and Sign immediate). Should return SrcB

MemtoReg Mux (selcts between ALU result and DataMemory RD). Returns Result 

PCSrc Mux (PC + 4 vs branch target). Also takes in signal from control unit PCSrc.

"""


class Mux2to1:
    """
    2 to 1 multiplexer for 32 bit instructions data
    
    Inputs:
    - input0 : 32 bit value selected when sel = 0
    - input1: 32 bit value selected when sel = 1
    - sel: 1 bit select signal 
    
    Output:
    - output: 32 bit selected value
    """
    
    def __init__(self, name = "MUX"):
        """
        Initialize multiplexer.
        
        @param name - Identifier for this MUX (e.g., "ALUSrc", "MemtoReg")
        """
        self.name = name
        self.output = 0
        
    def select(self, input0, input1, sel):
        """
        Select between two 32-bit inputs based on select signal.
        
        @param input0 - 32-bit value (sel = 0)
        @param input1 - 32-bit value (sel = 1)
        @param sel - Select signal (0 or 1)
        @return - Selected 32-bit value
        """
        if sel == 0:
            self.output = input0 & 0xFFFFFFFF
        else:
            self.output = input1 & 0xFFFFFFFF
        
        return self.output
    
    def get_output(self):
        """
        Get the last selected output.
        
        @return - 32-bit value
        """
        return self.output
    
    def reset(self):
        """
        Reset MUX output to 0.
        """
        self.output = 0


class ALUSrcMux(Mux2to1):
    """
    ALU Source Multiplexer.
    
    Selects the second input to the ALU:
    - sel = 0: RD2 (value from register file)
    - sel = 1: SignImm (sign-extended immediate from instruction)
    
    For R-type instructions (AND, OR): sel = 0 (use register)
    For I-type instructions (XORI): sel = 1 (use immediate)
    """
    
    def __init__(self):
        """
        Initialize ALUSrc MUX
        """
        super().__init__(name = "ALUSrc MUX")
    
    def select_src_b(self, rd2, sign_imm, alu_src):
        """
        Select ALU source B
        
        @param rd2 - 32-bit value from register file (RD2)
        @param sign_imm - 32-bit sign-extended immediate
        @param alu_src - Control signal (0 = RD2, 1 = immediate)
        @return - Selected 32-bit value for ALU input B
        """
        return self.select(rd2, sign_imm, alu_src)


class MemtoRegMux(Mux2to1):
    """
    Memory to Register Multiplexer.
    
    Selects data to write back to register file:
    - sel = 0: ALU result
    - sel = 1: Data Memory read data (RD)
    
    For (AND/OR/XORI): sel = 0 always (no memory access)
    """
    
    def __init__(self):
        """
        Initialize MemtoReg MUX.
        """
        super().__init__(name = "MemtoReg MUX")
    
    def select_write_back(self, alu_result, mem_read_data, mem_to_reg):
        """
        Select write-back data for register file.
        
        @param alu_result - 32-bit result from ALU
        @param mem_read_data - 32-bit data from Data Memory
        @param mem_to_reg - Control signal (0 = ALU result, 1 = memory)
        @return - Selected 32-bit value to write to register file
        """
        return self.select(alu_result, mem_read_data, mem_to_reg)


class PCSrcMux(Mux2to1):
    """
    Program Counter Source Multiplexer.
    
    Selects next program counter value:
    - sel = 0: PC + 4 (normal sequential execution)
    - sel = 1: Branch Target Address (for taken branches)
    
    PCSrc = Branch AND ALU.zero (computed externally by control unit)
    """
    
    def __init__(self):
        """Initialize PCSrc MUX."""
        super().__init__(name = "PCSrc MUX")
    
    def select_next_pc(self, pc_plus_4, branch_target, pc_src):
        """
        Select next PC value.
        
        @param pc_plus_4 - 32-bit PC + 4 (next sequential instruction)
        @param branch_target - 32-bit branch target address
        @param pc_src - Select signal (0 = PC+4, 1 = branch target)
        @return - Selected 32-bit next PC value
        """
        return self.select(pc_plus_4, branch_target, pc_src)


class ImmediateMux(Mux2to1):
    """
    Immediate Source Multiplexer (for extend.py).
    
    Selects which immediate value to pass to sign extend unit.
    Not heavily used for this assignment but included for completeness.
    """
    
    def __init__(self):
        """Initialize Immediate MUX."""
        super().__init__(name="ImmSrc MUX")
    
    def select_immediate(self, imm_i, imm_s, imm_src):
        """
        Select which immediate to extend.
        
        @param imm_i - I-type immediate (12 bits from bits 31:20)
        @param imm_s - S-type immediate (assembled from bits 31:25 and 11:7)
        @param imm_src - Select signal (0 = I, 1 = S, 2 = B, 3 = U)
        @return - Selected immediate value (12 or 20 bits)
        """
        if imm_src == 0:
            return imm_i
        elif imm_src == 1:
            return imm_s
        else:
            return 0


# For testing multiplexers independently
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Multiplexers")
    print("=" * 60)
    
    # Test ALUSrc MUX
    print("\n--- Test 1: ALUSrc MUX ---")
    alu_src_mux = ALUSrcMux()
    
    rd2 = 0x12345678
    sign_imm = 0x0000000F
    
    # R-type: sel = 0 (use RD2)
    result = alu_src_mux.select_src_b(rd2, sign_imm, 0)
    print(f"  ALUSrc = 0: RD2 = 0x{rd2:08X}, Imm = 0x{sign_imm:08X} -> 0x{result:08X}")
    print(f"    Expected: 0x{rd2:08X}")
    
    # I-type: sel = 1 (use immediate)
    result = alu_src_mux.select_src_b(rd2, sign_imm, 1)
    print(f"  ALUSrc = 1: RD2 = 0x{rd2:08X}, Imm = 0x{sign_imm:08X} -> 0x{result:08X}")
    print(f"    Expected: 0x{sign_imm:08X}")
    
    # Test MemtoReg MUX
    print("\n--- Test 2: MemtoReg MUX ---")
    memto_reg_mux = MemtoRegMux()
    
    alu_result = 0xABCDEF12
    mem_read = 0x87654321
    
    # sel = 0 (use ALU result)
    result = memto_reg_mux.select_write_back(alu_result, mem_read, 0)
    print(f"  MemtoReg = 0: ALU = 0x{alu_result:08X}, Mem = 0x{mem_read:08X} -> 0x{result:08X}")
    
    # sel = 1 (use memory data)
    result = memto_reg_mux.select_write_back(alu_result, mem_read, 1)
    print(f"  MemtoReg = 1: ALU = 0x{alu_result:08X}, Mem = 0x{mem_read:08X} -> 0x{result:08X}")
    
    # Test PCSrc MUX
    print("\n--- Test 3: PCSrc MUX ---")
    pc_src_mux = PCSrcMux()
    
    pc_plus_4 = 0x00000004
    branch_target = 0x00000100
    
    # sel = 0 (PC+4)
    result = pc_src_mux.select_next_pc(pc_plus_4, branch_target, 0)
    print(f"  PCSrc = 0: PC + 4 = 0x{pc_plus_4:08X}, Branch = 0x{branch_target:08X} -> 0x{result:08X}")
    
    # sel = 1 (branch target)
    result = pc_src_mux.select_next_pc(pc_plus_4, branch_target, 1)
    print(f"  PCSrc = 1: PC + 4 = 0x{pc_plus_4:08X}, Branch = 0x{branch_target:08X} -> 0x{result:08X}")
    
    # Test combined MUX in single cycle
    print("\n--- Test 4: Single Cycle Simulation ---")
    print("  Simulating: and x5, x1, x2 (R-type)")
    print("  ALUSrc = 0 (use RD2 from register)")
    print("  MemtoReg = 0 (write ALU result to register)")
    print("  PCSrc = 0 (next PC = PC + 4)")
    
    # Test get_output
    print("\n--- Test 5: Get Output ---")
    alu_src_mux.select_src_b(0xAAAAAAAA, 0x000000FF, 0)
    print(f"  Last output: 0x{alu_src_mux.get_output():08X}")
    
    # Test reset
    print("\n--- Test 6: Reset ---")
    alu_src_mux.reset()
    print(f"  After reset, output = {alu_src_mux.get_output()}")
    
    print("\n" + "=" * 60)
    print("All multiplexer tests Done")
    print("=" * 60)
    