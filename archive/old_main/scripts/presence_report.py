import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" )
    parser.add_argument("-o", "--output" )
    parser.add_argument("-c", "--count" )
    return parser.parse_args()

args = parse_args()
with open(args.file, 'r') as infile, open(args.output, 'w') as outfile:
    for line in infile:
        fields = line.split('\t')
        print(f'{fields[0]}\t{(len(fields)-1)/int(args.count)}', file=outfile)