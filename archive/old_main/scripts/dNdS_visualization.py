import pandas as pd
import matplotlib.pyplot as plt

# Load dataframe
df = pd.read_csv('dNdS.tsv', sep='\t', header=0)
df.dropna(inplace=True)
df.sort_values(by='count', inplace=True, ascending=False)
print(df)
# Create scatterplot
df.plot(x='count', y='mean', kind='scatter', s=2)

# Add title and axis labels
plt.title('Scatterplot of count vs. mean')
plt.xlabel('count')
plt.ylabel('mean')

plt.xlim(0, 2500)
plt.ylim(0, 7)

# Show plot
plt.show()