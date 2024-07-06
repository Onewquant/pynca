import pandas as pd
import numpy as np

for hospital in ('SNUH','SNUBH'):
    df = pd.read_csv(f'C:/Users/ilma0/PycharmProjects/pynca/resource/MET_CDM/Metformin CDM Supplement - {hospital}.csv')
    df['Covariate'] = df['Covariate'].map(lambda x:x[0].upper()+x[1:].lower())
    df['Beta_abs'] = df['Beta'].map(lambda x:np.abs(x))
    df = df.sort_values(by=['Beta_abs'], ascending=False, ignore_index=True)

    df.to_csv(f'C:/Users/ilma0/PycharmProjects/pynca/resource/MET_CDM/Metformin CDM Supplement - {hospital}_수정.csv', index=False)
    