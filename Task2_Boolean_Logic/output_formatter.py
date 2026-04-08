"""
output_formatter.py - Formats and prints all required outputs in the specified order.
Required Output Order:
1. Truth table
2. Canonical equation (SOP or POS)
3. Minterm/Maxterm list
4. K-Map grouping
5. Simplified Boolean expression
6. Validation result (PASS/FAIL)
"""

class OutputFormatter:
    
    def __init__(self, truth_table, boolean_expr, karnaugh_map, evaluator_result=None):
        """
        Initialize the output formatter with all required components.
        
        @param truth_table - TruthTable object
        @param boolean_expr - BooleanExpression object
        @param karnaugh_map - KarnaughMap object
        @param evaluator_result - Tuple (result_string, details_string) from evaluator
        """
        self.truth_table = truth_table
        self.boolean_expr = boolean_expr
        self.karnaugh_map = karnaugh_map
        self.evaluator_result = evaluator_result
    
    def print_all(self):
        """
        Print all outputs in the required order.
        """
        self.print_truth_table()
        self.print_canonical_equations()
        self.print_minterms_maxterms()
        self.print_kmap()
        self.print_simplified_expression()
        self.print_validation()
    
    def print_truth_table(self):
        """
        Print the truth table in a formatted table.
        """
        print("\n" + "=" * 50)
        print("TRUTH TABLE")
        print("=" * 50)
        
        # Generate variable names (A, B, C, D, ...)
        var_names = [chr(65 + i) for i in range(self.truth_table.num_vars)]
        
        # Print header
        header = " | ".join(var_names) + " | Output"
        print(header)
        print("-" * len(header))
        
        # Print each row
        for inputs, output in self.truth_table.rows:
            row_str = " | ".join(str(bit) for bit in inputs) + f" |   {output}"
            print(row_str)
    
    def print_canonical_equations(self):
        """
        Print the canonical SOP and POS forms.
        """
        print("\n" + "=" * 50)
        print("CANONICAL EQUATIONS")
        print("=" * 50)
        
        # Get SOP and POS from boolean_expression object
        sop = self.boolean_expr.get_canonical_sop()
        pos = self.boolean_expr.get_canonical_pos()
        
        print(f"Sum of Products (SOP): {sop}")
        print(f"Product of Sums (POS): {pos}")
    
    def print_minterms_maxterms(self):
        """
        Print minterm and maxterm lists.
        """
        print("\n" + "=" * 50)
        print("MINTERMS AND MAXTERMS")
        print("=" * 50)
        
        minterms = self.boolean_expr.get_minterm_list()
        maxterms = self.boolean_expr.get_maxterm_list()
        
        print(f"Minterms (1-outputs): {minterms}")
        print(f"Maxterms (0-outputs): {maxterms}")
        
        # Print binary representations
        minterms_binary = self.boolean_expr.get_minterms_binary()
        maxterms_binary = self.boolean_expr.get_maxterms_binary()
        
        if minterms_binary:
            print(f"Minterms (binary): {', '.join(minterms_binary)}")
        if maxterms_binary:
            print(f"Maxterms (binary): {', '.join(maxterms_binary)}")
    
    def print_kmap(self):
        """
        Print the Karnaugh Map.
        """
        self.karnaugh_map.display()
    
    def print_simplified_expression(self):
        """
        Print the simplified Boolean expression.
        """
        print("\n" + "=" * 50)
        print("SIMPLIFIED BOOLEAN EXPRESSION")
        print("=" * 50)
        
        simplified = self.karnaugh_map.get_simplified_expression()
        print(f"Simplified SOP: {simplified}")
    
    def print_validation(self):
        """
        Print validation results from evaluator.
        """
        print("\n" + "=" * 50)
        print("VALIDATION RESULT")
        print("=" * 50)
        
        if self.evaluator_result:
            # Check if evaluator_result is a tuple (result, details) or just a string
            if isinstance(self.evaluator_result, tuple) and len(self.evaluator_result) >= 2:
                result_str = self.evaluator_result[0]
                details = self.evaluator_result[1]
                print(f"Result: {result_str}")
                if details:
                    print(f"\nDetails:\n{details}")
            else:
                # Fallback if it's just a string
                print(f"Result: {self.evaluator_result}")
        else:
            print("Result: NOT RUN")


# Simple test function
if __name__ == "__main__":
    print("Testing OutputFormatter...\n")
    
    # Create a simple truth table for 2-variable AND gate
    from truth_table import TruthTable
    from boolean_expression import BooleanExpression
    from karnaugh_map import KarnaughMap
    
    and_rows = [
        ((0, 0), 0),
        ((0, 1), 0),
        ((1, 0), 0),
        ((1, 1), 1)
    ]
    
    tt = TruthTable(2, and_rows)
    bool_expr = BooleanExpression(tt)
    kmap = KarnaughMap(tt)
    
    formatter = OutputFormatter(tt, bool_expr, kmap)
    formatter.print_all()