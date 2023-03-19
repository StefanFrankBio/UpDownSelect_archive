import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", nargs='+')
    parser.add_argument("-o", "--outdir")
    return parser.parse_args()

def main():
    args = parse_args()
    report_files = args.files

    first_file = report_files.pop(0)
    df_merged = pd.read_csv(first_file, sep='\t', header=None)
    df_merged.columns = ['gene', first_file[:-11]]

    for file_name in report_files:
        df = pd.read_csv(file_name, sep='\t', header=None, names=['gene', file_name[:-11]])
        df_merged = pd.merge(df_merged, df, on='gene', how='outer')

    abritamr_col = 'data/reports/abritamr'
    if abritamr_col in df_merged.columns:
        df_merged[abritamr_col].fillna('BASE', inplace=True)

    df_merged.to_csv(f'{args.outdir}/report_table.tsv', sep='\t', index=False)

    df_no_NaN = df_merged.dropna()
    df_no_NaN.to_csv(f'{args.outdir}/report_table_no_NaN.tsv', sep='\t', index=False)

if __name__ == '__main__':
    main()