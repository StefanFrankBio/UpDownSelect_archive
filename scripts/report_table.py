import pandas as pd

df1 = pd.read_csv('data/temp/genes.temp', header=0, names=['gene'])
df2 = pd.read_csv('data/reports/meme_report.tsv', sep='\t', header=None, names=['gene', 'meme'])
df3 = pd.read_csv('data/reports/fel_report.tsv', sep='\t', header=None, names=['gene', 'fel'])
df4 = pd.read_csv('data/reports/slac_report.tsv', sep='\t', header=None, names=['gene', 'slac'])
df5 = pd.read_csv('data/reports/cml_report.tsv', sep='\t', header=None, names=['gene', 'codeml'])
df_merged = pd.merge(df1, df2, on='gene', how='left')
df_merged = pd.merge(df_merged, df3, on='gene', how='left')
df_merged = pd.merge(df_merged, df4, on='gene', how='left')
df_merged = pd.merge(df_merged, df5, on='gene', how='left')
df_merged.to_csv('data/reports/report_table.tsv', sep='\t', index=False)
df_no_NaN = df_merged.dropna()
df_no_NaN.to_csv('data/reports/report_table_no_NaN.tsv', sep='\t', index=False)