import unittest
from unittest.mock import patch, MagicMock
import argparse
import os
from parameter_optimization import check_R80_val, grep, create_folder_names, find_best_val, run_optimization

class TestParameterOptimization(unittest.TestCase):
    @patch('parameter_optimization.run_denovo_map_nm')
    def test_run_optimization(self, mock_run_denovo_map_nm):
        cpu = 4
        args = argparse.Namespace()
        args.min_val = 1
        args.max_val = 4
        args.popmap = "/path/to/popmap"
        val_m = 2

        mock_run_denovo_map_nm.return_value = "10"

        result = run_optimization(cpu, args, val_m)

        expected_result = {1: 10, 3: 10, 4: 10}
        self.assertEqual(result, expected_result)

    def test_find_best_val(self):
        results = {1: 10, 2: 30, 3: 20}

        result = find_best_val(results)

        self.assertEqual(result, 2)
    
    def test_create_folder_names(self):
        n_val = 3
        m_val = 4
        results = create_folder_names(n_val, m_val)

        expected_results = ("stacks_m3n3M4", "populations_m3n3M4")

        self.assertEqual(results, expected_results)

    def test_grep(self):
        file_path = 'tests/populations_m3n3M4/populations.log'
        search_text = "Kept"

        result = grep(file_path, search_text)

        self.assertEqual(result, "Kept 1234 loci blablabla\n")

    def test_check_R80_val(self):
        n_val = 3
        m_val = 4

        cwd = os.getcwd()
        try:
            os.chdir('tests')

            result = check_R80_val(n_val, m_val)

            self.assertEqual(result, "1234")
        finally:
            os.chdir(cwd)
        


if __name__ == '__main__':
    unittest.main()