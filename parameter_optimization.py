#!/bin/python3

import subprocess
import multiprocessing
import argparse
import os


def create_folder_names(n_val, m_val):
    stacks_folder = "stacks_m3n" + str(n_val) + "M" + str(m_val)
    pop_folder = "populations_m3n" + str(n_val) + "M" + str(m_val)
    return stacks_folder, pop_folder

def grep(file_path, search_text):
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if search_text in line:
                return line
    return None

def create_directories(dir_path):
    os.makedirs(dir_path)

def run_denovo_map_nm(n_val, m_val, cpu_count, samples_path, popmap_path):
    stacks_folder, pop_folder = create_folder_names(n_val, m_val)
    create_directories(stacks_folder)
    create_directories(pop_folder)

    subprocess.run(["denovo_map.pl", 
                    "-n", str(n_val), 
                    "-M", str(m_val), 
                    "-T", str(cpu_count), 
                    "-o", stacks_folder, 
                    "--samples", samples_path,
                    "--popmap", popmap_path],
                    check=True)
    
    subprocess.run(["populations", 
                    "-t", str(cpu_count), 
                    "--in-path", stacks_folder, 
                    "--out-path", pop_folder, 
                    "--popmap", popmap_path, 
                    "-R", "0.8"], 
                    check=True)
    
    R80_val = check_R80_val(n_val, m_val)  
    return R80_val

def check_R80_val(n_val, m_val):
    _, pop_folder = create_folder_names(n_val, m_val)
    pop_file = pop_folder + "/populations.log"
    R80_val = grep(pop_file, "Kept").split(" ")[1]
    return R80_val

def find_best_val(results):
    sorted_results = sorted(results.items())
    
    for i in range(len(sorted_results) - 1):
        current_value = sorted_results[i][1]
        next_value = sorted_results[i + 1][1]

        increase = ((next_value - current_value) / current_value)

        if increase < 0.05:
            return sorted_results[i][0]
        
    return sorted_results[-1][0]


def run_optimization(cpu, args, val_m=None):
    results = {}
    for val in range(args.min_val, args.max_val + 1):
        if val_m is None:
            R80_val = run_denovo_map_nm(val, val, cpu, args.samples, args.popmap)
        else:
            if val == val_m:
                continue
            R80_val = run_denovo_map_nm(val, val_m, cpu, args.samples, args.popmap)
        
        results[val] = int(R80_val)
    return results

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Run denovo_map.pl and populations for different n and m values")
    argparser.add_argument("--popmap", help="Path to the population map file")
    argparser.add_argument("--samples", help="Path to the samples file")
    argparser.add_argument("--cpu", type=int, help="Number of CPUs to use", default="1")
    argparser.add_argument("--min_val", type=int, help="Minimum value for n and m", default=1)
    argparser.add_argument("--max_val", type=int, help="Maximum value for n and m", default=7)
    args = argparser.parse_args()

    if args.cpu:
        cpu_count = args.cpu
    else:
        cpu_count = multiprocessing.cpu_count()

    results = run_optimization(cpu_count, args, val_m=None)
    best_val_m = find_best_val(results)
    loci_best_val = results[best_val_m]

    output_file = "param_vals_nm.txt"
    with open(output_file, 'w') as file:
        file.write(str(results) + "\n")

    results = run_optimization(cpu_count, args, val_m=best_val_m)
    results[best_val_m] = loci_best_val
    best_val_n = find_best_val(results)

    output_file = "param_vals_n.txt"
    with open(output_file, 'w') as file:
        file.write(str(results) + "\n")

    best_params_path = "stacks_m3n" + str(best_val_n) + "M" + str(best_val_m)
    
    output_file = "best_params_path.txt"
    with open(output_file, 'w') as file:
        file.write(best_params_path)
