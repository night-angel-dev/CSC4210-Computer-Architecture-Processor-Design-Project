"""
karnaugh_map.py - Generates and simplifies Boolean expressions using Karnaugh Maps
Supports 2, 3, and 4 variable K-maps
"""

class KarnaughMap:
    def __init__(self, truth_table):
        """
        Initialize K-map from a truth table.
        
        @param truth_table - TruthTable object with rows and num_vars
        """
        self.truth_table = truth_table
        self.num_vars = truth_table.num_vars
        self.map = None
        self.cell_positions = None
        self.prime_implicants = []
        self.simplified_expression = None
        
        # Build the K-map
        self._build_kmap()
    
    def _build_kmap(self):
        """
        Build the K-map grid based on number of variables.
        Structures:
        - 2 vars: 2x2 grid
        - 3 vars: 2x4 grid (rows: 0,1; cols: 00,01,11,10)
        - 4 vars: 4x4 grid (rows: 00,01,11,10; cols: 00,01,11,10)
        """
        if self.num_vars == 2:
            self._build_2var_kmap()
        elif self.num_vars == 3:
            self._build_3var_kmap()
        elif self.num_vars == 4:
            self._build_4var_kmap()
        else:
            raise ValueError("K-map only supports 2, 3, or 4 variables")
    
    def _build_2var_kmap(self):
        """Build 2x2 K-map: rows: 0,1; cols: 0,1"""
        # Gray code order: 00, 01, 11, 10
        # For 2 vars, order: 00, 01, 11, 10
        self.map = [[None for _ in range(2)] for _ in range(2)]
        self.cell_positions = {}
        
        # Mapping: (row, col) -> binary string
        # Row 0: A=0, Row 1: A=1
        # Col 0: B=0, Col 1: B=1
        for row in range(2):
            for col in range(2):
                binary = f"{row}{col}"
                output = self._get_output_for_binary(binary)
                self.map[row][col] = output
                self.cell_positions[binary] = (row, col)
    
    def _build_3var_kmap(self):
        """Build 2x4 K-map: rows: 0,1; cols: 00,01,11,10"""
        self.map = [[None for _ in range(4)] for _ in range(2)]
        self.cell_positions = {}
        
        # Column order in Gray code: 00, 01, 11, 10
        col_order = ["00", "01", "11", "10"]
        
        for row in range(2):  # A variable (row)
            for col_idx, col_bits in enumerate(col_order):  # B,C variables (col)
                binary = f"{row}{col_bits}"
                output = self._get_output_for_binary(binary)
                self.map[row][col_idx] = output
                self.cell_positions[binary] = (row, col_idx)
    
    def _build_4var_kmap(self):
        """Build 4x4 K-map: rows: 00,01,11,10; cols: 00,01,11,10"""
        self.map = [[None for _ in range(4)] for _ in range(4)]
        self.cell_positions = {}
        
        # Gray code order for both axes: 00, 01, 11, 10
        gray_order = ["00", "01", "11", "10"]
        
        for row_idx, row_bits in enumerate(gray_order):  # A,B variables (row)
            for col_idx, col_bits in enumerate(gray_order):  # C,D variables (col)
                binary = f"{row_bits}{col_bits}"
                output = self._get_output_for_binary(binary)
                self.map[row_idx][col_idx] = output
                self.cell_positions[binary] = (row_idx, col_idx)
    
    def _get_output_for_binary(self, binary):
        """
        Get the output value for a given binary input combination.
        
        @param binary - String of bits (e.g., "101")
        @return - Output value (0 or 1)
        """
        inputs = tuple(int(bit) for bit in binary)
        
        # Pad with leading zeros if needed (should already be correct length)
        if len(inputs) < self.num_vars:
            inputs = (0,) * (self.num_vars - len(inputs)) + inputs
        
        # Find matching row in truth table
        for row_inputs, output in self.truth_table.rows:
            if row_inputs == inputs:
                return output
        
        return 0  # Default if not found
    
    def display(self):
        """
        Print the K-map in a readable format.
        """
        print("\n" + "=" * 50)
        print(f"KARNAUGH MAP ({self.num_vars} variables)")
        print("=" * 50)
        
        if self.num_vars == 2:
            print("\n        B=0   B=1")
            print("      +-----+-----+")
            for row in range(2):
                print(f"A={row}   |  {self.map[row][0]}  |  {self.map[row][1]}  |")
                print("      +-----+-----+")
        
        elif self.num_vars == 3:
            print("\n        BC=00  BC=01  BC=11  BC=10")
            print("      +------+------+------+------+")
            for row in range(2):
                var_label = f"A={row}"
                print(f"{var_label}   |  {self.map[row][0]}   |  {self.map[row][1]}   |  {self.map[row][2]}   |  {self.map[row][3]}   |")
                print("      +------+------+------+------+")
        
        elif self.num_vars == 4:
            print("\n        CD=00  CD=01  CD=11  CD=10")
            print("      +------+------+------+------+")
            gray_order = ["00", "01", "11", "10"]
            for row_idx in range(4):
                var_label = f"AB={gray_order[row_idx]}"
                print(f"{var_label} |  {self.map[row_idx][0]}   |  {self.map[row_idx][1]}   |  {self.map[row_idx][2]}   |  {self.map[row_idx][3]}   |")
                print("      +------+------+------+------+")
    
    def simplify(self):
        """
        Simplify the Boolean expression using the K-map.
        Groups adjacent 1's in powers of 2 (1,2,4,8,16).
        
        @return - Simplified Boolean expression in SOP form
        """
        # Find all cells with output 1
        ones = []
        for binary, (row, col) in self.cell_positions.items():
            if self._get_cell_value(row, col) == 1:
                ones.append((binary, row, col))
        
        if not ones:
            self.simplified_expression = "0"
            return "0"
        
        # Cover all ones with prime implicants
        covered = set()
        prime_implicants = []
        
        # Try largest groups first (2^n cells)
        group_sizes = self._get_possible_group_sizes()
        
        for size in group_sizes:
            groups = self._find_groups_of_size(size, ones)
            for group in groups:
                # Check if this group covers any uncovered 1's
                group_cells = set(group)
                if not group_cells.issubset(covered):
                    # Add this prime implicant
                    prime_implicants.append(group)
                    covered.update(group_cells)
        
        # Convert prime implicants to Boolean expression
        terms = []
        for group in prime_implicants:
            term = self._group_to_expression(group)
            if term and term not in terms:
                terms.append(term)
        
        # Sort terms for consistent output
        terms.sort()
        
        if not terms:
            self.simplified_expression = "0"
        elif len(terms) == 1:
            self.simplified_expression = terms[0]
        else:
            self.simplified_expression = " + ".join(terms)
        
        return self.simplified_expression
    
    def _get_cell_value(self, row, col):
        """Get value at K-map cell."""
        if 0 <= row < len(self.map) and 0 <= col < len(self.map[0]):
            return self.map[row][col]
        return 0
    
    def _get_possible_group_sizes(self):
        """Return group sizes in descending order (largest first)."""
        max_cells = 2 ** self.num_vars
        sizes = []
        size = max_cells
        while size >= 1:
            sizes.append(size)
            size //= 2
        return sizes
    
    def _find_groups_of_size(self, size, ones):
        """
        Find all groups of adjacent cells of given size that contain only 1's.
        
        @param size - Number of cells in group (1,2,4,8,16)
        @param ones - List of (binary, row, col) tuples
        @return - List of groups, each group is list of (row, col) tuples
        """
        groups = []
        rows = len(self.map)
        cols = len(self.map[0])
        
        # For size 1, each 1 is its own group
        if size == 1:
            for _, row, col in ones:
                groups.append([(row, col)])
            return groups
        
        # For larger groups, check all possible rectangles
        # The number of rows in group must divide size
        for group_rows in range(1, rows + 1):
            if size % group_rows != 0:
                continue
            group_cols = size // group_rows
            
            if group_cols > cols:
                continue
            
            # Check all starting positions (with wrap-around)
            for start_row in range(rows):
                for start_col in range(cols):
                    group = []
                    valid = True
                    
                    # Build the group cells (with wrap-around)
                    for dr in range(group_rows):
                        r = (start_row + dr) % rows
                        for dc in range(group_cols):
                            c = (start_col + dc) % cols
                            
                            # Check if this cell is a 1
                            if self._get_cell_value(r, c) != 1:
                                valid = False
                                break
                            
                            group.append((r, c))
                        if not valid:
                            break
                    
                    # Also need to check rectangular shape (no holes)
                    if valid and len(group) == size:
                        # Check if this is a valid rectangle (not L-shaped)
                        if self._is_rectangle(group, group_rows, group_cols):
                            # Sort for consistent comparison
                            group.sort()
                            if group not in groups:
                                groups.append(group)
        
        return groups
    
    def _is_rectangle(self, group, expected_rows, expected_cols):
        """
        Check if group forms a valid rectangle.
        
        @param group - List of (row, col) tuples
        @param expected_rows - Expected number of rows
        @param expected_cols - Expected number of columns
        @return - True if rectangle, False otherwise
        """
        if len(group) != expected_rows * expected_cols:
            return False
        
        rows = set(r for r, _ in group)
        cols = set(c for _, c in group)
        
        # Check that rows are contiguous (considering wrap)
        if len(rows) != expected_rows:
            return False
        
        # Check that cols are contiguous (considering wrap)
        if len(cols) != expected_cols:
            return False
        
        return True
    
    def _group_to_expression(self, group):
        """
        Convert a group of K-map cells to a Boolean term.
        
        @param group - List of (row, col) tuples
        @return - String like "AB" or "A'B" or "C"
        """
        if not group:
            return None
        
        # Determine which variables are constant in this group
        # For 2 variables: A (row), B (col)
        # For 3 variables: A (row), B (col high bit), C (col low bit)
        # For 4 variables: A,B (row bits), C,D (col bits)
        
        # Get all binary strings for cells in group
        binary_strings = []
        for row, col in group:
            # Find the binary string for this cell
            for binary, (r, c) in self.cell_positions.items():
                if r == row and c == col:
                    binary_strings.append(binary)
                    break
        
        if not binary_strings:
            return None
        
        # Determine which bits are constant
        if self.num_vars == 2:
            var_names = ['A', 'B']
            bits_per_var = 1
            
            # Convert binary strings to list of bits
            bits_lists = [[int(bit) for bit in s] for s in binary_strings]
            
        elif self.num_vars == 3:
            var_names = ['A', 'B', 'C']
            bits_per_var = 1
            
            bits_lists = [[int(bit) for bit in s] for s in binary_strings]
            
        elif self.num_vars == 4:
            var_names = ['A', 'B', 'C', 'D']
            bits_per_var = 1
            
            bits_lists = [[int(bit) for bit in s] for s in binary_strings]
        
        else:
            return None
        
        # Build the term
        term_parts = []
        for var_idx in range(self.num_vars):
            # Check if this variable is constant across all cells
            values = [bits[var_idx] for bits in bits_lists]
            
            if all(v == 1 for v in values):
                # Always 1 -> include variable uncomplemented
                term_parts.append(var_names[var_idx])
            elif all(v == 0 for v in values):
                # Always 0 -> include variable complemented
                term_parts.append(var_names[var_idx] + "'")
            # else: variable varies -> omit from term
        
        if not term_parts:
            return "1"  # Group covers all cells
        
        return ''.join(term_parts)
    
    def get_simplified_expression(self):
        """
        Return the simplified expression.
        Calls simplify() if not already done.
        """
        if self.simplified_expression is None:
            self.simplify()
        return self.simplified_expression


