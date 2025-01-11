import argparse
import pandas

parser = argparse.ArgumentParser(description='Generate KML file from CSV file')
parser.add_argument('csv_file', type=str, help='CSV file to be converted to KML')

args = parser.parse_args()

print(f"Loading file {args.csv_file} ...")

data = pandas.read_csv(args.csv_file)