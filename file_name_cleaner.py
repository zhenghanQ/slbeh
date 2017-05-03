import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dest', type=str, help="directory where data are")
parser.add_argument('-t', '--dtype', type=int, help="0 for adults, 1 for kids, 2 for both")
args=parser.parse_args()
dest = args.dest
dtype = args.dtype

def file_cleaner_kids(data_dir):
    for f in os.listdir(data_dir):
        if not (f[:4].isdigit() and f[4] == '_'):
            if f[4] == 'n':
                new_name = f[0:4] + '_' + f[-7:]
                os.rename(
                    os.path.join(data_dir, f),
                    os.path.join(data_dir, new_name)
                )
    pass

def file_cleaner_adults(data_dir):
    for f in os.listdir(data_dir):
        if not(f[:3].upper() == 'SLA' and f[3:5].isdigit() and f[5] == '_'):
            if f[5] == 'n' or f[5:9] == 'real':
                new_name = 'SLA' + f[3:5] + '_' + f[-7:]
                os.rename(
                    os.path.join(data_dir, f),
                    os.path.join(data_dir, new_name)
                )
    pass

if dtype:
    if dtype > 1:
        file_cleaner_kids(dest)
        file_cleaner_adults(dest)
    else:
        file_cleaner_kids(dest)
else:
    file_cleaner_adults(dest)
