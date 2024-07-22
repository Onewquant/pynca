from tools import *



df = pd.read_csv('./prepdata.csv')
result = tblNCA(df, key=["ID", "FEEDING"], colTime="ATIME", colConc="CONC", dose='DOSE', tau=np.nan, adm="Extravascular", dur=0, doseUnit="mg", timeUnit="h", concUnit="ug/L", down="Log", R2ADJ=0, MW=0, SS=False, iAUC="", excludeDelta=1, slopeMode="BEST")
len(result['units'])
len(result.columns)

result2 = ncar_to_phoenix(df=result)
result2