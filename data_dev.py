from __future__ import division
import numpy as np
import pandas as pd
import scipy.stats
import os

 rsync oozernov@openmind7.mit.edu:/om/project/read/task_fmri/scripts/vis_results/results_pdf/results_phono_30perc_AboveChance_CovsHandSexWaveAge_011817.pdf /Users/ola/Desktop



language_1 = [1,2,2,2,1,1,2,1,1,2,1,2,1,1,2,2,1,1,2,1,2,2,1,2,2,2,1,2,1,2,1,1]
language_2 = [1,1,2,1,1,1,2,2,2,2,1,1,1,2,2,1,2,2,1,1,2,1,2,1,2,1,2,1,1,2,2,2]

kids_cols = [
    'rt', 'responses', 'trial_type', 'trial_index',
    'time_elapsed', 'internal_node_id', 'stimulus',
    'key_press', 'cond', 'targ', 'value'

]
"""
these require someone to check column headers
# TSL 1, 16, 26, 29, 36, 40, 41
# VSL 3, 4, 7, 16, 30, 34, 36
"""

base_dir ='/home/yoel/Desktop/SL/data_from_server/data_stim_added/'
sub_dirs = 'tsl_adults tsl_kids vsl_adults vsl_kids'.split(' ')

def add_cols(data, directory):
    columns_adults = [
        'rt','responses','trial_type',
        'trial_index','time_elapsed',
        'internal_node_id','stimulus',
        'key_press','cond','targ','value'
    ]
    if directory == 'tsl_adults' or directory == 'vsl_adults':
        data.columns = columns_adults
    return data

data_store = {
    'tsl_adults': [],
    'vsl_adults': [],
    'tsl_kids': [],
    'vsl_kids': []
}

for key in data_store.keys():
    if (key == 'tsl_adults' or key == 'vsl_adults'):
        for data in os.listdir(os.path.join(base_dir, key)):
            data_store[key].append(add_cols(
                data=pd.read_csv(os.path.join(base_dir, key, data), header=None),
                directory=key
            ))
    elif (key == 'tsl_kids' or key == 'vsl_kids'):
        for data in os.listdir(os.path.join(base_dir, key)):
            df = pd.read_csv(os.path.join(base_dir, key, data))
            if int(df.ix[0, 1][7:11]) in [3130, 3161, 3224, 3236, 3330, 3331, 3332]:
                df = pd.read_csv(os.path.join(base_dir, key, data), header=None)
                df.columns = kids_cols
            data_store[key].append(df)

def vsl_rt(data):
    """
    first item does not count, c is indexed accordingly
    returns response times as a list of tuples, (n_trial, n_response_time)
    input is single subject data
    """
    c = []
    for row in range(data.shape[0]):
        try:
            if (data.loc[row, 'targ'] in data.loc[row, 'stimulus']) and \
            (int(data.loc[row, 'rt']) != -1):
                c.append((row, int(data.loc[row, 'rt'])))
        except TypeError:
            pass
    return c[1:]


def tsl_rt(data):
    something = []
    for row in range(data.shape[0]):
        try:
            if data.loc[row, 'targ'] in data.loc[row, 'stimulus']:
                if int(data.loc[(row - 2), 'rt']) != -1000:
                    something.append((
                                      row - 2,
                                      int(data.loc[(row - 2), 'rt'])
                                     ))
                elif int(data.loc[(row - 1), 'rt']) != -1000:
                    something.append((
                                      row - 1,
                                      int(data.loc[(row - 1), 'rt'])
                                     ))
                elif int(data.loc[(row), 'rt']) != -1000:
                    something.append((
                                      row,
                                      int(data.loc[row, 'rt'])
                                     ))
                elif int(data.loc[(row + 1), 'rt']) != -1000:
                    something.append((
                                      row + 1,
                                      int(data.loc[(row + 1), 'rt'])
                                     ))
                elif int(data.loc[(row + 2), 'rt']) != -1000:
                    something.append((
                                      row + 2,
                                      int(data.loc[(row + 2), 'rt'])
                                     ))
        except TypeError:
            pass
    return something

def acc_vsl(data):
    language = data.cond[100]
    fc_idx = 309
    trials = []
    res = data.loc[fc_idx:, ['key_press','stimulus']]
    res.index = [x for x in range(res.shape[0])]
    for i in range(res.shape[0]):
        if (int(res.loc[i, 'key_press']) != -1) and (pd.isnull(res.loc[i, 'stimulus'])):
            trials.append(int(res.loc[i, 'key_press']))
    converted = []
    for val in trials:
        if int(val) == 49:
            converted.append(1)
        elif int(val) == 50:
                converted.append(2)
    if language == 'lang1':
        pat = language_1
    elif language == 'lang2':
        pat = language_2
    return (np.array(converted) == np.array(pat)).mean()

def acc_tsl(data_frame):
    language = data_frame.cond[100]
    # 37 -> left_arrow, 39 -> right_arrow
    fc_idx = 607
    responses = data_frame.loc[fc_idx:, ['key_press','stimulus']]
    responses.index= [x for x in range(responses.shape[0])]
    idxs = []
    converted = []
    c = 0
    i = 6
    while c < 224:
        idxs.append(i)
        i += 7
        c += 7
    responses = responses.loc[idxs, 'key_press']
    for val in responses:
        if int(val) == 37:
            converted.append(1)
        elif int(val) == 39:
            converted.append(2)
    if language == 'lang1':
        pat = language_1
    elif language == 'lang2':
        pat = language_2
    return (np.array(converted) == np.array(pat)).mean()
