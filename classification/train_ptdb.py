import pandas as pd
from keras.layers import CuDNNLSTM
from keras.layers import Dense
from keras.models import Sequential
from sklearn.metrics import confusion_matrix, classification_report
from keras.callbacks import EarlyStopping, ModelCheckpoint
from classification.data_managing import get_rnn_train_test_set


def make_model(input_shape, output_dim):
    print("model dim: ", input_shape, output_dim)
    model = Sequential()
    model.add(CuDNNLSTM(64, input_shape=input_shape, batch_size=None, return_sequences=False))
    model.add(Dense(200, activation='relu'))
    model.add(Dense(output_dim, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model


selected_labels = ['Healthy control', 'Myocardial infarction', 'Bundle branch block', 'Cardiomyopathy']
window_size = 1024
trainX, trainY, testX, testY, record_list = get_rnn_train_test_set(selected_labels, window_size)

model = make_model((trainX.shape[1], trainX.shape[2]),
                   trainY.shape[-1])

checkpoint = ModelCheckpoint('weights_best_model', monitor='val_loss', verbose=1, save_best_only=True, mode='min')
early_stopping = EarlyStopping(patience=5)
callbacks_list = [checkpoint, early_stopping]

model.fit(trainX, trainY,
          validation_split=0.15,
          epochs=10,
          batch_size=512,
          callbacks=callbacks_list,
          verbose=0)

print(testX.shape)
output = model.predict_classes(testX)
print(len(record_list), len(output), len(testY.argmax(axis=1)))
summed = pd.DataFrame({'record': record_list,
                       'predictions': output,
                       'label': testY.argmax(axis=1)})
summed = summed.groupby('record').mean()
summed["predicted label"] = summed['predictions'] > 0.5

print(confusion_matrix(testY.argmax(axis=1), output))
print(classification_report(summed['label'], summed["predicted label"]))
