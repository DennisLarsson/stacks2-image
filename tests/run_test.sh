#!/bin/bash

./parameter_optimization.py --popmap popmap_test --samples /test_samples/ --min_val 1 --max_val 3

diff best_params.txt expected_best_params.txt