# Simple test function
if __name__ == "__main__":
    from truth_table import TruthTable
    
    print("Testing KarnaughMap...\n")
    
    # Test 1: 2-variable AND gate (A*B)
    print("Test 1: 2-variable AND gate")
    and_rows = [
        ((0, 0), 0),
        ((0, 1), 0),
        ((1, 0), 0),
        ((1, 1), 1)
    ]
    tt1 = TruthTable(2, and_rows)
    kmap1 = KarnaughMap(tt1)
    kmap1.display()
    result1 = kmap1.simplify()
    print(f"\nSimplified expression: {result1}")
    print(f"Expected: AB\n")
    
    # Test 2: 2-variable OR gate (A+B)
    print("\n" + "=" * 60)
    print("Test 2: 2-variable OR gate")
    or_rows = [
        ((0, 0), 0),
        ((0, 1), 1),
        ((1, 0), 1),
        ((1, 1), 1)
    ]
    tt2 = TruthTable(2, or_rows)
    kmap2 = KarnaughMap(tt2)
    kmap2.display()
    result2 = kmap2.simplify()
    print(f"\nSimplified expression: {result2}")
    print(f"Expected: A + B\n")
    
    # Test 3: 3-variable function (A'B'C + A'BC' + AB'C' + ABC)
    print("\n" + "=" * 60)
    print("Test 3: 3-variable XOR-like function")
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
    tt3 = TruthTable(3, xor_rows)
    kmap3 = KarnaughMap(tt3)
    kmap3.display()
    result3 = kmap3.simplify()
    print(f"\nSimplified expression: {result3}")
    
    # Test 4: 4-variable function (majority function - output 1 when at least 3 inputs are 1)
    print("\n" + "=" * 60)
    print("Test 4: 4-variable Majority function (at least 3 ones)")
    majority_rows = [
        ((0,0,0,0), 0),
        ((0,0,0,1), 0),
        ((0,0,1,0), 0),
        ((0,0,1,1), 0),
        ((0,1,0,0), 0),
        ((0,1,0,1), 0),
        ((0,1,1,0), 0),
        ((0,1,1,1), 1),
        ((1,0,0,0), 0),
        ((1,0,0,1), 0),
        ((1,0,1,0), 0),
        ((1,0,1,1), 1),
        ((1,1,0,0), 0),
        ((1,1,0,1), 1),
        ((1,1,1,0), 1),
        ((1,1,1,1), 1)
    ]
    tt4 = TruthTable(4, majority_rows)
    kmap4 = KarnaughMap(tt4)
    kmap4.display()
    result4 = kmap4.simplify()
    print(f"\nSimplified expression: {result4}")
    print(f"Expected: ABC + ABD + ACD + BCD (or similar)")
    