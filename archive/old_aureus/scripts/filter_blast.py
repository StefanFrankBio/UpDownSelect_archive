import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile")
    parser.add_argument("-o", "--outfile")
    return parser.parse_args()

args = parse_args()
df = pd.read_csv(args.infile, sep="\t", names=["sseqid", "qlen", "length", "pident"])
df["len_ident"] = df["length"] / df["qlen"] * df["pident"]
df.sort_values("len_ident", inplace=True, ascending=False, ignore_index=True)
df = df[df['len_ident'] >= 70]
seq_ids = df['sseqid'].to_list()
with open(args.outfile, 'w') as outfile:
    for i in seq_ids:
        print(i, file=outfile)
