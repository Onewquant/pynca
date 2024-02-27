import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


filename = 'pt_type'
with open(f'C:/Users/ilma0/PycharmProjects/pynca/resource/MET_CDM/{filename}.txt', 'r', encoding='utf-8-sig') as file:
    content = file.read()

df = pd.DataFrame([c for c in content], columns=['pt_type'])
df['pt_type'] = df['pt_type'].map({'X':'NMPT','O':'HIPT'})

for filename in ['HbA1C_start_value', 'HbA1C_end_value']:
    with open(f'C:/Users/ilma0/PycharmProjects/pynca/resource/MET_CDM/{filename}.txt', 'r', encoding='utf-8-sig') as file:
        content = file.read()

    df[filename] = content.split('/')
    df[filename] = df[filename].map(int)/10

df['HbA1C_start_value'].describe()
df['HbA1C_end_value'].describe()
df['pt_type'].describe()

df['HbA1C_start_value'].sum()*10
df['HbA1C_end_value'].sum()*10