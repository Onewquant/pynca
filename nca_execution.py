from project_tools import *


df = pd.read_csv('./prepdata.csv')

result = tblNCA(df, key=["ID", "FEEDING"], colTime="ATIME", colConc="CONC",
                dose='DOSE', adm="Extravascular", dur=0, doseUnit="mg",
                timeUnit="h", concUnit="ug/L", down="Log", R2ADJ=0,
                MW=0, SS=False, iAUC="", excludeDelta=1)

print(result)