import argparse
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" )
    parser.add_argument("-o", "--output") 
    return parser.parse_args()

def main():
    args = parse_args()
    with open(args.file, 'r') as infile, open(args.output, 'w') as outfile:
        for row in infile:
            my_string = row.replace(': ', '\t')
            my_string = my_string.split('\t')
            my_string[0] = re.sub(r'\W+', '_', my_string[0])
            my_string = '\t'.join(my_string).rstrip()
            print(my_string, file=outfile)

if __name__ == '__main__':
    main()