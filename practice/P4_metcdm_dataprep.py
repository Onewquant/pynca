import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

resource_dir = 'C:/Users/ilma0/PycharmProjects/pynca/resource/MET_CDM'

filename = 'pt_type'
with open(f'{resource_dir}/{filename}.txt', 'r', encoding='utf-8-sig') as file:
    content = file.read()

df = pd.DataFrame([c for c in content], columns=['pt_type'])
df['pt_type'] = df['pt_type'].map({'X':'NMPT','O':'HIPT'})

for filename in ['HbA1C_start_value', 'HbA1C_end_value']:
    with open(f'{resource_dir}/{filename}.txt', 'r', encoding='utf-8-sig') as file:
        content = file.read()

    df[filename] = content.split('/')
    df[filename] = df[filename].map(int)/10

df['HbA1C_delta'] = df['HbA1C_end_value'] - df['HbA1C_start_value']
df['HbA1C_pct_delta'] = 100*df['HbA1C_delta']/df['HbA1C_start_value']

df['HbA1C_pct_delta']

df.to_csv(f'{resource_dir}/SNUBH.csv', index=False, encoding='utf-8')

df['HbA1C_start_value'].describe()
df['HbA1C_end_value'].describe()
df['pt_type'].describe()

df['HbA1C_start_value'].sum()*10
df['HbA1C_end_value'].sum()*10