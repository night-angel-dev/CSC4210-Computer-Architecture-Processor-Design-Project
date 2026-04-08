"""
evaluator.py - Validates simplified expression against original truth table
Compares the simplified Boolean expression with the original truth table
"""

class ExpressionEvaluator:
    
    @staticmethod
    def evaluate_expression(expression, inputs, num_vars):
        """
        Evaluate a Boolean expression for given input values.
        This is a simplified evaluator that handles basic SOP expressions.
        
        @param expression - String containing Boolean expression (SOP form)
        @param inputs - Tuple of input values (0/1)
        @param num_vars - Number of variables
        @return - Output value (0 or 1)
        """
        # Handle special cases
        if expression == "0":
            return 0
        if expression == "1":
            return 1
        
        # Create variable mapping
        var_names = [chr(65 + i) for i in range(num_vars)]  # A, B, C, ...
        var_map = {}
        for i, var in enumerate(var_names):
            var_map[var] = inputs[i] # A = 1 or 0
            var_map[var + "'"] = 1 - inputs[i]  # Complemented variable (1-A = 1 or 0)
        
        # Split expression into terms (SOP: terms separated by +)
        # Remove spaces and split by +
        expression = expression.replace(" ", "")
        terms = expression.split('+')
        
        # Evaluate each term (AND of literals)
        for term in terms:
            # Evaluate term: product of literals
            term_result = 1
            # Parse term into literals (each literal is 1-2 chars: A, A', B, B', etc.)
            i = 0
            while i < len(term):
                if i + 1 < len(term) and term[i+1] == "'":
                    # Complemented literal (e.g., A')
                    literal = term[i:i+2]
                    i += 2
                else:
                    # Regular literal (e.g., A)
                    literal = term[i]
                    i += 1
                
                # Look up the value
                if literal in var_map:
                    term_result &= var_map[literal]
                else:
                    # Unknown literal - assume 1 (should not happen)
                    pass
                
                # If term_result becomes 0, no need to check remaining literals
                if term_result == 0:
                    break
            
            # If any term evaluates to 1, the whole expression is 1 (OR)
            if term_result == 1:
                return 1
        
        return 0
    
    @staticmethod
    def validate(truth_table, simplified_expression):
        """
        Compare simplified expression with original truth table.
        
        @param truth_table - TruthTable object with original data
        @param simplified_expression - String containing simplified Boolean expression
        @return - Tuple (result_string, details_string)
        """
        print("\n" + "=" * 50)
        print("VALIDATION")
        print("=" * 50)
        
        all_match = True
        details = []
        
        # Iterate through all rows in truth table
        for i, (inputs, expected_output) in enumerate(truth_table.rows):
            # Evaluate simplified expression for these inputs
            calculated_output = ExpressionEvaluator.evaluate_expression(
                simplified_expression, inputs, truth_table.num_vars
            )
            
            # Compare
            match = (calculated_output == expected_output)
            all_match = all_match and match
            
            # Create binary string for display
            binary_str = ''.join(str(bit) for bit in inputs)
            
            # Store details
            status = "[PASS]" if match else "[FAIL]"
            details.append(f"  {status} {binary_str} -> Expected: {expected_output}, Got: {calculated_output}")
        
        # Print validation summary
        print(f"\nSimplified Expression: {simplified_expression}")
        print(f"\nValidation Results:")
        for detail in details:
            print(detail)
        
        print("\n" + "-" * 50)
        if all_match:
            print("RESULT: PASS")
            print("The simplified expression matches the original truth table for all inputs.")
        else:
            print("RESULT: FAIL")
            print("The simplified expression does NOT match the original truth table.")
        print("=" * 50)
        
        return "PASS" if all_match else "FAIL"


# Simple test function
if __name__ == "__main__":
    print("Testing ExpressionEvaluator...\n")
    
    # Create a simple truth table for 2-variable AND gate
    from truth_table import TruthTable
    
    # AND gate truth table
    and_rows = [
        ((0, 0), 0),
        ((0, 1), 0),
        ((1, 0), 0),
        ((1, 1), 1)
    ]
    
    tt = TruthTable(2, and_rows)
    
    # Test with correct simplified expression
    print("Test 1: Correct simplification (AND gate = AB)")
    ExpressionEvaluator.validate(tt, "AB")
    
    print("\n" + "=" * 60 + "\n")
    
    # Test with incorrect expression
    print("Test 2: Incorrect simplification (OR gate instead of AND)")
    ExpressionEvaluator.validate(tt, "A+B")
    
    print("\n" + "=" * 60 + "\n")
    
    # Test with 3-variable XOR-like function
    xor_rows = [
        ((0, 0, 0), 0),
        ((0, 0, 1), 1),
        ((0, 1, 0), 1),
        ((0, 1, 1), 0),
        ((1, 0, 0), 1),
        ((1, 0, 1), 0),
        ((1, 1, 0), 0),
        ((1, 1, 1), 1)
    ]
    
    tt2 = TruthTable(3, xor_rows)
    print("Test 3: 3-variable XOR-like function with correct expression")
    ExpressionEvaluator.validate(tt2, "A'B'C + A'BC' + AB'C' + ABC")