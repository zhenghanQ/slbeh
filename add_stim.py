import os
import pandas as pd
import numpy as np
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data', type=str, help="directory where data are")
parser.add_argument('-t', '--dtype', type=int, help=" interger value, 0 for combined SQL file, 1 for seperate files")
parser.add_argument('-o', '--out', type=str, help="output directory for modified files")
args=parser.parse_args()
data = args.data
dtype = args.dtype
out = args.out

tsl_f = [
4,5,6,1,2,3,10,11,12,7,8,9,1,2,3,7,8,9,10,11,12,4,5,6,1,2,3,
10,11,12,7,8,9,1,2,3,4,5,6,10,11,12,7,8,9,4,5,6,10,11,12,7,8,
9,1,2,3,4,5,6,10,11,12,1,2,3,7,8,9,10,11,12,7,8,9,4,5,6,1,2,3,
10,11,12,7,8,9,4,5,6,7,8,9,1,2,3,4,5,6,10,11,12,1,2,3,4,5,6,7,
8,9,4,5,6,7,8,9,1,2,3,10,11,12,4,5,6,7,8,9,10,11,12,1,2,3,4,5,
6,10,11,12,1,2,3,7,8,9,1,2,3,10,11,12,4,5,6,1,2,3,4,5,6,10,11,
12,7,8,9,10,11,12,1,2,3,7,8,9,4,5,6,1,2,3,4,5,6,10,11,12,7,8,
9,4,5,6,10,11,12,7,8,9,1,2,3,4,5,6,10,11,12,1,2,3,7,8,9,1,2,3,
10,11,12,7,8,9,4,5,6,7,8,9,4,5,6,1,2,3,10,11,12,7,8,9,10,11,12,
1,2,3,4,5,6,1,2,3,10,11,12,7,8,9,4,5,6,10,11,12,7,8,9,1,2,3,4,
5,6,1,2,3,10,11,12,7,8,9,4,5,6,4,5,6,1,2,3,10,11,12,7,8,9,1,2,3,
7,8,9,10,11,12,4,5,6,1,2,3,10,11,12,7,8,9,1,2,3,4,5,6,10,11,12,
7,8,9,4,5,6,10,11,12,7,8,9,1,2,3,4,5,6,10,11,12,1,2,3,7,8,9,10,
11,12,7,8,9,4,5,6,1,2,3,10,11,12,7,8,9,4,5,6,7,8,9,1,2,3,4,5,6,
10,11,12,1,2,3,4,5,6,7,8,9,4,5,6,7,8,9,1,2,3,10,11,12,4,5,6,7,
8,9,10,11,12,1,2,3,4,5,6,10,11,12,1,2,3,7,8,9,1,2,3,10,11,12,
4,5,6,1,2,3,4,5,6,10,11,12,7,8,9,10,11,12,1,2,3,7,8,9,4,5,6,1,
2,3,4,5,6,10,11,12,7,8,9,4,5,6,10,11,12,7,8,9,1,2,3,4,5,6,10,
11,12,1,2,3,7,8,9,1,2,3,10,11,12,7,8,9,4,5,6,7,8,9,4,5,6,1,2,3,
10,11,12,7,8,9,10,11,12,1,2,3,4,5,6,1,2,3,10,11,12,7,8,9,4,5,6,
10,11,12,7,8,9,1,2,3,4,5,6,1,2,3,10,11,12,7,8,9,4,5,6
]

