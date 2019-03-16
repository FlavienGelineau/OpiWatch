import pandas as pd
import matplotlib.pyplot as plt

'''
RESP : respiraiton
pleth : plethysmograph. pulse oximeter pleth
V : tension ecg
average : moyenne glissante.
II : inconnu au bataillon

'''
def get_patient_bidmc_csv_n(n, prefix = '../../../'):
    id = str(n) if n>=10 else '0'+str(n)
    breath = pd.read_csv(prefix + 'data/bidmc_csv/bidmc_{}_Breaths.csv'.format(id))
    numerics = pd.read_csv(prefix + 'data/bidmc_csv/bidmc_{}_Numerics.csv'.format(id))
    signals = pd.read_csv(prefix + 'data/bidmc_csv/bidmc_{}_Signals.csv'.format(id))

    age = pd.read_csv(prefix+'data/bidmc_csv/bidmc_{}_Fix.txt'.format(id),
                      error_bad_lines=False,
                      warn_bad_lines=False,
                      sep = ':').to_dict()
    return breath, numerics, signals, age

def feature_extraction(signals, age_dict):
    try:
        age = [int(vals['Age']) for _, vals in age_dict.items()][0]
    except:
        print('error with age')
        age = None
    res = {'age':age,
            'mean resp':signals[' RESP'].mean(),
            'std resp':signals[' RESP'].std(),
            'mean pleth':signals[' PLETH'].mean(),
            'std pleth':signals[' PLETH'].std(),
            'mean II':signals[' II'].mean(),
            'std II':signals[' II'].std(),
            }
    try:
        res['mean V'] =signals[' V'].mean()
        res['std V']= signals[' V'].std()
        res['mean AVR']= signals[' AVR'].mean()
        res['std AVR'] = signals[' AVR'].std()
    except:
        res['mean V'] = None
        res['std V'] = None
        res['mean AVR'] = None
        res['std AVR'] = None
    return res

if __name__ =='__main__':
    health_signals = []
    for n in range(1,54):
        print(n)
        breath, numerics, signals, age = get_patient_bidmc_csv_n(n)
        health_signals.append(feature_extraction(signals, age))
    df = pd.DataFrame(health_signals)
    print(df.corr())
    print(df.mean())
