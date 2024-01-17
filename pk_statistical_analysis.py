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




drug_pkparams_list = list()

for drug, df in drug_fpp_df_dict.items(): break

    df = df.iloc[1:].reset_index(drop=True)

    for fpp_col, pk_param in pkparams_dict.items(): break

        for compcol, comp_df in df.groupby(by=comp_col): break

            pk_mean = round(np.mean(df[fpp_col]),3)
            pk_sd = round(np.std(df[fpp_col]),3)
            pk_cv_pct = round(100*pk_sd/pk_mean,2)
            pk_median = round(np.median(df[fpp_col]),3)
            pk_min = round(np.min(df[fpp_col]),3)
            pk_max = round(np.max(df[fpp_col]),3)

            drug_pkparams_list.append({'Substance':drug,'Parameter':pk_param,'Statistics':'Mean', 'Feeding': compcol, 'Value':pk_mean})
            drug_pkparams_list.append({'Substance':drug,'Parameter':pk_param,'Statistics':'SD', 'Feeding': compcol, 'Value':pk_sd})
            drug_pkparams_list.append({'Substance':drug,'Parameter':pk_param,'Statistics':'CV%', 'Feeding': compcol, 'Value':pk_cv_pct})
            drug_pkparams_list.append({'Substance':drug,'Parameter':pk_param,'Statistics':'Median', 'Feeding': compcol, 'Value':pk_median})
            drug_pkparams_list.append({'Substance':drug,'Parameter':pk_param,'Statistics':'Min', 'Feeding': compcol, 'Value':pk_min})
            drug_pkparams_list.append({'Substance':drug,'Parameter':pk_param,'Statistics':'Max', 'Feeding': compcol, 'Value':pk_max})