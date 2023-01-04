import pandas as pd
import glob

filenames = glob.glob('data/dNdS/*.dnds')
out_df = pd.DataFrame([], columns=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
genes = []
for file in filenames:
    genes.append(file.split('/')[-1].split('.')[0])
    df = pd.read_table(file, sep='\t', header=0)
    filtered_df = df.query("status == 'passed'")['dN/dS']
    out_df.loc[len(out_df)] = filtered_df.describe()

out_df.insert(0, 'gene', genes)
out_df.sort_values(by='mean', ascending=False, inplace=True)

out_df.to_csv('dNdS.report', sep='\t', index=False)