import sys
import subprocess

input_data = sys.stdin.read()
input_data = input_data.strip().split('\t')

input_data[0] = f'data/multi/{input_data[0]}.fasta'
base = '_'.join(input_data[1].split('_')[:2])
input_data[1] = f'data/seqkit/{base}/{input_data[1]}.ffn'

with open(input_data[0], "a") as outfile:
    with open(input_data[1], 'r') as infile:
        print(infile.read(), file=outfile, end='')