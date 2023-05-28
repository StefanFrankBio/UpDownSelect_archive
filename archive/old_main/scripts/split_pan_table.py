import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" )
    parser.add_argument("-o", "--output" )
    return parser.parse_args()

args = parse_args()
with open(args.file, 'r') as infile, open(args.output, 'w') as outfile:
    for line in infile:
        fields = line.strip().split('\t')
        for field in fields[1:]:
            split_field = field.rsplit("_", 1)
            print(f'{fields[0]}\t{split_field[0]}\t_{split_field[1]}', file=outfile)