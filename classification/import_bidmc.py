from classification.explorations.explo_bidmc import get_patient_bidmc_csv_n, feature_extraction
import pandas as pd
import numpy as np


def resample_dataframe_to_10_ms(signals):
    resample_index = pd.date_range(start=signals.index[0], end=signals.index[-1], freq='10ms')
    dummy_frame = pd.DataFrame(np.NaN, index=resample_index, columns=signals.columns)
    new_signals = signals.combine_first(dummy_frame).interpolate()
    new_signals.to_csv('initial.csv')
    new_signals['Time [s]'] = new_signals.index.microsecond
    new_signals = new_signals[(new_signals['Time [s]'] / 1000) % 10 == 0]
    new_signals['Time [s]']/=10**6
    return new_signals


if __name__ == '__main__':
    health_signals = []
    for n in range(1, 54):
        breath, numerics, signals, age = get_patient_bidmc_csv_n(n, prefix='../../')
        signals.index = pd.to_datetime(signals['Time [s]'], unit='s')
        new_signals = resample_dataframe_to_10_ms(signals)
        print(new_signals.columns)
        health_signals.append(new_signals[['II', ' V', ' AVR']])
        # health_signals.append(feature_extraction(signals, age))
    df = pd.DataFrame(health_signals)
    # print(df.resample('10T').mean())
