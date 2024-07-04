import pandas as pd
from datetime import datetime



input_dir = 'C:/Users/ilma0/PycharmProjects/pynca/resource/Infliximab/infliximab raw data'
result_dir = 'C:/Users/ilma0/PycharmProjects/pynca/resource/Infliximab'

pidf = pd.read_csv(f'{input_dir}/infliximab_환자정보.csv')
ldf = pd.read_csv(f'{input_dir}/infliximab_검사.csv')
tgddf = pd.read_csv(f'{input_dir}/infliximab_약품(target).csv')
ccddf = pd.read_csv(f'{input_dir}/infliximab_약품(concomitant).csv')
dgdf = pd.read_csv(f'{input_dir}/infliximab_진단.csv')
nrdf = pd.read_csv(f'{input_dir}/infliximab_간호기록.csv')

adf = ldf[ldf['검사명'] == 'Anti-Infliximab Ab [정밀면역검사] (정량)'].copy()
adf['ADA_CONC'] = adf['항목별 검사결과'].map(lambda x: float(x.split('\r\n*')[0].replace('< 2.5','2.4').replace('> 125.0','126')))
adf['ADA_POS'] = (adf['ADA_CONC'] > 2.4)*1

pt_df = pidf[pidf['환자번호'].isin(adf['환자번호'].unique())]
pt_df.columns = ['ID','SEX','BIRTH']
# pt_df = pd.DataFrame(adf['환자번호'].unique(), columns=['ID'])

result_df = list()
for inx, pid in enumerate(pt_df['ID']): break

    # Pt info
    result_frag = pt_df[pt_df['ID']==pid].copy()

    # ADA
    adf_frag = adf[adf['환자번호']==pid].sort_values(by=['검사 접수일시'])
    fada_date = adf_frag['검사 시행일자'].iloc[0]
    # adf_frag['검사 접수일시'].iloc[0]

    # target drug
    tgddf_frag = tgddf[tgddf['환자번호']==pid].sort_values(by=['약품 오더일자'])
    tgddf_frag = tgddf_frag[tgddf_frag['약품 오더일자'] < fada_date]
    tgd_date = tgddf_frag['약품 오더일자'].iloc[0]


    # period_dict = {'SC':0,'MIV':0,'IVS':0,'IV':0}
    count_dict = {'SC_COUNT':0,'MIV_COUNT':0,'IVS_COUNT':0,'IV_COUNT':0, 'TOT_COUNT':0}
    tot_dose_dict = {'SC_DOSE':0,'MIV_DOSE':0,'IVS_DOSE':0,'IV_DOSE':0, 'TOT_DOSE':0}
    # mean_dose_dict = {'SC':0,'MIV':0,'IVS':0,'IV':0}
    for tgd_inx, tgd_row in tgddf_frag[['[실처방] 1회 처방량','[실처방] 경로','[실처방] 용법','[실처방] 처방일수']].iterrows():
        tgd_route = tgd_row['[실처방] 경로']
        tgd_dose = int(tgd_row['[실처방] 1회 처방량'].replace('mg',''))
        dorwk = tgd_row['[실처방] 용법'].split(' ')[0]
        if dorwk[-1]=='일':
            count = int(tgd_row['[실처방] 처방일수']/(int(dorwk[0])*1))
        else:
            count = int(tgd_row['[실처방] 처방일수']/(int(dorwk[0])*14))

        if tgd_route=='SC':
            count_dict['SC_COUNT']+=count
            tot_dose_dict['SC_DOSE']+=count*tgd_dose
            tot_dose_dict['TOT_DOSE']+=count*tgd_dose
        elif tgd_route=='MIV':
            count_dict['MIV_COUNT']+=count
            tot_dose_dict['MIV_DOSE']+=count*tgd_dose
            count_dict['IV_COUNT']+=count
            tot_dose_dict['IV_DOSE']+=count*tgd_dose
            tot_dose_dict['TOT_DOSE'] += count * tgd_dose
        elif tgd_route=='IVS':
            count_dict['IVS_COUNT']+=count
            tot_dose_dict['IVS_DOSE']+=count*tgd_dose
            count_dict['IV_COUNT']+=count
            tot_dose_dict['IV_DOSE']+=count*tgd_dose
            tot_dose_dict['TOT_DOSE'] += count * tgd_dose




    result_frag['INF_START_DATE'] = tgd_date
    result_frag['ROUTE']='/'.join(list(tgddf_frag['[실처방] 경로'].unique()))
    result_frag['TOTAL_COUNT']='/'.join(list(tgddf_frag['[실처방] 경로'].unique()))
    result_frag['ROUTE']='/'.join(list(tgddf_frag['[실처방] 경로'].unique()))
    result_frag['ADA_TEST_DATE'] = tgd_date

    # concomitant drug
    ccddf_frag = ccddf[ccddf['환자번호']==pid].sort_values(by=['약품명(성분명)','약품 오더일자'])
    ccddf_frag = ccddf_frag[(ccddf_frag['약품 오더일자'] < fada_date)&(ccddf_frag['약품 오더일자'] >= tgd_date)]
    ccddf_frag['약품명(성분명)'].unique()
    # ccddf_frag = ccddf_frag[~ccddf_frag['간호사 수행 여부'].isna()]
    # ccddf_frag['약품 오더일자'].iloc[0]

    # 간호기록 (키, 몸무게, BMI)
    nrdf_frag = nrdf[nrdf['환자번호']==pid].sort_values(by=['간호기록 작성일자'])
    nrdf_frag = nrdf_frag[(nrdf_frag['간호기록 작성일자'] < fada_date)&(nrdf_frag['간호기록 작성일자'] >= tgd_date)]
    nrdf_frag[nrdf_frag['항목명']=='BMI']

    # 진단기록
    dgdf_frag = dgdf[dgdf['환자번호']==pid]
    if len(dgdf_frag)!=0:
        dgdf_frag[['첫 진단 당시 나이','원내 진단명']]
        dg_list = dgdf_frag['원내 진단명'].unique()
        dgdate = 'N'
        dgrec = 'U'
        for dgn in dg_list:
            if ('Crohn'.upper() in dgn.upper()):
                dgrec = 'C'
                break
    else:
        dgrec = 'E'
