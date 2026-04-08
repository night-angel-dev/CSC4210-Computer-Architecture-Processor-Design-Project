"""
test.py - Unit tests for all modules in the Boolean Expression Simplifier
"""

import unittest
from truth_table import TruthTable
from boolean_expression import BooleanExpression
from karnaugh_map import KarnaughMap
from evaluator import ExpressionEvaluator


class TestTruthTable(unittest.TestCase):
    """Test cases for TruthTable class"""
    
    def test_2var_and(self):
        """Test 2-variable AND gate"""
        rows = [
            ((0, 0), 0),
            ((0, 1), 0),
            ((1, 0), 0),
            ((1, 1), 1)
        ]
        tt = TruthTable(2, rows)
        
        self.assertEqual(tt.num_vars, 2)
        self.assertEqual(tt.minterms, [3])
        self.assertEqual(tt.maxterms, [0, 1, 2])
    
    def test_2var_or(self):
        """Test 2-variable OR gate"""
        rows = [
            ((0, 0), 0),
            ((0, 1), 1),
            ((1, 0), 1),
            ((1, 1), 1)
        ]
        tt = TruthTable(2, rows)
        
        self.assertEqual(tt.minterms, [1, 2, 3])
        self.assertEqual(tt.maxterms, [0])
    
    def test_3var_xor(self):
        """Test 3-variable XOR-like function"""
        rows = [
            ((0, 0, 0), 0),
            ((0, 0, 1), 1),
            ((0, 1, 0), 1),
            ((0, 1, 1), 0),
            ((1, 0, 0), 1),
            ((1, 0, 1), 0),
            ((1, 1, 0), 0),
            ((1, 1, 1), 1)
        ]
        tt = TruthTable(3, rows)
        
        self.assertEqual(tt.minterms, [1, 2, 4, 7])
        self.assertEqual(tt.maxterms, [0, 3, 5, 6])


class TestBooleanExpression(unittest.TestCase):
    """Test cases for BooleanExpression class"""
    
    def test_sop_and(self):
        """Test SOP for AND gate"""
        rows = [((0, 0), 0), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)]
        tt = TruthTable(2, rows)
        be = BooleanExpression(tt)
        
        self.assertEqual(be.get_canonical_sop(), "AB")
    
    def test_sop_or(self):
        """Test SOP for OR gate"""
        rows = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)]
        tt = TruthTable(2, rows)
        be = BooleanExpression(tt)
        
        self.assertEqual(be.get_canonical_sop(), "A'B + AB' + AB")
    
    def test_pos_and(self):
        """Test POS for AND gate"""
        rows = [((0, 0), 0), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)]
        tt = TruthTable(2, rows)
        be = BooleanExpression(tt)
        
        expected = "(A+B) * (A+B') * (A'+B)"
        self.assertEqual(be.get_canonical_pos(), expected)
    
    def test_minterm_list(self):
        """Test minterm list formatting"""
        rows = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)]
        tt = TruthTable(2, rows)
        be = BooleanExpression(tt)
        
        self.assertEqual(be.get_minterm_list(), "m(1,2,3)")
    
    def test_maxterm_list(self):
        """Test maxterm list formatting"""
        rows = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)]
        tt = TruthTable(2, rows)
        be = BooleanExpression(tt)
        
        self.assertEqual(be.get_maxterm_list(), "M(0)")


class TestKarnaughMap(unittest.TestCase):
    """Test cases for KarnaughMap class"""
    
    def test_2var_and_simplify(self):
        """Test K-map simplification for AND gate"""
        rows = [((0, 0), 0), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)]
        tt = TruthTable(2, rows)
        kmap = KarnaughMap(tt)
        
        simplified = kmap.simplify()
        self.assertEqual(simplified, "AB")
    
    def test_2var_or_simplify(self):
        """Test K-map simplification for OR gate"""
        rows = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)]
        tt = TruthTable(2, rows)
        kmap = KarnaughMap(tt)
        
        simplified = kmap.simplify()
        # Could be "A + B" or "B + A"
        self.assertTrue(simplified == "A + B" or simplified == "B + A")
    
    def test_3var_simplify(self):
        """Test K-map simplification for 3-variable function"""
        rows = [
            ((0, 0, 0), 0), ((0, 0, 1), 1),
            ((0, 1, 0), 1), ((0, 1, 1), 0),
            ((1, 0, 0), 1), ((1, 0, 1), 0),
            ((1, 1, 0), 0), ((1, 1, 1), 1)
        ]
        tt = TruthTable(3, rows)
        kmap = KarnaughMap(tt)
        
        simplified = kmap.simplify()
        # This XOR-like function cannot be simplified further
        expected = "A'B'C + A'BC' + AB'C' + ABC"
        self.assertEqual(simplified, expected)


class TestEvaluator(unittest.TestCase):
    """Test cases for ExpressionEvaluator class"""
    
    def test_evaluate_and(self):
        """Test evaluation of AND expression"""
        evaluator = ExpressionEvaluator()
        
        # Test AB expression
        self.assertEqual(evaluator.evaluate_expression("AB", (0, 0), 2), 0)
        self.assertEqual(evaluator.evaluate_expression("AB", (0, 1), 2), 0)
        self.assertEqual(evaluator.evaluate_expression("AB", (1, 0), 2), 0)
        self.assertEqual(evaluator.evaluate_expression("AB", (1, 1), 2), 1)
    
    def test_evaluate_or(self):
        """Test evaluation of OR expression"""
        evaluator = ExpressionEvaluator()
        
        # Test A+B expression
        self.assertEqual(evaluator.evaluate_expression("A+B", (0, 0), 2), 0)
        self.assertEqual(evaluator.evaluate_expression("A+B", (0, 1), 2), 1)
        self.assertEqual(evaluator.evaluate_expression("A+B", (1, 0), 2), 1)
        self.assertEqual(evaluator.evaluate_expression("A+B", (1, 1), 2), 1)
    
    def test_evaluate_complement(self):
        """Test evaluation with complemented variables"""
        evaluator = ExpressionEvaluator()
        
        # Test A'B' expression (NOR)
        self.assertEqual(evaluator.evaluate_expression("A'B'", (0, 0), 2), 1)
        self.assertEqual(evaluator.evaluate_expression("A'B'", (0, 1), 2), 0)
        self.assertEqual(evaluator.evaluate_expression("A'B'", (1, 0), 2), 0)
        self.assertEqual(evaluator.evaluate_expression("A'B'", (1, 1), 2), 0)
    
    def test_validate_pass(self):
        """Test validation passes for correct expression"""
        rows = [((0, 0), 0), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)]
        tt = TruthTable(2, rows)
        evaluator = ExpressionEvaluator()
        
        result = evaluator.validate(tt, "AB")
        self.assertEqual(result, "PASS")  # Check tuple's first element


def run_all_tests():
    """Run all test cases"""
    print("\n" + "=" * 60)
    print("RUNNING UNIT TESTS")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTruthTable))
    suite.addTests(loader.loadTestsFromTestCase(TestBooleanExpression))
    suite.addTests(loader.loadTestsFromTestCase(TestKarnaughMap))
    suite.addTests(loader.loadTestsFromTestCase(TestEvaluator))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n[SUCCESS] All tests passed!")
    else:
        print("\n[FAILURE] Some tests failed.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_all_tests()