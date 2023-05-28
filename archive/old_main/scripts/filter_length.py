import os
from Bio import SeqIO

multi_dir = "data/rmdup/"
filtered_dir = "data/filtered_multi/"

if not os.path.exists(filtered_dir):
    os.makedirs(filtered_dir)

for filename in os.listdir(multi_dir):
    if filename.endswith(".fasta") or filename.endswith(".fa"):
        filepath = os.path.join(multi_dir, filename)
        print(f"Processing file: {filepath}")
        records_to_keep = []
        seq_lengths = []
        for seq_record in SeqIO.parse(filepath, "fasta"):
            seq_length = len(seq_record)
            seq_lengths.append(seq_length)
            if abs(seq_length - sum(seq_lengths) / len(seq_lengths)) / (sum(seq_lengths) / len(seq_lengths)) * 100 <= 50:
                records_to_keep.append(seq_record)
        num_removed = len(seq_lengths) - len(records_to_keep)
        if len(records_to_keep) >= 3:
            new_filename = os.path.splitext(filename)[0] + ".fasta"
            new_filepath = os.path.join(filtered_dir, new_filename)
            with open(new_filepath, "w") as output_handle:
                SeqIO.write(records_to_keep, output_handle, "fasta")
            print("Filtered file written to:", new_filepath)
            starting_mean = sum(seq_lengths) / len(seq_lengths)
            ending_mean = sum([len(seq_record) for seq_record in records_to_keep]) / len(records_to_keep)
            print(f"Starting mean length: {starting_mean:.2f}")
            print(f"Ending mean length: {ending_mean:.2f}")
            if num_removed > 0:
                print(f"Number of sequences removed: {num_removed}")
            else:
                print("No sequences were removed from this file.")
        else:
            print("Not enough sequences remaining after filtering.")
