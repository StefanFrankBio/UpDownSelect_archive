import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dNdS_per_site" )
    parser.add_argument("-f", "--FEL_per_site" )
    parser.add_argument("-s", "--SLAC_per_site" )
    parser.add_argument("-o", "--output" )
    return parser.parse_args()

args = parse_args()
file1 = pd.read_csv(args.dNdS_per_site, sep="\t")
file2 = pd.read_csv(args.FEL_per_site, sep="\t")
file3 = pd.read_csv(args.SLAC_per_site, sep="\t")
merged = pd.merge(file1, file2, on="site")
merged = pd.merge(merged, file3, on="site")
merged.to_csv(args.output, sep="\t", index=False)
