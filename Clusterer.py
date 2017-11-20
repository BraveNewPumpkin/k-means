import sys
import pandas as pd
from pathlib import Path
from pprint import pprint

usage = 'Clusterer.py number_of_clusters /path/to/input/dataset.csv /path/to/output/file'

if len(sys.argv) < 4:
    print('not enough arguments\n')
    print(usage)
    sys.exit(1)
if len(sys.argv) > 4:
    print('too many arguments\n')
    print(usage)
    sys.exit(1)

def main(argv):
    number_of_clusters = argv[1]
    input_data_path = Path(argv[2])
    output_data_path = Path(argv[3])

    data = pd.read_csv(filepath_or_buffer=input_data_path, delim_whitespace=True)



    with output_data_path.open(mode='w') as output_data_stream:
        data.to_csv(output_data_stream, index=False)

    return 0

main(sys.argv)