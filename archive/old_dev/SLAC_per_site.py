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
    lower_pval = data[['P [dN/dS > 1]', 'P [dN/dS < 1]']].min(axis=1)
    new_data = pd.DataFrame({'site': range(len(data)), 'SLAC_p_value': lower_pval, 'SLAC_category': 'neutral'})
    new_data.loc[lower_pval == data['P [dN/dS > 1]'], 'SLAC_category'] = 'positive'
    new_data.loc[lower_pval == data['P [dN/dS < 1]'], 'SLAC_category'] = 'negative'
    new_data.loc[lower_pval == data[['P [dN/dS > 1]', 'P [dN/dS < 1]']].max(axis=1), 'SLAC_category'] = 'neutral'
    new_data.to_csv(args.outfile, sep='\t', index=False)

if __name__ == "__main__":
    main()