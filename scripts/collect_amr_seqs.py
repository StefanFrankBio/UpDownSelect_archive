import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile")
    parser.add_argument("-d", "--identifier")
    parser.add_argument("-o", "--outdir")
    return parser.parse_args()

def main():
    args = parse_args()
    with open(args.infile) as infile:
        data = json.load(infile)
    for feature in data['features']:
        gene = feature.get('expert', {}).get('amrfinder', {}).get('gene')
        if gene:
            gene = gene.replace('/', '_')
            with open(f'{args.outdir}/{gene}.fasta', 'a+') as outfile:
                print(f'>{args.identifier}', file=outfile)
                print(feature['nt'], file=outfile)

if __name__ == '__main__':
    main()
    