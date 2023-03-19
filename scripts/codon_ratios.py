import argparse
import itertools
import json

codons = [''.join(x) for x in itertools.product('ACGT', repeat=3)]
codon_to_aa = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
}

def get_substitutions(codon):
    substitutions = []
    for i, base in enumerate(codon):
        for new_base in 'ACGT':
            if base != new_base:
                new_codon = codon[:i] + new_base + codon[i+1:]
                substitutions.append(new_codon)
    return substitutions

def calculate_ratios():
    ratios = {}
    for codon in codons:
        subs = get_substitutions(codon)
        same_aa_count = sum(1 for sub in subs if codon_to_aa[codon] == codon_to_aa[sub])
        ratio = same_aa_count / len(subs)
        ratios[codon] = ratio
    return ratios

def main(output_path):
    ratios = calculate_ratios()
    with open(output_path, "w") as outfile:
        json.dump(ratios, outfile, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    main(args.output)