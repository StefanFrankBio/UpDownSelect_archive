#!/usr/bin/env python3
import os
import argparse
import json
import itertools
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import re
from collections import Counter
from scipy.stats import binomtest, chisquare
import numpy as np
np.seterr(invalid='ignore')

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DEFAULT_CODON_TABLE_PATH = BASE_DIR + '/' + 'resources/default_codon_table.json'
# DEFAULT_SITE_COUNTS_PATH = BASE_DIR + '/' + 'resources/default_site_counts.json'
# DEFAULT_SUB_COUNTS_PATH = BASE_DIR + '/' + 'resources/default_sub_counts.json'

DEFAULT_CODON_TABLE_PATH = 'resources/default_codon_table.json'
DEFAULT_SITE_COUNTS_PATH = 'resources/default_site_counts.json'
DEFAULT_SUB_COUNTS_PATH = 'resources/default_sub_counts.json'

def site_counts(codon_table, outfile):
    with open(codon_table, 'r') as infile:
        codon_dict = json.load(infile)
    keys = codon_dict.keys()
    alphabet = {char for string in keys for char in string}
    site_counts_dict = {}
    for codon in keys:
        subs = single_substitutions(codon, alphabet)
        NS = sum([codon_dict[sub] != codon_dict[codon] for sub in subs]) / len(subs)
        SS = 1 - NS
        NS_rounded = round(NS, 3)
        SS_rounded = round(SS, 3)
        site_counts_dict[codon] = (NS_rounded, SS_rounded)
    with open(outfile, 'w') as outfile:
        json.dump(site_counts_dict, outfile, indent=4)

def single_substitutions(codon, alphabet):
    substitutions = []
    for i, base in enumerate(codon):
        for new_base in alphabet:
            if base != new_base:
                new_codon = codon[:i] + new_base + codon[i+1:]
                substitutions.append(new_codon)
    return substitutions

def sub_counts(codon_table, outfile):
    with open(codon_table, 'r') as infile:
        codon_dict = json.load(infile)
    keys = codon_dict.keys()
    codon_pairs = list(itertools.product(keys, repeat=2))
    sub_counts_dict = {}
    for r, v in codon_pairs:
        subs = [r[:i] + v[i] + r[i+1:] for i in range(3) if r[i] != v[i]]
        NS = sum([codon_dict[sub] != codon_dict[r] for sub in subs])
        SS = len(subs) - NS
        sub_counts_dict.setdefault(r, {})[v] = (NS, SS)
        sub_counts_dict[r]['---'] = (0,0)
    with open(outfile, 'w') as outfile:
        json.dump(sub_counts_dict, outfile, indent=4)

def transpose(infile):
    msa = list(SeqIO.parse(infile, "fasta"))
    codons_by_seq = []
    for record in msa:
        codons_by_seq.append(re.findall(r'...', str(record.seq)))
    codons_by_site = list(map(list, zip(*codons_by_seq)))
    transpose_dict = {}
    for i, site in enumerate(codons_by_site):
        count = Counter(site)
        count['---'] = 0
        sorted_counts = sorted(count.items(), key=lambda x: (-x[1], x[0]))
        transpose_dict[i] = sorted_counts
    return transpose_dict

def consensus(transpose_dict, outfile=False):
    consensus = ''.join([val[0][0] for val in transpose_dict.values()])
    consensus = Seq(consensus)
    consensus = SeqRecord(consensus, id='consensus', description='')
    if outfile:
        with open("output.fasta", "w") as output_file:
            SeqIO.write(consensus, outfile, "fasta")
    else:
        return consensus

def per_sequence(infile, outfile, site_counts, sub_counts, ref_file=False):
    if ref_file:
        reference = next(SeqIO.parse(ref_file, "fasta"))
    else:
        reference = consensus(transpose(infile))
    variants = list(SeqIO.parse(infile, "fasta"))

    with open(site_counts, 'r') as infile:
        site_counts_dict = json.load(infile)

    with open(sub_counts, 'r') as infile:
        sub_counts_dict = json.load(infile)

    ref_codons = re.findall(r'...', str(reference.seq))
    N = sum(site_counts_dict[codon][0] for codon in ref_codons)
    S = sum(site_counts_dict[codon][1] for codon in ref_codons)

    with open(outfile, 'w') as outfile:
        print('id', 'N', 'S', 'NS', 'SS', 'dNdS', file=outfile, sep='\t')
        for variant in variants:
            var_codons = re.findall(r'...', str(variant.seq))
            NS = 0
            SS = 0
            for ref, var in zip(ref_codons, var_codons):
                subs = sub_counts_dict[ref][var]
                NS += subs[0]
                SS += subs[1]
            try:
                print(variant.id, N, S, NS, SS, (NS/N)/(SS/S), file=outfile, sep='\t')
            except ZeroDivisionError:
                print(variant.id, N, S, NS, SS, file=outfile, sep='\t')

