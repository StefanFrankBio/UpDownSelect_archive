import argparse
import json
import re
from Bio import SeqIO
from Bio.Data import CodonTable

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--consensus" )
    parser.add_argument("-v", "--variant")
    parser.add_argument("-o", "--output")
    return parser.parse_args()

def read_fasta(filepath, multi=False):
    if multi:
        return list(SeqIO.parse(filepath, "fasta"))
    else:
        return next(SeqIO.parse(filepath, "fasta"))

args = parse_args()
consensus = read_fasta(args.consensus)
gene = consensus.id
consensus = str(consensus.seq).upper()
variants = read_fasta(args.variant, multi=True)

json_file_path = 'output.json'
with open('resources/codon_ratios.json', 'r') as file:
    codon_data = json.load(file)
codons_consensus = re.findall(r'...', consensus)
codons_consensus_no_N = [codon for codon in codon_data if 'N' not in codon]
N = sum(codon_data[codon] for codon in codons_consensus_no_N) / len(codons_consensus_no_N)
S = 1 - N

with open(args.output, 'w') as outfile:
    header = ['id', 'N', 'S', 'NS', 'SS', 'dN', 'dS', 'dNdS']
    print('\t'.join(header), file=outfile)
    for variant in variants:
        variant_id = str(variant.id)
        codons_variant = re.findall(r'...', str(variant.seq))

        stop_codons = {'TAA', 'TAG', 'TGA'}
        invalid_characters = {'N', '-'}

        different_codons = [(c1, c1[:i] + c2[i] + c1[i+1:])
                            for c1, c2 in zip(codons_consensus, codons_variant)
                            for i, (b1, b2) in enumerate(zip(c1, c2)) if b1 != b2]
        
        filtered_different_codons = [codon_pair for codon_pair in different_codons
                                    if not (set(codon_pair[0]) & invalid_characters) and not (set(codon_pair[1]) & invalid_characters)
                                    and codon_pair[0] not in stop_codons and codon_pair[1] not in stop_codons]

        different_codons = filtered_different_codons


        standard_table = CodonTable.unambiguous_dna_by_id[1]

        print(gene, variant_id)
        print(different_codons)
        different_amino_acids = [standard_table.forward_table[codon_consensus] != standard_table.forward_table[codon_sequence]
                                 for codon_consensus, codon_sequence in different_codons]


        NS = sum(different_amino_acids)
        SS = len(different_amino_acids) - NS

        dN = NS / N
        dS = SS / S
        if dS == 0:
            dNdS = 'divZero'
        else:
            dNdS = dN / dS
        output_list = [variant_id, N, S, NS, SS, dN, dS, dNdS]
        output_list = [str(i) for i in output_list]

        print('\t'.join(output_list), file=outfile)


