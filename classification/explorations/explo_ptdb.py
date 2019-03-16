import os

from tqdm import tqdm
from wfdb import io, plot
import pandas as pd
# https://mc.ai/diagnosing-myocardial-infarction-using-long-short-term-memory-networks-lstms/
# The folder where you want to store your data
data_folder = '../data/'
# First get the list of available records and then download
# those records and store them in data_folder.
record_names = io.get_record_list('ptbdb')
#io.dl_database('ptbdb', data_folder, record_names)

# Read the first record
record_name = record_names[0]
print(record_name)
record = io.rdrecord(record_name="../data/ptdb/"+record_name)

records = []
for record_name in tqdm(record_names):
    record = io.rdrecord(record_name=os.path.join('../data/ptdb/', record_name))
    print(record.sig_name)
    # label = comments_to_dict(record.comments)['Reason for admission'][1:]
    label = record.comments[4].split(": ")[-1]
    patient = record_name.split('/')[0]
    signal_length = record.sig_len
    records.append({'name': record_name, 'label': label, 'patient': patient, 'signal_length': signal_length})

channels = record.sig_name
df_records = pd.DataFrame(records)
print(df_records)