def per_site(infile, outfile, site_counts, sub_counts, codon_table):
    transpose_dict = transpose(infile)
    with open(site_counts, 'r') as infile:
        site_counts_dict = json.load(infile)

    with open(sub_counts, 'r') as infile:
        sub_counts_dict = json.load(infile)

    with open(codon_table, 'r') as infile:
        codon_dict = json.load(infile)

    with open(outfile, 'w') as outfile:
        print('site', 'codon', 'aa', 'total_subs', 'NS', 'SS', 'N', 'S', 'binom_p_value', 'chi2_p_value', file=outfile, sep='\t')
        print(transpose_dict)
        for key, value in transpose_dict.items():
            ref_codon = value[0][0]
            ref_aa = codon_dict[ref_codon]
            N = site_counts_dict[ref_codon][0]
            S = site_counts_dict[ref_codon][1]
            NS = 0
            SS = 0
            for v in value:
                NS += sub_counts_dict[ref_codon][v[0]][0] * v[1]
                SS += sub_counts_dict[ref_codon][v[0]][1] * v[1]
            
            total_subs = NS + SS
            
            if total_subs == 0:
                NS_rounded = 0
                SS_rounded = 0
                binom_p_value = 1
                chi2_p_value = 1
            else:
                NS_rounded = round(NS / total_subs, 3)
                SS_rounded = round(1 - NS_rounded, 3)
                binom_results = binomtest(NS, total_subs, N)
                binom_p_value = round(binom_results.pvalue, 3)
                _ , chi2_p_value = chisquare([NS_rounded, SS_rounded], [N, S])
                chi2_p_value = round(chi2_p_value, 3)
                if ref_codon in ['ATG', 'TGG']:
                    chi2_p_value = 1.0

            print(key, ref_codon, ref_aa, total_subs, NS_rounded, SS_rounded, N, S, binom_p_value, chi2_p_value, file=outfile, sep='\t')

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    
    site_counts_parser = subparsers.add_parser('site_counts')
    site_counts_parser.add_argument('-c', '--codon_table', default=DEFAULT_CODON_TABLE_PATH)
    site_counts_parser.add_argument('-o', '--outfile')
    
    sub_counts_parser = subparsers.add_parser('sub_counts')
    sub_counts_parser.add_argument('-c', '--codon_table', default=DEFAULT_CODON_TABLE_PATH)
    sub_counts_parser.add_argument('-o', '--outfile')

    per_sequence_parser = subparsers.add_parser('per_sequence')
    per_sequence_parser.add_argument('-i', '--infile', required=True)
    per_sequence_parser.add_argument('-o', '--outfile', default='per_seq.tsv')
    per_sequence_parser.add_argument('-s', '--site-counts', default=DEFAULT_SITE_COUNTS_PATH)
    per_sequence_parser.add_argument('-u', '--sub-counts', default=DEFAULT_SUB_COUNTS_PATH)
    per_sequence_parser.add_argument('-r', '--reference')

    per_site_parser = subparsers.add_parser('per_site')
    per_site_parser.add_argument('-i', '--infile', required=True)
    per_site_parser.add_argument('-o', '--outfile', default='per_site.tsv')
    per_site_parser.add_argument('-s', '--site-counts', default=DEFAULT_SITE_COUNTS_PATH)
    per_site_parser.add_argument('-u', '--sub-counts', default=DEFAULT_SUB_COUNTS_PATH)
    per_site_parser.add_argument('-c', '--codon_table', default=DEFAULT_CODON_TABLE_PATH)

    consensus_parser = subparsers.add_parser('consensus')
    consensus_parser.add_argument('-i', '--infile', required=True)
    consensus_parser.add_argument('-o', '--outfile')

    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == 'site_counts':
        site_counts(args.codon_table, args.outfile)
    elif args.command == 'sub_counts':
        sub_counts(args.codon_table, args.outfile)
    elif args.command == 'per_sequence':
        per_sequence(args.infile, args.outfile, args.site_counts, args.sub_counts)
    elif args.command == 'per_site':
        per_site(args.infile, args.outfile, args.site_counts, args.sub_counts, args.codon_table)
    elif args.command == 'consensus':
        consensus(transpose(args.infile), args.outfile)

if __name__ == '__main__':
    main()