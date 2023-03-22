import argparse
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" )
    return parser.parse_args()

def read_fasta(filepath, multi=False):
    if multi:
        return list(SeqIO.parse(filepath, "fasta"))
    else:
        return next(SeqIO.parse(filepath, "fasta"))
    
def main():
    args = parse_args()
    outfile_name = ''.join(args.file.split('_')[:2])
    fasta = read_fasta(args.file, multi=True)
    fasta[0].id = 'chromosome'
    fasta[0].name = ''
    fasta[0].description = ''
    for i, record in enumerate(fasta[1:]):
        record.id = f"plasmid_{i}"
        record.name = ''
        record.description = ''
    SeqIO.write(fasta, f'{outfile_name}.fna', 'fasta')

if __name__ == '__main__':
    main()