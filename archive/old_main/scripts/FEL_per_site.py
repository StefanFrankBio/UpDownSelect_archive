import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile")
    parser.add_argument("-o", "--outfile")
    return parser.parse_args()

def main():
    args = parse_args()
    data = pd.read_csv(args.infile, sep='\t')
    data['FEL_category'] = 'neutral'
    data.loc[data['alpha'] > data['beta'], 'FEL_category'] = 'negative'
    data.loc[data['beta'] > data['alpha'], 'FEL_category'] = 'positive'
    output_data = data[['p-value', 'FEL_category']]
    output_data = output_data.rename(columns={'p-value': 'FEL_p_value'})
    output_data.insert(0, 'site', range(0, len(output_data)))
    output_data.to_csv(args.outfile, sep='\t', index=False)

if __name__ == "__main__":
    main()