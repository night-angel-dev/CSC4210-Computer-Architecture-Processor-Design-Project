"""
truth_table.py - Defines TruthTable class and validates structure and stores minterms/maxterms

"""


class TruthTable:
    
    """
    Initializes a TruthTabel object
    
    @param num_vars - Integer value of number of input variables (n >= 2)
    @param rows - List of tuples (inputs, outputs) values where  
        - inputs: tuple of integers (0 or 1) representing input combinaaton 
        - output: integer (0 or 1) representing function output
            
    Notes:
    - Using tuples for inputs ensures immutabibility meanign they can not be changed accidentally
    - Storing rows as (inputs, output) preserves original order
    
    """
    
    
    def __init__(self, num_vars, rows):
        self.num_vars = num_vars
        self.rows = rows # List of (inputs, output) tuples
        
        # Will stores indices from 0 to 2^n-1 where output is 1 or 0
        self.minterms = [] # Indexes where output = 1
        self.maxterms = [] # Indexes where output = 0
        
        # Process the turht table to extract minterms & maxterms at initialization
        self._process_terms()

        pass
    
    """
    Extracts minterms and mactersm from the truth table rows by iterating through each row
    and categorizing it based on output.
    
    The row index (0 to 2^n-1) represents the minterm/maxterm number
    
    """
    def _process_terms(self):
        
        for i, (inputs, output) in enumerate(self.rows):
            
            if output == 1:
                self.minterms.append(i)
            
            else:
                self.maxterms.append(i)
        
        
        
        pass
    
    
    """
    Verifies that the truth table meets all requirements. 
    
    @return - Returns Boolean True if truth table is valid, False otherwise
        
    Main validation checks:
    - Correct number of rows, must be exactly 2^n
    - All output values are either 0 or 1
    
    Notes:
    This doesnt validate that each input combination appears exaclty once. 
    That will be handled during the input collection since its about input format, not the data itself
    
    """
    def validate(self):
        
        # First check, verifiy row coutn matches 2^n
        expected_rows = 2 ** self.num_vars
        if len(self.rows) != expected_rows:
            return False
        
        # Second check, verify all outputs are binary (0 or 1)
        for inputs, output in self.rows:
            if output not in (0,1):
                return False


        # if we pass both checks, the truth tabel is valid
        return True
        
        pass
    
    
    """
    Get the input combination for a given row index, provides accesa to row data. 
    
    @param index - Integer value representing a row index from 0 to 2^n-1
    @returns - a tuple value, the input combination for that row
    """
    def get_input_combination(self, index):
        
        return self.rows[index][0]
    
    
    """
    Get the output value for a given row index.
    
    @param index - Integer value representing row index between 0 and 2^n-1
    @return - Integer value representing the output (1 or 0)
    
    Note:
    Similar to the above function
    """
    def get_output(self, index):
        
        return self.rows[index][1]
    
    
    def get_minterm_list(self):
        """
        Returns minterm list as formatted string in form of 
        m(#, #, #, #)
        """
        
        if not self.minterms:
            return "None"
        
        return f"m({','.join(map(str, self.minterms))})"

    def get_maxterm_list(self):
        """
        Returns maxterm list as formatted string in the form of
        M(#, #, #, #)
        """
        
        if not self.maxterms:
            return "None"
        
        return f"M({','.join(map(str, self.maxterms))})"
            
        
    """
    Creates a string reperesentation of the truth table
    
    @return - String value of Formatted truth table for dispplay
    """
    def __str__(self):
        
        # Create header with variable names (A, B, C ....)
        variables = [chr(65 + i) for i in range(self.num_vars)]
        
        
        col_width = 1 # 1 or 0 characters
        spacing = 3 # Space between columns
        
        header = " | ".join(variables) + " | F"
        
        # Seperator lines
        separator = "-" * len(header)
        
        
        # create rows
        lines = [header, separator]
        
        for inputs, output in self.rows:
            
            # Convert the tuple of ints to string with spaces
            input_strs = [str(bit).ljust(col_width) for bit in inputs]
            row_str = (" " * spacing).join(input_strs) + f"{' ' * spacing}{output}"
            lines.append(row_str)
        
        return "\n".join(lines)

# Test block
if __name__ == "__main__":
    
    print("Testing TruthTable class: \n")
    
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
    
    truthtable1 = TruthTable(3, test_rows)
    
    print(f"Number of variables: {truthtable1.num_vars}")
    print(f"Validation result: {truthtable1.validate()}")
    print(f"Minterms: {truthtable1.get_minterm_list()}")
    print(f"Maxterms: {truthtable1.get_maxterm_list()}")
    print("\nTruth Table:")
    print(truthtable1)
    

