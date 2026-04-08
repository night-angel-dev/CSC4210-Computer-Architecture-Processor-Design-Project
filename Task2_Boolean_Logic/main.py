"""
main.py - Main program flow for Boolean Expression Simplifier
Ties together all modules: input_handler, boolean_expression, 
karnaugh_map, evaluator, and output_formatter
"""

from truth_table import TruthTable
from input_handler import InputHandler
from boolean_expression import BooleanExpression
from karnaugh_map import KarnaughMap
from evaluator import ExpressionEvaluator
from output_formatter import OutputFormatter


def main():
    """
    Main program flow:
    1. Get truth table from user (interactive input)
    2. Create TruthTable object
    3. Generate canonical SOP and POS forms
    4. Generate K-map and simplify expression
    5. Validate simplified expression against original truth table
    6. Output all results in required format
    """
    print("\n" + "=" * 60)
    print("BOOLEAN EXPRESSION SIMPLIFIER")
    print("Supports 2, 3, or 4 variables")
    print("=" * 60)
    
    while True:
        print("\n" + "-" * 40)
        
        # Step 1: Get truth table from user
        handler = InputHandler()
        num_vars, rows = handler.get_truth_table()
        
        if num_vars is None:
            print("Error: Could not create truth table.")
            return
        
        # Step 2: Create TruthTable object (THIS WAS MISSING)
        truth_table = TruthTable(num_vars, rows)
        
        # Step 3: Generate canonical forms
        bool_expr = BooleanExpression(truth_table)
        
        # Step 4: Generate K-map and simplify
        kmap = KarnaughMap(truth_table)
        simplified = kmap.get_simplified_expression()
        
        # Step 5: Validate simplified expression
        evaluator = ExpressionEvaluator()
        result = evaluator.validate(truth_table, simplified)
        
        # Step 6: Output everything
        formatter = OutputFormatter(truth_table, bool_expr, kmap, result)
        formatter.print_all()
        
        # Ask user if they want to continue
        print("\n" + "-" * 40)
        again = input("Would you like to simplify another truth table? (y/n): ").strip().lower()
        if again != 'y':
            print("\nThank you for using the Boolean Expression Simplifier!")
            break


if __name__ == "__main__":
    main()