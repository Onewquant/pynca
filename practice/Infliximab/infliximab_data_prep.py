import pandas as pd
from datetime import datetime



input_dir = 'C:/Users/ilma0/PycharmProjects/pynca/resource/Infliximab/infliximab raw data'
result_dir = 'C:/Users/ilma0/PycharmProjects/pynca/resource/Infliximab'

ldf = pd.read_csv(f'{input_dir}/infliximab_검사.csv')
tgddf = pd.read_csv(f'{input_dir}/infliximab_약품(target).csv')
ccddf = pd.read_csv(f'{input_dir}/infliximab_약품(concomitant).csv')
dgdf = pd.read_csv(f'{input_dir}/infliximab_진단.csv')
nrdf = pd.read_csv(f'{input_dir}/infliximab_간호기록.csv')

adf = ldf[ldf['검사명'] == 'Anti-Infliximab Ab [정밀면역검사] (정량)'].copy()
adf['ADA_CONC'] = adf['항목별 검사결과'].map(lambda x: float(x.split('\r\n*')[0].replace('< 2.5','2.4').replace('> 125.0','126')))
adf['ADA_POS'] = (adf['ADA_CONC'] > 2.4)*1

pt_df = pd.DataFrame(adf['환자번호'].unique(), columns=['ID'])

for inx, pid in enumerate(pt_df['ID']): break

    # ADA
    adf_frag = adf[adf['환자번호']==pid].sort_values(by=['검사 접수일시'])
    fada_date = adf_frag['검사 시행일자'].iloc[0]
    adf_frag['검사 접수일시'].iloc[0]

    # target drug
    tgddf_frag = tgddf[tgddf['환자번호']==pid].sort_values(by=['약품 오더일자'])
    tgddf_frag = tgddf_frag[tgddf_frag['약품 오더일자'] < fada_date]
    tgddf_frag['약품 오더일자'].iloc[0]

    # concomitant drug
    ccddf_frag = ccddf[ccddf['환자번호']==pid].sort_values(by=['약품명(성분명)','약품 오더일자'])
    ccddf_frag = ccddf_frag[ccddf_frag['약품 오더일자'] < fada_date]
    ccddf_frag['약품명(성분명)'].unique()
    # ccddf_frag = ccddf_frag[~ccddf_frag['간호사 수행 여부'].isna()]
    # ccddf_frag['약품 오더일자'].iloc[0]

    # 간호기록 (키, 몸무게, BMI)
    nrdf_frag = nrdf[nrdf['환자번호']==pid].sort_values(by=['간호기록 작성일자'])

    # 진단기록
    dgdf_frag = dgdf[dgdf['환자번호']==pid]
