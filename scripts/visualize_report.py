import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("data/reports/report_table_no_NaN.tsv", sep="\t")

# Create a scatter plot
plt.scatter(df["meme"], df["fel"], c=df["codeml"], cmap="coolwarm")
plt.xlabel("MEME")
plt.ylabel("FEL")
plt.title("MEME vs FEL with Codeml values as color")
plt.colorbar()
plt.show()