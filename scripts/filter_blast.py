import argparse
import pandas as pd
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile")
    parser.add_argument("-l", "--length_ratio", type=float)
    parser.add_argument("-a", "--amr_seqs")
    parser.add_argument("-o", "--outfile")
    return parser.parse_args()

args = parse_args()
df = pd.read_csv(args.infile, sep="\t", names=["sseqid", "qlen", "length"])
df["len_ratio"] = df["length"] / df["qlen"]
df.sort_values("len_ratio", inplace=True, ascending=False, ignore_index=True)
df = df[df["len_ratio"] >= args.length_ratio]
df.drop_duplicates(subset=["sseqid"], keep="first", inplace=True)

def read_fasta(filepath, multi=False):
    if multi:
        return list(SeqIO.parse(filepath, "fasta"))
    else:
        return next(SeqIO.parse(filepath, "fasta"))
    
amr_seqs = read_fasta(args.amr_seqs, multi=True)
amr_ids = [record.id for record in amr_seqs]
df = df[~df['sseqid'].str.contains('|'.join(amr_ids))]
with open(args.outfile, 'w') as outfile:
    for i in df['sseqid'].tolist():
        print(i, file=outfile)
