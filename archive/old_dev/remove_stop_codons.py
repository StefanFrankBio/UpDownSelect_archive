import argparse
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" )
    return parser.parse_args()

def read_fasta(filepath, multi=False):
    if multi:
        return list(SeqIO.parse(filepath, "fasta"))
    else:
        return next(SeqIO.parse(filepath, "fasta"))
    
args = parse_args()
seqs = read_fasta(args.file, multi=True)
for record in seqs:
    record.seq = record.seq[:-3]

with open(args.file, 'w') as outfile:
    SeqIO.write(seqs, outfile, "fasta")