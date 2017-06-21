import csv

# Write out csv file, from list input
def write_csv_rows(out_file,in_list):
    with open(out_file, 'wt') as csvfile:
        write_csv = csv.writer(csvfile, delimiter=',',
                              quotechar="'", quoting=csv.QUOTE_MINIMAL)
        for row in in_list:
            write_csv.writerow(row)

# Read in csv as list
def read_csv_rows(in_file):
    result = []
    with open(in_file, 'rt') as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar="'")
        for row in rows:
            result.append(','.join(row))
    return result
