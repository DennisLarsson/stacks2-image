import unittest
from unittest.mock import patch, MagicMock
import argparse
from ..parameter_optimization import check_R80_val, grep, create_folder_names, find_best_val, run_optimization

class TestParameterOptimization(unittest.TestCase):
    @patch('parameter_optimization.run_denovo_map_nm')
    def test_run_optimization(self, mock_run_denovo_map_nm):
        # Mock the inputs
        cpu = 4
        args = argparse.Namespace()
        args.min_val = 1
        args.max_val = 4
        args.popmap = "/path/to/popmap"
        val_m = 2

        # Mock the run_denovo_map_nm function to return a string
        mock_run_denovo_map_nm.return_value = "10"

        # Call the function
        result = run_optimization(cpu, args, val_m)

        # Check the result
        expected_result = {1: 10, 3: 10, 4: 10}
        self.assertEqual(result, expected_result)

    def test_find_best_val(self):
        # Mock the inputs
        results = {1: 10, 2: 30, 3: 20}

        # Call the function
        result = find_best_val(results)

        # Check the result
        self.assertEqual(result, 2)
    
    def test_create_folder_names(self):
        # Mock the inputs
        n_val = 3
        m_val = 4
        results = create_folder_names(n_val, m_val)

        #Define the expected results
        expected_results = ("stacks_m3n3M4", "populations_m3n3M4")

        # Check the result
        self.assertEqual(results, expected_results)

    def test_grep(self):
        # Mock the inputs
        file_path = "populations_m3n3M4/populations.log"
        search_text = "Kept"

        # Call the function
        result = grep(file_path, search_text)

        # Check the result
        self.assertEqual(result, "Kept 1234 loci blablabla\n")

    def test_check_R80_val(self):
        # Mock the inputs
        n_val = 3
        m_val = 4

        # Call the function
        result = check_R80_val(n_val, m_val)

        # Check the result
        self.assertEqual(result, "1234")


if __name__ == '__main__':
    unittest.main()