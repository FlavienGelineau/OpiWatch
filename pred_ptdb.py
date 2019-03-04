from wfdb import io, plot
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import CuDNNLSTM
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report
from tqdm import tqdm


from wfdb import io, plot

# The folder where you want to store your data
data_folder = '../data/ptdb/'
# First get the list of available records and then download
# those records and store them in data_folder.
record_names = io.get_record_list('ptbdb')
#io.dl_database('ptbdb', data_folder, record_names)

# Read the first record
record_name = record_names[0]
record = io.rdrecord(record_name=os.path.join(data_folder, record_name))

records = []
for record_name in tqdm(record_names):
    record = io.rdrecord(record_name=os.path.join(data_folder, record_name))
    # label = comments_to_dict(record.comments)['Reason for admission'][1:]
    label = record.comments[4].split(": ")[-1]
    patient = record_name.split('/')[0]
    signal_length = record.sig_len
    records.append({'name': record_name, 'label': label, 'patient': patient, 'signal_length': signal_length})

channels = record.sig_name
df_records = pd.DataFrame(records)
print(df_records['label'].value_counts())
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
fig, axes = plt.subplots(15, 2, figsize=(20, 40))
for idx, (control_channel, infarct_channel) in enumerate(zip(control_data, infarct_data)):
    axes[idx][0].plot(control_channel[:3000])
    axes[idx][1].plot(infarct_channel[:3000])

# These are the labels we'll be using. I you want to include more heart conditions, simply add them to this list.
selected_labels = [
    'Healthy control',
    'Myocardial infarction'
]
# The label map will be used to do one-hot encoding with the labels.
label_map = {label: value for label, value in zip(selected_labels, range(len(selected_labels)))}

test_patients = []
train_patients = []
# We will use 80% of the available subject to train the model
# The remaining 20% will be used to test the performance.
test_size = 0.2

# Randomly divide the subjects in train and test set.
for label in selected_labels:
    df_selected = df_records.loc[df_records['label'] == label]
    patients = df_selected['patient'].unique()
    n_test = math.ceil(len(patients) * test_size)
    test_patients += list(np.random.choice(patients, n_test, replace=False))
    train_patients += list(patients[np.isin(patients, test_patients, invert=True)])


def make_set(df_data, label_map, record_id, window_size=2048, n_channels=15):
    """
    1. Loads the ECG data from the records specified in df_data
    2. Divide the signal data in windows of size window_size (default of 2048 which is enough to capture 3 heart beats.)


    returns:
        dataX: contains windowed ecg data (shape = n_windwows, n_channels, window_size)
        dataY: containts label for each window
        record_list: If required also returns a list specifying the record name for each window, else is empty list.
    """
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


# Set patient as the index of the dataframe to easily extract the meta data by patient
df_patient_records = df_records.set_index('patient')
# Select the meta data of the patient we need.
df_train_patients = df_patient_records.loc[train_patients]
df_test_patients = df_patient_records.loc[test_patients]
window_size = 1024
trainX, trainY, _ = make_set(df_train_patients, label_map, False, window_size, 15)
testX, testY, record_list = make_set(df_test_patients, label_map, True, window_size, 15)


def make_model(input_shape, output_dim, dropout=0.2):
    print("model dim: ", input_shape, output_dim)
    model = Sequential()
    model.add(CuDNNLSTM(128, input_shape=input_shape, batch_size=None, return_sequences=True))
    model.add(CuDNNLSTM(64, return_sequences=False))
    model.add(Dense(output_dim, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model



# Shuffle the data
trainX, trainY = shuffle(trainX, trainY)

# Since we have a large class inbalance we need to udjust the weights for it.
fractions = 1-trainY.sum(axis=0)/len(trainY)
weights = fractions[trainY.argmax(axis=1)]

model = make_model((trainX.shape[1], trainX.shape[2]), trainY.shape[-1], CuDNNLSTM)

model.fit(trainX, trainY, epochs=50, batch_size=512, sample_weight=weights)


# Predict the label for each sequence
output = model.predict_classes(testX)
# Inspect the accuracy on sequence level.
print(confusion_matrix(testY.argmax(axis=1), output))

# Group all sequences of the same subject and take the average of all the predictions
# Remember labels are one-hot encoded, so [1,0] is healthy, [0,1] is infarct.
# If we take the argmax over the output we get a 0 (healthy) or 1 (infarct) as label.
summed = pd.DataFrame({'record':record_list, 'predictions':output, 'label':testY.argmax(axis=1)}).groupby('record').mean()
summed["predicted label"]= summed['predictions'] > 0.5

print(classification_report(summed['label'], summed["predicted label"]))

