import argparse
import csv
import json

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" )
    parser.add_argument("-o", "--output")
    parser.add_argument("-m", "--metric")
    return parser.parse_args()

def main():
    args = parse_args()
    with open(args.file) as json_file:
        data = json.load(json_file)
    
    headers = data['MLE']['headers']
    
    if args.metric == 'meme' or args.metric == 'fel':
        content = data['MLE']['content']
        with open(args.output, mode='w', newline='') as tsv_file:
            writer = csv.writer(tsv_file, delimiter='\t')
            writer.writerow([header[0] for header in headers])
            for row in content['0']:
                writer.writerow(row)
    
    elif args.metric == 'slac':
        content = data['MLE']['content']['0']['by-site']
        with open(args.output, mode='w', newline='') as tsv_file:
            writer = csv.writer(tsv_file, delimiter='\t')
            writer.writerow([header[0] for header in headers])
            for row in content['AVERAGED']:
                writer.writerow(row)
    else:
        pass

if __name__ == '__main__':
    main()