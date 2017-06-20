import csv
import argparse
import itertools

from thermo_utils import csv_row_writer, read_csv_rows

# Read input/output arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o','--output',required=True)
parser.add_argument('-d','--dof',required=True)
# parser.add_argument('-v','--version',required=False)
args = parser.parse_args()


# Write all rows to equations CSV file
csv_row_writer(args.output,outRows)
print('Output file: %s' % args.output)
