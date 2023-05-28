import argparse
import re
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pan_table" )
    parser.add_argument("-s", "--source_table" )
    parser.add_argument("-o", "--output")    
    return parser.parse_args()

args = parse_args()
dicty = defaultdict(list)
with open(args.pan_table, 'r') as pan_table, open(args.source_table, 'r') as source_table:
    sources = source_table.read()
    split_sources = re.split(r'[\t\n]', sources)
    for line in pan_table:
        fields = line.rstrip().split('\t')
        idents = fields[1:]
        for ident in idents:
            num = split_sources.index(ident)
            dicty[fields[0]].append(split_sources[num-1])

for key in dicty:
    if 'chromosome' in dicty[key] and 'plasmid' in dicty[key]:
        dicty[key] = 'mixed'
    elif 'chromosome' in dicty[key]:
        dicty[key] = 'chromosome'
    elif 'plasmid' in dicty[key]:
        dicty[key] = 'plasmid'

with open(args.output, 'w') as outfile:
    for key, value in dicty.items():
        outfile.write(f'{key}\t{value}\n')
