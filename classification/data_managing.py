from tqdm import tqdm
import os
import pandas as pd, numpy as np
from wfdb import io
import math
from sklearn.utils import shuffle


data_folder = '../data/ptdb/'



def get_record(record_names):
    records = []
    for record_name in tqdm(record_names):
        record = io.rdrecord(record_name=os.path.join(data_folder, record_name))
        label = record.comments[4].split(": ")[-1]
        patient = record_name.split('/')[0]
        signal_length = record.sig_len
        records.append({'name': record_name, 'label': label, 'patient': patient, 'signal_length': signal_length})
    return pd.DataFrame(records)


def get_train_test_set(selected_labels, record_names):
    test_patients = []
    train_patients = []

    test_size = 0.2

    df_records = get_record(record_names)
    # Randomly divide the subjects in train and test set.
    for label in selected_labels:
        df_selected = df_records.loc[df_records['label'] == label]
        patients = df_selected['patient'].unique()
        n_test = math.ceil(len(patients) * test_size)
        test_patients += list(np.random.choice(patients, n_test, replace=False))
        train_patients += list(patients[np.isin(patients, test_patients, invert=True)])

    return train_patients, test_patients, df_records


def make_set(df_data, label_map, record_id, window_size=2048, n_channels=15):
    n_windows = 0

    for _, record in df_data.iterrows():
        n_windows += record['signal_length'] // window_size

    dataX = np.zeros((n_windows, n_channels, window_size))
    dataY = np.zeros((n_windows, len(label_map)))

    record_list = []

    nth_window = 0
    for i, (patient, record) in enumerate(df_data.iterrows()):
        # read the record, get the signal data and transpose it
        signal_data = io.rdrecord(os.path.join(data_folder, record['name'])).p_signal.transpose()
        n_rows = signal_data.shape[-1]
        n_windows = n_rows // window_size
        dataX[nth_window:nth_window + n_windows] = np.array(
            [signal_data[:, i * window_size:(i + 1) * window_size] for i in range(n_windows)])
        dataY[nth_window:nth_window + n_windows][:, label_map[record.label]] = 1
        nth_window += n_windows

        if record_id:
            record_list += n_windows * [record['name']]

    return dataX, dataY, record_list

def get_rnn_train_test_set(selected_labels, window_size):
    record_names = io.get_record_list('ptbdb')

    label_map = {label: value for label, value in zip(selected_labels, range(len(selected_labels)))}

    train_patients, test_patients, df_records = get_train_test_set(selected_labels, record_names)
    # Set patient as the index of the dataframe to easily extract the meta data by patient
    df_patient_records = df_records.set_index('patient')
    # Select the meta data of the patient we need.
    df_train_patients = df_patient_records.loc[train_patients]
    df_test_patients = df_patient_records.loc[test_patients]
    trainX, trainY, _ = make_set(df_train_patients, label_map, False, window_size, 15)
    testX, testY, record_list = make_set(df_test_patients, label_map, True, window_size, 15)

    trainX, trainY = shuffle(trainX, trainY)
    return trainX, trainY, testX, testY, record_list