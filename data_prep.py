import pandas as pd
import numpy as np


"""
# 농도를 ug/L 단위로, 부피는 L 단위로 바꿔서 피닉스 돌린다
# 피닉스 점찍기 : 
#             -> 3 points 후 R2(adj)가 0.0001 이상 감소하는 지점 바로 직전 점으로 선택
#             -> 3 points 에 Cmax가 포함되는 경우에는 Cmax도 포함하여 선택
# cf) Best fit ? : Cmax 이후 R2(adj)가 무조건 최대인 point
# (Best fit != SOP 로직) 인때: best fit으로 돌렸을때 5 points 이상 포함되어 있는경우 
#                             -> R2(adj)가 떨어졌다가 다시 올라서 max 값 되었을 수 있으므로 확인해봐야
"""

result_type = 'Phoenix'
result_type = 'R'

drug_list = ['Sitagliptin', 'Empagliflozin', 'Metformin']
drug_dose_dict = {'Sitagliptin': 100, 'Empagliflozin': 25, 'Metformin': 1500}
dose_unit_dict = {'Sitagliptin': 'mg', 'Empagliflozin': 'mg', 'Metformin': 'mg'}
conc_unit_dict = {'Sitagliptin': 'ng/mL', 'Empagliflozin': 'ng/mL', 'Metformin': 'ng/mL'}

input_file_dir_path = 'C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK분석'
result_file_dir_path = 'C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK분석'

drug_prep_df_dict = dict()

for drug in drug_list:

    drug_prep_df = list()

    input_file_name = f"A125_05FDI2310_Conc_{drug}.xlsx"
    input_file_path = f"{input_file_dir_path}/{input_file_name}"

    result_file_name = f"CKD379_ConcPrep_{drug}({result_type}).csv"
    result_file_path = f"{result_file_dir_path}/{result_file_name}"

    df = pd.read_excel(input_file_path)

    for sn, fdf in df.groupby(by=['Subject No.']):

        fdf['ID'] = fdf['Subject No.'].copy()
        fdf['DOSE'] = drug_dose_dict[drug]
        fdf['NTIME'] = fdf['Planned Time'].map(lambda x:float(x.split('h')[0]))
        fdf['ATIME'] = fdf['Actual Time'].map(lambda x: float(x))
        fdf['CONC'] = fdf['Concentration'].map(lambda x: float(x) if x not in ('BLQ', 'N.C.') else np.nan)

        if len(fdf[fdf['NTIME'] == 0])==2:
            period_change_inx = fdf[fdf['NTIME'] == 0].index[-1]
        elif len(fdf[fdf['NTIME'] == 0])==1:
            period_change_inx = len(df)+1
        else:
            print('NTIME = 0h 인 지점이 아예 없거나 3개 이상 입니다.')
            raise ValueError

        fdf['PERIOD'] = fdf.apply(lambda row: 1 if float(row.name) < period_change_inx else 2, axis=1)

        fdf['FEEDING'] = fdf.apply(lambda row: f"{row['ID'][0]}{row['PERIOD']}", axis=1).map({'A1':'FED','A2':'FASTING','B1':'FASTING','B2':'FED'})

        fdf['DRUG'] = drug

        for period, pfdf in fdf.groupby(by=['PERIOD']):

            pfdf = pfdf.sort_values(by=['NTIME'])
            pfdf.index = list(range(min(pfdf.index),min(pfdf.index)+len(pfdf)))

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

            if result_type == 'Phoenix':
                pfdf['CONC'] = pfdf['CONC'].map(lambda x: str(x) if not np.isnan(x) else '.')
                drug_prep_df.append(pfdf[['ID', 'DOSE', 'NTIME', 'ATIME', 'CONC', 'PERIOD', 'FEEDING', 'DRUG']])
            elif result_type == 'R':
                drug_prep_df.append(pfdf[['ID', 'DOSE', 'NTIME', 'ATIME', 'CONC', 'PERIOD', 'FEEDING', 'DRUG']].dropna())

    drug_prep_df = pd.concat(drug_prep_df, ignore_index=True)

    if result_type == 'Phoenix':
        unit_row_dict = {'DOSE':dose_unit_dict[drug], 'NTIME': 'h', 'ATIME': 'h', 'CONC':conc_unit_dict[drug]}
        additional_row = dict()
        for c in list(drug_prep_df.columns):
            try: additional_row[c] = unit_row_dict[c]
            except: additional_row[c] = ''

        drug_prep_df = pd.concat([pd.DataFrame([additional_row], index=['',]), drug_prep_df])

    drug_prep_df_dict[drug] = drug_prep_df.copy()
    drug_prep_df.to_csv(result_file_path, header=True, index=False)

# drug_prep_df['ID'].unique()

# drug_prep_df[['ID', 'Screening No.']].drop_duplicates().reset_index(drop=True).to_csv(f'{result_file_dir_path}/ID_SNUM.csv', index=False)



