from tools import *


drug_list = ['Metformin','Sitagliptin', 'Empagliflozin']
# df = pd.read_csv('./CKD379_ConcPrep_Empagliflozin(R).csv')
result_dict=dict()
for drug in drug_list:
    df = pd.read_csv(f'./CKD379_ConcPrep_{drug}(R).csv')
    result = tblNCA(df, key=["ID", "FEEDING"], colTime="ATIME", colConc="CONC",
                    dose='DOSE', tau=np.nan, adm="Extravascular", dur=0, doseUnit="mg",
                    timeUnit="h", concUnit="ug/L", down="Log", R2ADJ=0, MW=0,
                    SS=False, iAUC="", excludeDelta=1, slopeMode="SNUHCPT", outputStyle="PW")
    result = result.sort_values(by=['FEEDING', 'ID'], ignore_index=True)
    result.to_csv(f'./AUTOResult({drug}).csv', index=False, encoding='utf-8-sig')
    result_dict[drug] = result.copy()

    # result_dict





result.columns


multiple_col_str = 'N_Samples	Dose	Rsq	Rsq_adjusted	Corr_XY	No_points_lambda_z	Lambda_z	Lambda_z_intercept	Lambda_z_lower	Lambda_z_upper	HL_Lambda_z	Span	Tlag	Tmax	Cmax	Cmax_D	Tlast	Clast	Clast_pred	AUClast	AUClast_D	AUCall	AUCINF_obs	AUCINF_D_obs	AUC_%Extrap_obs	AUCINF_pred	AUCINF_D_pred	AUC_%Extrap_pred	Tmin	Cmin	Ctau	Cavg	Swing_Tau	Fluctuation%	Fluctuation%_Tau	CLss_F	MRTINF_obs	MRTINF_pred	Vz_F	Accumulation_Index	AUC_TAU	AUC_TAU_D	AUC_TAU_%Extrap	AUMC_TAU'
multiple_col_str = '"'+multiple_col_str.replace('\t','", "') + '"'

single_col_str = 'N_Samples	Dose	Rsq	Rsq_adjusted	Corr_XY	No_points_lambda_z	Lambda_z	Lambda_z_intercept	Lambda_z_lower	Lambda_z_upper	HL_Lambda_z	Span	Tlag	Tmax	Cmax	Cmax_D	Tlast	Clast	Clast_pred	AUClast	AUClast_D	AUCall	AUCINF_obs	AUCINF_D_obs	AUC_%Extrap_obs	Vz_F_obs	Cl_F_obs	AUCINF_pred	AUCINF_D_pred	AUC_%Extrap_pred	Vz_F_pred	Cl_F_pred	AUMClast	AUMCINF_obs	AUMC_%Extrap_obs	AUMCINF_pred	AUMC_%Extrap_pred	MRTlast	MRTINF_obs	MRTINF_pred'
single_col_str = '"'+single_col_str.replace('\t','", "') + '"'




col_dict={
 # <존재 공통항목>
 "Dose":"DOSE",
 "Rsq":"R2",
 "Rsq_adjusted":"R2ADJ",
 "Corr_XY":"CORRXY",
 "No_points_lambda_z":"LAMZNPT",
 "Lambda_z":"LAMZ",
 "Lambda_z_intercept":"b0",
 "Lambda_z_lower":"LAMZLL",
 "Lambda_z_upper":"LAMZUL",
 "HL_Lambda_z":"LAMZHL",
 "Tlag":"TLAG",
 "Tmax":"TMAX",
 "Cmax":"CMAX",
 "Cmax_D":"CMAXD",
 "Tlast":"TLST",
 "Clast":"CLST",
 "Clast_pred":"CLSTP",
 "AUClast":"AUCLST",
 "AUClast_D":"AUCLSTD",
 "AUCall":"AUCALL",
 "AUCINF_obs":"AUCIFO",
 "AUCINF_D_obs":"AUCIFOD",
 "AUC_%Extrap_obs":"AUCPEO",
 "AUCINF_pred":"AUCIFP",
 "AUCINF_D_pred":"AUCIFPD",
 "AUC_%Extrap_pred":"AUCPEP",

 # <존재 항목> (Single Dose)
 "Vz_F_obs": "VZFO",
 "Cl_F_obs": "CLFO",
 "Vz_F_pred": "VZFP",
 "Cl_F_pred": "CLFP",
 "AUMClast": "AUMCLST",
 "AUMCINF_obs": "AUMCIFO",
 "AUMC_%Extrap_obs": "AUMCPEO",
 "AUMCINF_pred":"AUMCIFP",
 "AUMC_%Extrap_pred": "AUMCPEP",

 # <후속 추가 필요>
 # <후속 추가 필요> (공통)
 "Span": "SPAN",           #@@ LAMZUL-LAMZLL/LAMZHL
 "MRTINF_obs":"MRTIFO",    #@@ AUMCIFO/AUCIFO (non-infusion에서) AUMCIFO/AUCIFO - infusion time/2 (infusion에서)
 "MRTINF_pred": "MRTIFP",  #@@ AUMCIFP/AUCIFP (non-infusion에서) AUMCIFP/AUCIFP - infusion time/2 (infusion에서)

 # <후속 추가 필요> (single 투여)
 "MRTlast":"MRTLST",   #@@ AUMClast/AUClast

 # <후속 추가 필요> (multiple 투여)
 "Cavg": "CAVG",                    # AUCTAU / TAU
 "Swing_Tau": "SWINGTAU",           # (CMAX-CTAU)/CTAU
 "Fluctuation%": "FLUCTP",          # 100 * (CMAX-CMIN)/CAVG
 "Fluctuation%_Tau": "FLUCTPTAU",   # 100 * (CMAX-CTAU)/CAVG
 "AUC_TAU_D":"AUCTAUD",             # AUCTAU/DOSE
 "CLss_F":"CLSSF",                  # DOSE/AUCTAU
 "AUC_TAU_%Extrap":"",              # 100 * (AUCTAU - AUCLST)/AUCTAU (Dosing Time + Tau > Tlast 일떄), 0  (Dosing Time + Tau < Tlast 일떄)
 "Vz_F":"VZF",                      # DOSE / (LAMZ * AUCTAU * F)
 "Accumulation_Index":"ACCIDX",     # 1-EXP(-LAMZ*TAU)


 # <새로 추가 필요>
 # <새로 추가 필요> (공통)
 "Tmin":"TMIN",                #@@
 "Cmin":"CMIN",                #@@
 "N_Samples":"NSAMPLES",       #@@

 # <새로 추가 필요> (multiple 투여)
 "TAU":"TAU",                   # 이건 dose처럼 함수에 input으로 입력해야할듯
 "Ctau": "CTAU",                # 부분계산 필요
 "AUC_TAU":"AUCTAU",            # 부분계산 필요
 "AUMC_TAU":"AUMCTAU",          # 부분계산 필요

  }

trans_dict = dict()
for k, v in col_dict.items():
 trans_dict.update({v:k})

