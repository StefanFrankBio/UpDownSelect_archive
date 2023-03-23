import argparse
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file" )
    return parser.parse_args()

def main():
    args = parse_args()
    with open(args.file, 'r') as infile:
        for row in infile:
            my_string = row.replace(': ', '\t')
            my_string = my_string.split('\t')
            my_string[0] = re.sub(r'\W+', '_', my_string[0])
            my_string = '\t'.join(my_string).rstrip()
            print(my_string)

if __name__ == '__main__':
    main()