import argparse
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    return parser.parse_args()

def read_fasta(filepath, multi=False):
    if multi:
        return list(SeqIO.parse(filepath, "fasta"))
    else:
        return next(SeqIO.parse(filepath, "fasta"))
    
def main():
    args = parse_args()
    msa = read_fasta(args.input, multi=True)
    for i, _ in enumerate(msa):
        msa[i].seq = msa[i].seq[:-3]

    SeqIO.write(msa, args.output, "fasta")

if __name__ == '__main__':
    main()