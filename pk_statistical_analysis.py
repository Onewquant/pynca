import sys, os
sys.path.append(os.path.dirname(os.path.abspath("__file__")))

from project_tools import *

result_type = 'Phoenix'
result_type = 'R'
drug_list = ['Sitagliptin', 'Empagliflozin', 'Metformin']
input_file_dir_path = 'C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK분석'
result_file_dir_path = 'C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK분석/Stats'

comp_col = 'FEEDING'
drug_fpp_df_dict = load_data_dict(drug_list=drug_list, filename_format=f"Final Parameters Pivoted ([drug]).xls", input_file_dir_path=input_file_dir_path)

pkparams_dict = {'AUClast':'AUCt',
                 'AUCINF_obs':'AUCinf',
                 'Cmax':'Cmax',
                 'Tmax':'Tmax',
                 'HL_Lambda_z':'T1/2',
                 'CLss_F':'CL/F',
                 'Vz_F':'Vd/F'
                 }

pkparams_result_dict = dict()
gmr_result_dict = dict()

for drug, df in drug_fpp_df_dict.items():

    drug_pkparams_df = list()
    drug_gmr_df = list()

    df = df.iloc[1:].reset_index(drop=True)

    for compcol, comp_df in df.groupby(by=comp_col):

        for fpp_col, pk_param in pkparams_dict.items():

            pk_mean = round(np.mean(comp_df[fpp_col]),2)
            pk_sd = round(np.std(comp_df[fpp_col]),2)
            pk_cv_pct = round(100*pk_sd/pk_mean,1)
            pk_median = round(np.median(comp_df[fpp_col]),2)
            pk_min = round(np.min(comp_df[fpp_col]),2)
            pk_max = round(np.max(comp_df[fpp_col]),2)

            pk_geo_mean = round(g_mean(x=comp_df[fpp_col]),2)

            drug_pkparams_df.append({'Substance':drug,'Parameter':pk_param,'Statistics':'Mean', 'Feeding': compcol, 'Value':pk_mean})
            drug_pkparams_df.append({'Substance':drug,'Parameter':pk_param,'Statistics':'SD', 'Feeding': compcol, 'Value':pk_sd})
            drug_pkparams_df.append({'Substance':drug,'Parameter':pk_param,'Statistics':'CV%', 'Feeding': compcol, 'Value':pk_cv_pct})
            drug_pkparams_df.append({'Substance':drug,'Parameter':pk_param,'Statistics':'Median', 'Feeding': compcol, 'Value':pk_median})
            drug_pkparams_df.append({'Substance':drug,'Parameter':pk_param,'Statistics':'Min', 'Feeding': compcol, 'Value':pk_min})
            drug_pkparams_df.append({'Substance':drug,'Parameter':pk_param,'Statistics':'Max', 'Feeding': compcol, 'Value':pk_max})

            drug_gmr_df.append({'Substance':drug,'Parameter':pk_param,'Statistics':'Geometric Mean', 'Feeding': compcol, 'Value':pk_geo_mean})

    drug_pkparams_df = pd.DataFrame(drug_pkparams_df)
    drug_gmr_df = pd.DataFrame(drug_gmr_df)
    # Geometric Mean 비교

    pkparams_result_dict[drug] = pd.pivot_table(data=drug_pkparams_df, index=['Substance','Parameter','Statistics'], columns=['Feeding'], values='Value')
    gmr_result_dict[drug] = pd.pivot_table(data=drug_gmr_df, index=['Substance','Parameter','Statistics'], columns=['Feeding'], values='Value')

    pkparams_result_dict[drug].columns.name = None
    gmr_result_dict[drug].columns.name = None

    pkparams_result_dict[drug] = pkparams_result_dict[drug][['FED','FASTED']].copy()
    gmr_result_dict[drug] = gmr_result_dict[drug][['FED','FASTED']].copy()

    gmr_result_dict[drug]['GMR'] = gmr_result_dict[drug]['FED']/gmr_result_dict[drug]['FASTED']
    # gmr_result_dict[drug]['GMR(CI)'] =

    # z값
    # 90% CI : 1.645
    # 95% CI : 1.96
    # np.log(0.8)
    # np.log(1.25)
    # drug_pkparams_dict[drug].index.names

# 90% CI : 1.645
drug = 'Sitagliptin'
drug = 'Empagliflozin'
drug = 'Metformin'

pkparams_result_dict[drug]
gmr_result_dict[drug]