from tqdm import tqdm
import os
import pandas as pd, numpy as np
from wfdb import io
import math
from sklearn.utils import shuffle

from classification.twa import get_twadb_db

data_folder = '../../data/ptdb/'


def get_record(record_names, prefix='../'):
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

    test_size = 0.1

    df_records = get_record(record_names)
    # Randomly divide the subjects in train and test set.
    if selected_labels != None:
        for label in selected_labels:
            df_selected = df_records.loc[df_records['label'] == label]
            patients = df_selected['patient'].unique()
            n_test = math.ceil(len(patients) * test_size)
            test_patients += list(np.random.choice(patients, n_test, replace=False))
            train_patients += list(patients[np.isin(patients, test_patients, invert=True)])
    else:
        df_selected = df_records.copy()
        patients = df_selected['patient'].unique()
        n_test = math.ceil(len(patients) * test_size)
        test_patients += list(np.random.choice(patients, n_test, replace=False))
        train_patients += list(patients[np.isin(patients, test_patients, invert=True)])

    return train_patients, test_patients, df_records


def format_X(signal_data, taux_echant, overlapping, indices_channels, window_size):
    signal_data = signal_data[indices_channels]
    signal_data_resampled = np.transpose(
        np.array(
            [np.mean(signal_data[:, i * taux_echant:(i + 1) * taux_echant], axis=1) for i in
             range(len(signal_data[0]) // taux_echant)]))

    n_rows = signal_data_resampled.shape[-1]
    n_windows = n_rows * overlapping // window_size - 1

    data_for_patient = np.array(
        [signal_data_resampled[:,
         i * int(window_size / overlapping):i * int(window_size / overlapping) + window_size] for i in
         range(n_windows)])
    return data_for_patient, n_rows, n_windows


def get_len_set(df_data, overlapping, window_size, taux_echant):
    n_windows = 0
    for _, record in df_data.iterrows():
        n_windows += (record['signal_length'] * overlapping // window_size) // taux_echant
    return n_windows


def make_set(df_data, label_map, record_id, indices_channels, window_size=2048, taux_echant=1):
    n_channels = len(indices_channels)
    overlapping = 2

    n_windows = get_len_set(df_data, overlapping, window_size, taux_echant)

    dataX = np.zeros((n_windows, n_channels, window_size))
    dataY = np.zeros((n_windows, len(label_map)))

    record_list = []

    nth_window = 0
    for i, (patient, record) in tqdm(enumerate(df_data[:5].iterrows())):
        signal_data = io.rdrecord(os.path.join(data_folder, record['name'])).p_signal.transpose()
        data_for_patient, n_rows, n_windows = format_X(
            signal_data, taux_echant, overlapping, indices_channels, window_size)

        dataX[nth_window:nth_window + n_windows] = data_for_patient
        dataY[nth_window:nth_window + n_windows][:, label_map[record.label]] = 1

        last_id = nth_window + n_windows

        nth_window += n_windows

        if record_id:
            record_list += n_windows * [record['name']]

    dataX = dataX[:nth_window]
    dataY = dataY[:nth_window]

    if not record_id:
        X_twa, Y_twa = get_twadb_db()
        print(X_twa.shape)
        print(Y_twa.shape)
        print(dataX.shape)
        print(dataY.shape)
        dataX = np.array(dataX.tolist() + X_twa.tolist())
        dataY = np.array(dataY.tolist() + Y_twa.tolist())

    print('nth_window', nth_window)
    print('last id', last_id)
    print('len dataX', len(dataX))
    return dataX, dataY, record_list


def get_rnn_train_test_set(selected_labels, window_size):
    ptdb_features = ['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'vx', 'vy', 'vz']
    chosen_features = ['avr']
    chosen_indices = [ptdb_features.index(elt) for elt in chosen_features]
    record_names = pd.read_csv('../../data/ptdb/RECORDS').values.reshape(-1)
    print(record_names)

    label_map = {label: value for label, value in zip(selected_labels, range(len(selected_labels)))}

    train_patients, test_patients, df_records = get_train_test_set(selected_labels, record_names)
    df_patient_records = df_records.set_index('patient')
    # Select the meta data of the patient we need.
    df_train_patients = df_patient_records.loc[train_patients]
    df_test_patients = df_patient_records.loc[test_patients]
    trainX, trainY, _ = make_set(df_train_patients, label_map, False, window_size=window_size,
                                 indices_channels=chosen_indices)
    testX, testY, record_list = make_set(df_test_patients, label_map, True, window_size=window_size,
                                         indices_channels=chosen_indices)

    trainX, trainY = shuffle(trainX, trainY)
    return trainX, trainY, testX, testY, record_list
