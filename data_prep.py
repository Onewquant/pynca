import pandas as pd
import numpy as np

drug_list = ['Sitagliptin', 'Empagliflozin', 'Metformin']
drug_dose_dict = {'Sitagliptin': 100, 'Empagliflozin': 25, 'Metformin': 1500}

input_file_dir_path = 'D:\임상시험 Sub-I\CKD379-FDI\PK분석'
result_file_dir_path = 'D:\임상시험 Sub-I\CKD379-FDI\PK분석'

for drug in drug_list:

    drug_prep_df = list()

    input_file_name = f"A125_05FDI2310_Conc_{drug}.xlsx"
    input_file_path = f"{input_file_dir_path}/{input_file_name}"

    result_file_name = f"CKD379_ConcPrep_{drug}.csv"
    result_file_path = f"{result_file_dir_path}/{result_file_name}"

    df = pd.read_excel(input_file_path)

    for sn, fdf in df.groupby(by=['Subject No.']):

        fdf['ID'] = fdf['Subject No.'].copy()
        fdf['DOSE'] = drug_dose_dict[drug]
        fdf['NTIME'] = fdf['Planned Time'].map(lambda x:float(x.split('h')[0]))
        fdf['ATIME'] = fdf['Actual Time'].map(lambda x: float(x))
        fdf['CONC'] = fdf['Concentration'].map(lambda x: float(x) if x not in ('BLQ', 'N.C.') else np.nan)

        try:
            period_change_inx = fdf[(fdf['NTIME'].diff(1).fillna(method='bfill') > 0) == False].index[0]
        except:
            continue

        fdf['PERIOD'] = fdf.apply(lambda row: 1 if float(row.name) < period_change_inx else 2, axis=1)

        fdf['FEEDING'] = fdf.apply(lambda row: f"{row['ID'][0]}{row['PERIOD']}", axis=1).map({'A1':'FED','A2':'FASTING','B1':'FASTING','B2':'FED'})

        fdf['DRUG'] = drug

        for period, pfdf in fdf.groupby(by=['PERIOD']):
            if not np.isnan(np.nanmax(pfdf['CONC'])):
                tmax_inx = pfdf[pfdf['CONC'] == np.nanmax(pfdf['CONC'])].iloc[0].name
            else:
                print('All Conc Values are NAN !')
                tmax_inx = np.nan

            blq_before_tmax_inx_list = list(pfdf[(pfdf['CONC'].isna()) & (pfdf.index < tmax_inx)].index)
            blq_after_tmax_inx_list = list(pfdf[(pfdf['CONC'].isna()) & (pfdf.index > tmax_inx)].index)

            for blqinx in blq_before_tmax_inx_list:
                pfdf.at[blqinx,'CONC'] = 0.0

            for blqinx in blq_after_tmax_inx_list:
                pfdf.at[blqinx,'CONC'] = np.nan

            drug_prep_df.append(pfdf[['ID', 'DOSE', 'NTIME', 'ATIME', 'CONC', 'PERIOD', 'FEEDING', 'DRUG']].dropna())

    drug_prep_df = pd.concat(drug_prep_df, ignore_index=True)

    drug_prep_df.to_csv(result_file_path, header=True, index=False)

# drug_prep_df['ID'].unique()