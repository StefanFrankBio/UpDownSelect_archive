import argparse
import numpy as np
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    parser.add_argument("-g", "--gene")
    return parser.parse_args()

def parse_file(file_path):
    df = pd.read_csv(file_path, sep='\t')
    dNdS_values = df['dNdS'].replace('divZero', np.nan).dropna().astype(float)
    return dNdS_values.tolist()

def main():
    args = parse_args()
    input_file = args.input
    dNdS_values = parse_file(input_file)
    
    if len(dNdS_values) > 0:
        # min_val = min(dNdS_values)
        mean_val = np.mean(dNdS_values)
        # max_val = max(dNdS_values)
        # std_dev = np.std(dNdS_values)
        print(f"{args.gene}\t{mean_val}")

if __name__ == "__main__":
    main()
