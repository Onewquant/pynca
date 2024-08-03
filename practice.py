from tools import *

rdf = pd.read_csv('./prepdata.csv')

# 데이터 변환
df = rdf[~(rdf['CONC']=='.')].copy()
df = df.iloc[1:].copy()

df['CONC'] = df['CONC'].map(float)
df['ATIME'] = df['ATIME'].map(float)
df = df.sort_values(by=['ID','ATIME'])

result = tblNCA(concData=df[df['S_M']==1],key=['ID'],colTime="ATIME",colConc='CONC', down="Log",dose=0.5, tau=0, slopeMode='BEST', colStyle='pw')
result = tblNCA(concData=df[df['S_M']==2],key=['ID'],colTime="ATIME",colConc='CONC', down="Log",dose=0.5, tau=0, slopeMode='BEST', colStyle='ncar')
result.to_csv('./NCA_single.csv',index=False)





