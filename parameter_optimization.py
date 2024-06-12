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
                    "-n", n_val, 
                    "-M", m_val, 
                    "-T", cpu_count, 
                    "-o", stacks_folder, 
                    "--samples", samples_path,
                    "--popmap", popmap_path],
                    check=True)
    
    subprocess.run(["populations", 
                    "-t", cpu_count, 
                    "--in_path", stacks_folder, 
                    "--out_path", pop_folder, 
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
    return max(results, key=results.get)

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

    results = run_optimization(cpu_count, args, val_m=best_val_m)
    results[best_val_m] = loci_best_val
    best_val_n = find_best_val(results)

    best_params = "m3n" + str(best_val_n) + "M" + str(best_val_m)
    
    output_file = "best_params.txt"
    with open(output_file, 'w') as file:
        file.write(best_params)