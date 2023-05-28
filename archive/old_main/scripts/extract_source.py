import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" )
    return parser.parse_args()

args = parse_args()
with open(args.file, 'r') as infile:
    for line in infile:
        if line.startswith("chromosome") or line.startswith("plasmid"):
            fields = line.split('\t')
            gene = fields[0].split('_')[0]
            if fields[8].startswith('ID='):
                ident = fields[8].split(';')[0].replace('ID=', '')
                print(f'{ident}\t{gene}')