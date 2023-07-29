import argparse
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile")
    parser.add_argument("-d", "--identifier")
    parser.add_argument("-o", "--outfile")
    return parser.parse_args()

def read_fasta(filepath, multi=False):
    if multi:
        return list(SeqIO.parse(filepath, "fasta"))
    else:
        return next(SeqIO.parse(filepath, "fasta"))
    
def find_substring_indices(seq):
    substrings = "TAA|TAG|TGA"
    
    matches = re.finditer(substrings, seq)
    indices = [match.start() for match in matches]
    
    return sorted(indices)

def split_by_modulo(lst):
    outlist = [[] for i in range(3)]
    for i in lst:
        outlist[i % 3].append(i)
    return outlist

def match_stop_positions(lst):
    results = []
    for i in lst:
        results.extend(list(zip(i, i[1:])))
    return results

def main():
    args = parse_args()
    fasta = read_fasta(args.infile, multi=True)
    ss_orfs = []
    for f in fasta:
        seq = str(f.seq)
        stop_positions = find_substring_indices(seq)
        stop_positions_by_frame = split_by_modulo(stop_positions)
        stops = match_stop_positions(stop_positions_by_frame)
        ss_orfs.extend([seq[x+3:y] for x,y in stops if y-x > 100])
    ss_orfs = [seq for seq in ss_orfs if all(char in 'ACGT' for char in seq)]
    seq_records = [SeqRecord(Seq(seq), id=f"{args.identifier}_{i}", description="") for i, seq in enumerate(ss_orfs)]
    SeqIO.write(seq_records, args.outfile, "fasta")

if __name__ == '__main__':
    main()