tsl_f1 = [
8, 3, 10, 11, 6, 7, 8, 3, 10, 5, 12, 1, 2, 9, 4, 5, 12, 1, 11,
6, 7, 2, 9, 4, 8, 3, 10, 2, 9, 4, 5, 12, 1, 8, 3, 10, 11, 6,
7, 5, 12, 1, 2, 9, 4, 11, 6, 7, 8, 3, 10, 5, 12, 1, 11, 6, 7,
2, 9, 4, 8, 3, 10, 11, 6, 7, 2, 9, 4, 5, 12, 1, 8, 3, 10, 5,
12, 1, 11, 6, 7, 8, 3, 10, 2, 9, 4, 11, 6, 7, 2, 9, 4, 5, 12, 1,
8, 3, 10, 2, 9, 4, 11, 6, 7, 5, 12, 1, 8, 3, 10, 5, 12, 1, 2, 9, 4,
8, 3, 10, 11, 6, 7, 2, 9, 4, 8, 3, 10, 5, 12, 1, 2, 9, 4, 11, 6,
7, 8, 3, 10, 5, 12, 1, 11, 6, 7, 8, 3, 10, 5, 12, 1, 2, 9, 4, 11,
6, 7, 5, 12, 1, 8, 3, 10, 5, 12, 1, 11, 6, 7, 8, 3, 10, 2, 9, 4,
5, 12, 1, 11, 6, 7, 8, 3, 10, 2, 9, 4, 5, 12, 1, 8, 3, 10, 11, 6,
7, 2, 9, 4, 8, 3, 10, 5, 12, 1, 11, 6, 7, 2, 9, 4, 5, 12, 1, 8, 3,
10, 11, 6, 7, 2, 9, 4, 5, 12, 1, 8, 3, 10, 11, 6, 7, 2, 9, 4, 8, 3,
10, 5, 12, 1, 11, 6, 7, 2, 9, 4, 11, 6, 7, 8, 3, 10, 5, 12, 1, 2, 9,
4, 5, 12, 1, 8, 3, 10, 11, 6, 7, 2, 9, 4, 5, 12, 1, 2, 9, 4, 11, 6, 7,
8, 3, 10, 2, 9, 4, 11, 6, 7, 5, 12, 1, 8, 3, 10, 2, 9, 4, 11, 6, 7, 2, 9,
4, 5, 12, 1, 8, 3, 10, 11, 6, 7, 2, 9, 4, 5, 12, 1, 2, 9, 4, 8, 3, 10, 5,
12, 1, 11, 6, 7, 5, 12, 1, 2, 9, 4, 11, 6, 7, 8, 3, 10, 2, 9, 4, 5, 12, 1,
11, 6, 7, 5, 12, 1, 2, 9, 4, 11, 6, 7, 8, 3, 10, 11, 6, 7, 5, 12, 1, 2, 9, 4,
8, 3, 10, 2, 9, 4, 11, 6, 7, 8, 3, 10, 5, 12, 1, 11, 6, 7, 2, 9, 4, 8, 3, 10,
5, 12, 1, 11, 6, 7, 8, 3, 10, 2, 9, 4, 5, 12, 1, 11, 6, 7, 8, 3, 10, 5, 12, 1,
2, 9, 4, 8, 3, 10, 5, 12, 1, 11, 6, 7, 2, 9, 4, 11, 6, 7, 8, 3, 10, 2, 9, 4, 5,
12, 1, 11, 6, 7, 2, 9, 4, 8, 3, 10, 2, 9, 4, 5, 12, 1, 8, 3, 10, 11, 6, 7, 5, 12,
1, 2, 9, 4, 8, 3, 10, 11, 6, 7, 5, 12, 1, 2, 9, 4, 8, 3, 10, 11, 6, 7, 5, 12, 1,
11, 6, 7, 8, 3, 10, 2, 9, 4, 11, 6, 7, 8, 3, 10, 5, 12, 1, 11, 6, 7, 8, 3, 10, 5,
12, 1, 2, 9, 4, 11, 6, 7, 2, 9, 4, 5, 12, 1, 8, 3, 10, 5, 12, 1, 11, 6, 7, 2, 9, 4,
11, 6, 7, 8, 3, 10, 2, 9, 4, 5, 12, 1, 11, 6, 7, 8, 3, 10, 5, 12, 1, 2, 9, 4, 8, 3, 10
]

start_idx = 27
end_idx = 602

def mkstim(data):
    sounds = {
    1:'../../tones/1A.wav', 2:'../../tones/1B.wav', 3:'../../tones/1C.wav',
    4:'../../tones/2A.wav', 5:'../../tones/2B.wav', 6:'../../tones/2C.wav',
    7:'../../tones/3A.wav', 8:'../../tones/3B.wav', 9:'../../tones/3C.wav',
    10:'../../tones/4A.wav', 11:'../../tones/4B.wav', 12:'../../tones/4C.wav'
  }
    out = []
    if data.cond[0] == 'lang1':
        for i in tsl_f:
            out.append(sounds[i])
    elif data.cond[0] == 'lang2':
        for i in tsl_f1:
            out.append(sounds[i])
    return out

if dtype:
    files = [x for x in os.listdir(data) if 'tsl' in x]
    for i in files:
        df = pd.read_csv(os.path.join(data, i))
        try:
            df.ix[start_idx:end_idx, 'stimulus'] = mkstim(df)
            df.to_csv(os.path.join(out, df.value[2] + '_tsl.csv'), index=None)
        except ValueError:
            print("{} gave an error".format(df.value[2]))

# one big file
else:
    files = data + '/tsl_table.csv'
    bigdf = pd.read_csv(os.path.join(data, files))
    bigdf.columns = [
        'rt', 'responses', 'trial_type', 'trial_index',
        'time_elapsed', 'internal_node_id', 'stimulus',
        'keypress', 'cond', 'targ', 'value'
    ]
    indices_to_split = []
    row_items = []
    for idx, row_item in enumerate(bigdf.responses):
        try:
            if "Q0" in row_item:
                indices_to_split.append(idx)
                row_items.append(row_item)
        except TypeError:
            pass
    indices_to_split.append(len(bigdf.responses))
    last_item = indices_to_split[-1]
    final_tups = []
    for idx, item in enumerate(row_items):
        final_tups.append((item, indices_to_split[idx], indices_to_split[idx+1]))
    for item in final_tups:
        bigdf['responses'][item[1]:item[2]] = item[0]
    par_data = []
    for item in row_items:
        temp = bigdf.loc[bigdf.responses == item]
        par_data.append(temp)
    for data in par_data:
        data.index = [x for x in range(data.shape[0])]
    # 27 go up to 602
    for par in range(len(par_data)):
        par_data[par].loc[27:602, 'stimulus'] = mkstim(par_data[par])
        par_data[par].to_csv(os.path.join(out, par_data[par].value[2] + '.csv'), index=None)
