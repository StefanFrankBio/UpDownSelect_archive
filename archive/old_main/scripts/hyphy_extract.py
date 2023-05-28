import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" )
    parser.add_argument("-g", "--gene")
    parser.add_argument("-m", "--metric")
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.file, sep='\t')
    if args.metric == 'meme':
        min_val = df.iloc[:, 6].min()
    elif args.metric == 'fel':
        min_val = df.iloc[:, 4].min()
    elif args.metric == 'slac':
        min_val = df.iloc[:, 9].min()
    print(args.gene, min_val, sep='\t')

if __name__ == '__main__':
    main()