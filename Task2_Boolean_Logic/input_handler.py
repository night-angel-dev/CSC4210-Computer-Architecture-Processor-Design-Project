"""
input_handler.py - Handles user input and truth table collection
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
    from binary_utils import binary_to_hexadecimal, decimal_to_padded_binary, binary_addition, decimal_to_binary
    # print("Import is a success")
    
except ImportError as e:
    print(f"Import from Task1 failed: {e}")


class InputHandler:
    
    @staticmethod
    def get_truth_table():
        """
        Gets truth table from user input.

        @return num_vars - integer number of variables
        @return rows - list of tuples ((inputs), output)
        """
        
        # Header
        print("\n" + "=" * 50)
        print("Truth Table Input")
        print("=" * 50)
        
        # Get number of variables
        while True:
            
            try:
                # Keeping things simple since, for section 2, only function with 2-4 variables will be used
                # to construct a Karnaugh map
                num_vars = int(input("Enter number of input variables (2-4): ")) 
                
                if num_vars >= 2 and num_vars <= 4:
                    break
                else:
                    print("The number entered is not in the range of 2-4, please try again.")
                    
            except ValueError:
                print("Please enter a valid integer.")
        
        # Generate all possible input combinations in order
        rows = []
        total_rows = 2 ** num_vars
        
        print(f"\nEnter the output (0 or 1) for each input combination (Enter just the number):")
        print(f"Total entries needed: {total_rows}")
        print("-" * 40)

        # Loop through each possible input combination
        for i in range(total_rows):
            
            # Convert index to binary string with leading zeros
            binary_str = decimal_to_padded_binary(i, num_vars)
            
            # Convert binary string to tuple of integers, i.e., "101" -> (1,0,1)
            inputs = []
            for bit in binary_str:
                integer_value = int(bit)
                inputs.append(integer_value)
            inputs = tuple(inputs)
            
            # Show current progress
            print(f"\nEntry {i+1}/{total_rows}")
            print(f"Input combination: {binary_str} {inputs}")
            
            # Get output from user with validation
            while True:
                try:
                    output = int(input("Output (0 or 1): "))

                    # validate and add to rows                
                    if output == 0 or output == 1:
                        rows.append((inputs, output))
                        break
                    else:
                        print("Invalid input, please enter 0 or 1")
                        
                except ValueError:
                    print("Invalid input, please enter 0 or 1")
        
        # Print Summary
        print("\n" + "-" * 40)
        print(f"Successfully recorded {total_rows} truth table entries.")
        
        return num_vars, rows


# Test
if __name__ == "__main__":
    num_vars, rows = InputHandler.get_truth_table()
    
    print("\n" + "=" * 50)
    print("Truth Table Summary")
    print("=" * 50)
    
    print(f"Variables: {num_vars}")
    print(f"Rows: {len(rows)}")
    
    print("\nTruth Table: ")
    for inputs, output in rows:
        binary_str = ''.join(str(bit) for bit in inputs)
        print(f"{binary_str} -> {output}")