from wfdb import io
import pandas as pd
import os
from tqdm import tqdm
import numpy as np

data_folder = '../../data/twadb/'

# record_names = io.get_record_list('twadb')
record_names = ['twa00', 'twa01', 'twa02', 'twa03', 'twa04', 'twa05', 'twa06', 'twa07', 'twa08', 'twa09', 'twa10',
                'twa11', 'twa12', 'twa13', 'twa14', 'twa15', 'twa16', 'twa17', 'twa18', 'twa19', 'twa20', 'twa21',
                'twa22', 'twa23', 'twa24', 'twa25', 'twa26', 'twa27', 'twa28', 'twa29', 'twa30', 'twa31', 'twa32',
                'twa33', 'twa34', 'twa35', 'twa36', 'twa37', 'twa38', 'twa39', 'twa40', 'twa41', 'twa42', 'twa43',
                'twa44', 'twa45', 'twa46', 'twa47', 'twa48', 'twa49', 'twa50', 'twa51', 'twa52', 'twa53', 'twa54',
                'twa55', 'twa56', 'twa57', 'twa58', 'twa59', 'twa60', 'twa61', 'twa62', 'twa63', 'twa64', 'twa65',
                'twa66', 'twa67', 'twa68', 'twa69', 'twa70', 'twa71', 'twa72', 'twa73', 'twa74', 'twa75', 'twa76',
                'twa77', 'twa78', 'twa79', 'twa80', 'twa81', 'twa82', 'twa83', 'twa84', 'twa85', 'twa86', 'twa87',
                'twa88', 'twa89', 'twa90', 'twa91', 'twa92', 'twa93', 'twa94', 'twa95', 'twa96', 'twa97', 'twa98',
                'twa99']


def get_record(record_names, prefix=''):
    records = []
    for record_name in tqdm(record_names):
        record = io.rdrecord(record_name=os.path.join(data_folder, record_name))
        data = np.transpose(np.mean(record.p_signal, axis=1))
        records.append(data)

    return np.array(records)


records = get_record(record_names, prefix='')
print(records.shape)
