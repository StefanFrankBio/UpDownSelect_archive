import argparse
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile")
    parser.add_argument("-o", "--order")
    return parser.parse_args()

def main():
    args = parse_args()
    records = list(SeqIO.parse(args.infile, 'fasta'))
    record_dict = {record.id: record for record in records}

    with open(args.order, 'r') as order_file:
        sequence_order = [line.strip() for line in order_file]

    with open(args.infile, 'w') as output_fasta:
        for header in sequence_order:
            SeqIO.write(record_dict[header], output_fasta, 'fasta')

if __name__ == '__main__':
    main()



