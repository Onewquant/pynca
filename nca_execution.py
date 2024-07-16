from project_tools import *


df = pd.read_csv('C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK_analysis/CKD379_ConcPrep_Sitagliptin(R).csv')

result = tblNCA(df, key=["ID", "FEEDING"], colTime="ATIME", colConc="CONC",
                dose=100, adm="Extravascular", dur=0, doseUnit="mg",
                timeUnit="h", concUnit="ug/L", down="Log", R2ADJ=0,
                MW=0, SS=False, iAUC="", excludeDelta=1)

print(result)