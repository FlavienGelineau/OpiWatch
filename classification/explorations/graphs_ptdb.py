from wfdb import io, plot
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from tqdm import tqdm
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import CuDNNLSTM
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report

from wfdb import io, plot

# The folder where you want to store your data
data_folder = '../../../data/ptdb/'

# First get the list of available records and then download
# those records and store them in data_folder.
record_names = io.get_record_list('ptbdb')

# Read the first record
record_name = record_names[0]
record = io.rdrecord(record_name=os.path.join(data_folder, record_name))

records = []
for record_name in tqdm(record_names):
    record = io.rdrecord(record_name=os.path.join(data_folder, record_name))
    # label = comments_to_dict(record.comments)['Reason for admission'][1:]
    print(record.samps_per_frame)
    label = record.comments[4].split(": ")[-1]
    patient = record_name.split('/')[0]
    signal_length = record.sig_len
    records.append({'name': record_name, 'label': label, 'patient': patient, 'signal_length': signal_length})

channels = record.sig_name
df_records = pd.DataFrame(records)
df_records.to_csv('df_records.csv')
# Get the first occurence of healthy control and Myocardial infarction
control = df_records[df_records['label'] == 'Healthy control'].iloc[0]
infarct = df_records[df_records['label'] == 'Myocardial infarction'].iloc[0]
# Get the signal data
control_data = io.rdrecord(record_name=os.path.join(data_folder, control['name'])).p_signal
infarct_data = io.rdrecord(record_name=os.path.join(data_folder, infarct['name'])).p_signal

# Transpose the data for easier handling.
control_data = np.transpose(control_data)
infarct_data = np.transpose(infarct_data)

# Plot data
print(['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz'])
fig, axes = plt.subplots(15, 2, figsize=(20, 40))
for idx, (control_channel, infarct_channel) in enumerate(zip(control_data, infarct_data)):
    axes[idx][0].plot(control_channel[:3000])
    axes[idx][1].plot(infarct_channel[:3000])

plt.show()