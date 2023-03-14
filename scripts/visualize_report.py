import pandas as pd
import matplotlib.pyplot as plt

# Load the data
# df = pd.read_csv("data/reports/report_table_no_NaN.tsv", sep="\t")

# Create a scatter plot
# plt.scatter(df["meme"], df["fel"], c=df["codeml"], cmap="coolwarm")
# plt.xlabel("MEME")
# plt.ylabel("FEL")
# plt.title("MEME vs FEL with Codeml values as color")
# plt.colorbar()
# plt.show()

# Load your dataframe
df = pd.read_csv("data/reports/report_table_no_NaN.tsv", sep="\t")
abritamr_codes, _ = pd.factorize(df["abritamr"])
abritamr_order = ["BASE", "VIRULENCE", "AMR"]
df["abritamr"] = pd.Categorical(df["abritamr"], categories=abritamr_order)
df = df.sort_values("abritamr")
abritamr_codes, _ = pd.factorize(df["abritamr"])
for i, col1 in enumerate(["meme", "fel", "slac", "codeml"]):
    for j, col2 in enumerate(["meme", "fel", "slac", "codeml"]):
        if i < j:
            # Create the scatter plot
            plt.figure()
            plt.scatter(df[col1], df[col2], c=abritamr_codes)
            plt.xscale("log")
            plt.yscale("log")
            plt.xlabel(col1)
            plt.ylabel(col2)
            cbar = plt.colorbar()
            cbar.set_ticks(range(len(abritamr_order)))
            cbar.set_ticklabels(abritamr_order)
            
            plt.show()