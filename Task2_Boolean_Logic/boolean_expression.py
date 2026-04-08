"""
boolean_expression.py - responsible for boolean expression generation.
Convrts a truth table to canonical SOP/POS forms and minterm/maxterm lists
"""

# importing binary_utils from Task 1
import sys
import os

# Get the directory of current file 
current_dir = os.path.dirname(os.path.abspath(__file__))

# Goes up one level and into Task 1 folder
task1_path = os.path.join(current_dir, "..", "Task1_Data_Systems")

# Add to path
if task1_path not in sys.path:
    sys.path.insert(0, task1_path)

try:
    from binary_utils import decimal_to_padded_binary, decimal_to_binary
    # print("Import is a success")
    
except ImportError as e:
    print(f"Import from Task1 failed: {e}")



class BooleanExpression:
    
    def __init__(self, truth_table):
        """
        Initializes with a TruthTable object
        
        @param truth_table - TruthTable object containing minterms/maxterms
        """
        self.tt = truth_table
        
        # Generatre variable names (A, B, C, ...)
        self.vars = [chr(65 + i) for i in range(self.tt.num_vars)]
        pass
    
    
    def get_canonical_sop(self):
        """
        Generate Sum of Products form from minterms.
        
        Example: 1 (001), 2 (010), 4 (100), 7 (111) = A'B'C + A'BC' + AB'C' + ABC
        
        @return - String containing SOP expression
        """
        
        if not self.tt.minterms:
            return "0"
        
        terms = []
        
        for minterm in self.tt.minterms:
            
            # Convert minterm to binary and pad to match variable count
            binary = decimal_to_padded_binary(minterm, self.tt.num_vars)
            
            # Create terms like A'B'C
            term = ''
            
            for i, bit in enumerate(binary):
                if bit == '1':
                    term += self.vars[i]
                else:
                    term += self.vars[i] + "'" # Complement variable A'
            terms.append(term)
            
        return " + ".join(terms)
        
    
    def get_canonical_pos(self):
        """
        Generate produdct of susm form from maxterms
        
        Example: 0(000), 3(011), 5(101), 6(110) = (A+B+C)(A+B'+C')(A'+B+C')(A'+B'+C)
        
        @return - String containg POS expression
        """
        
        if not self.tt.maxterms:
            return "1"
        
        terms = []
        
        for maxterm in self.tt.maxterms:
            
            # Convert maxterm to binary and pad to match variable count
            binary = decimal_to_padded_binary(maxterm, self.tt.num_vars)
            
            term = '('
            
            for i, bit in enumerate(binary):
                if bit == '0': # POS: 0 means variable, 1 means complement
                    term += self.vars[i]
                
                else:
                    term += self.vars[i] + "'"
                    
                if i < self.tt.num_vars - 1:
                    term += '+'
            
            term += ')'
            terms.append(term)
                
        return " * ".join(terms) 
        
        
    def get_minterm_list(self):
        """
        Returns minterm list as formatted string in form of 
        m(#, #, #, #)
        """
        
        if not self.tt.minterms:
            return "None"
        
        return f"m({','.join(map(str, self.tt.minterms))})"
    
    
    def get_maxterm_list(self):
        """
        Returns maxterm list as formatted string in the form of
        M(#, #, #, #)
        """
        
        if not self.tt.maxterms:
            return "None"
        
        return f"M({','.join(map(str, self.tt.maxterms))})"
    
    def get_minterms_binary(self):
        """
        Return minterms in binary format, will be useful for kmaps
        
        @return - list of binary strings for each minterm
        """
        if not self.tt.minterms:
            return []
        
        minterms_binary = []
        
        for minterm in self.tt.minterms:
            binary = decimal_to_padded_binary(minterm, self.tt.num_vars)
            minterms_binary.append(binary)
            
        return minterms_binary
        
        
    def get_maxterms_binary(self):
        """
        Return maxterms in binary format.
        
        @return - List of binary strings for each maxterm
        """
        if not self.tt.maxterms:
            return []
        
        maxterms_binary = []
        
        for maxterm in self.tt.maxterms:
            binary = decimal_to_padded_binary(maxterm, self.tt.num_vars)
            maxterms_binary.append(binary)
            
        return maxterms_binary
    
    
        
    
    def __str__(self):
        """
        String showing both SOP & POS
        """
        
        return f"SOP: {self.get_canonical_sop()}\nPOS: {self.get_canonical_pos()}"
        
    
# Test
if __name__ == "__main__":
    
    print("Testing BooleanExpression")
    
    # Test with 3 - variable XOR function 
    test_rows = [
        
        ((0, 0, 0), 0), # 0
        ((0, 0, 1), 1), # 1
        ((0, 1, 0), 1), # 2
        ((0, 1, 1), 0), # 3
        ((1, 0, 0), 1), # 4
        ((1, 0, 1), 0), # 5
        ((1, 1, 0), 0), # 6
        ((1, 1, 1), 1)  # 7
    ]
    
    from truth_table import TruthTable
    tt = TruthTable(3, test_rows)
    be = BooleanExpression(tt)
    
    print("-" * 30)
    print("SOP: \n")
    print(be.get_canonical_sop())
    print("\n")
    
    print("-" * 30)
    print("POS: \n")
    print(be.get_canonical_pos())
    print("\n")
    
    print("-" * 30)
    print("Minterm List: \n")
    print(be.get_minterm_list())
    print("\n")
    
    print("-" * 30)
    print("Maxterm List: \n")
    print(be.get_maxterm_list())
    print("\n")
    
    print("-" * 30)
    print("Minterms Binary: \n")
    print(be.get_minterms_binary())
    print("\n")
    
    print("-" * 30)
    print("Maxterms Binary: \n")
    print(be.get_maxterms_binary())
    print("\n")
    
    print("-" * 30)
    print("__str__ (String showing both SOP & POS): \n")
    print(be)
    print("\n")
    
    # Test Case where all outputs = 1
    print("-" * 30)
    print("Test Case All 1's: \n")
    all_ones = [((0,0), 1), ((0,1), 1), ((1,0), 1), ((1,1), 1)]
    tt2 = TruthTable(2, all_ones)
    be2 = BooleanExpression(tt2)
    print(f"SOP: {be2.get_canonical_sop()}") # Expected: AB' + AB + ... (all products)
    print(f"POS: {be2.get_canonical_pos()}") # Expected: 1
    print(f"Maxterms: {be2.get_maxterm_list()}") # Expected: None
    
    
    # Test Case where all outputs = 0
    print("\n" + "-" * 30)
    print("Test Case All 0's: \n")
    all_zeros = [((0,0), 0), ((0,1), 0), ((1,0), 0), ((1,1), 0)]
    tt3 = TruthTable(2, all_zeros)
    be3 = BooleanExpression(tt3)
    print(f"SOP: {be3.get_canonical_sop()}") # Expected: 0
    print(f"POS: {be3.get_canonical_pos()}") # Expected: all maxterms
    print(f"Minterms: {be3.get_minterm_list()}") # Expected: None
    