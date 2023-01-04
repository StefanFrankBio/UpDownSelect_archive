import argparse
from Bio import SeqIO
import re
import itertools
import statistics

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reference")
    parser.add_argument("-v", "--variant")
    parser.add_argument("-o", "--output")
    return parser.parse_args()

def read_fasta(filepath, multi=False):
    if multi:
        return list(SeqIO.parse(filepath, "fasta"))
    else:
        return next(SeqIO.parse(filepath, "fasta"))

def findall(regex, sequence):
    return re.findall(f"{regex}", sequence)

def single_substitutions(codon):
    substitutions = []
    for i, nt in enumerate(codon):
        possible_subs = ["A", "C", "G", "T"]
        possible_subs.remove(nt)
        for sub in possible_subs:
            substitutions.append(codon[:i] + sub + codon[i+1:])
    return substitutions

def build_trans_table():
    nucs = "TCAG"
    aminos = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
    codons = (itertools.product(nucs, nucs, nucs))
    codons = ["".join(tpl) for tpl in codons]
    return dict(zip(codons, aminos))

def main():
    args = parse_args()
    reference = read_fasta(args.reference)
    ref_seq = str(reference.seq).upper()
    ref_codons = findall('...', ref_seq)
    trans_table = build_trans_table()
    ns_ratios = []
    for codon in ref_codons:
        if 'N' not in codon:
            substitutions = single_substitutions(codon)
            trans_codon = trans_table[codon]
            trans_subs = [trans_table[sub] for sub in substitutions]
            ns_ratios += [tsub == trans_codon for tsub in trans_subs]

    variants = read_fasta(args.variant, multi=True)
    with open(args.output, 'w') as outfile:
        print(*['ID', 'dN/dS', 'dN', 'dS', 'status'], file=outfile, sep='\t')
        for variant in variants:
            var_seq = str(variant.seq)
            internal_gaps_var = var_seq.strip('-').count('-')
            if ref_seq == var_seq:
                print(*[variant.id, -1, 0, 0, 'identical'], file=outfile, sep='\t')
            # elif internal_gaps % 3 != 0:
            # elif internal_gaps_ref - internal_gaps_var != 0:
            #     print(*[variant.id, -1, 0, 0, 'frame_shifted'], file=outfile, sep='\t')
            #     print(reference.id, variant.id, 'frame shifted!')
            else:
                test = [(i, v) for i, (r, v) in enumerate(zip(ref_seq, var_seq)) if r != v and v != '-']
                test2 = []
                for tpl in test:
                    ref_codon = ref_codons[tpl[0]//3]
                    if 'N' not in ref_codon:                        
                        var_codon = ref_codon[:tpl[0]%3] + tpl[1] + ref_codon[tpl[0]%3+1:]
                        test2.append(trans_table[ref_codon] == trans_table[var_codon])
                ns_ratio = statistics.mean(ns_ratios)
                dN = (len(test2)-sum(test2))/(1-ns_ratio)
                dS = sum(test2)/ns_ratio
                if dS:
                    dNdS = dN/dS
                    print(*[variant.id, dNdS, dN, dS, 'passed'], file=outfile, sep='\t')
                else:
                    print(*[variant.id, -1, 0, 0, 'dS = 0'], file=outfile, sep='\t')

if __name__ == '__main__':
    main()