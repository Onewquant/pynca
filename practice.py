from tools import *



rdf = pd.read_csv('./prepdata.csv')
# result = tblNCA(df, key=["ID", "FEEDING"], colTime="ATIME", colConc="CONC", dose='DOSE', tau=np.nan, adm="Extravascular", dur=0, doseUnit="mg", timeUnit="h", concUnit="ug/L", down="Log", R2ADJ=0, MW=0, SS=False, iAUC="", excludeDelta=1, slopeMode="BEST")

# 데이터 변환
df = rdf[~(rdf['CONC']=='.')].copy()
df = df.iloc[1:].copy()


df['CONC'] = df['CONC'].map(float)
df['ATIME'] = df['ATIME'].map(float)
df = df.sort_values(by=['ID','ATIME'])

result = tblNCA(concData=df[df['S_M']==1],key=['ID'],colTime="ATIME",colConc='CONC', down="Log",dose=0.5,slopeMode='BEST')
result.to_csv('./NCA_single.csv',index=False)


# result = tblNCA(concData=df[df['GRP'].isin([2,4])],key=['ID'],colTime="A_TIME",colConc='CONC',dose=0.5,slopeMode='SNUHCPT')
result['TAU'] = np.nan
result =ncar_to_phoenix(result)

