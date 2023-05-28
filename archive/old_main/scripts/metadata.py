import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    return parser.parse_args()

args = parse_args()
df = pd.read_csv(args.input, sep='\t', header=None, names=['Accession', 'Attribute', 'Value'])
pivoted_df = df.pivot_table(index='Accession', columns='Attribute', values='Value', aggfunc='first')
column_order = ['geo_loc_name', 'host', 'collection_date']
pivoted_df = pivoted_df[column_order]
pivoted_df.to_csv(args.output, sep='\t', header=True)