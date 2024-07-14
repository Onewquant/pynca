import pandas as pd
import os
from typing import List, Union
import numpy as np
import warnings

def sNCA(x: np.ndarray,
                 y: np.ndarray,
                 dose: float = 0,
                 adm: str = "Extravascular",
                 dur: float = 0,
                 doseUnit: str = "mg",
                 timeUnit: str = "h",
                 concUnit: str = "ug/L",
                 iAUC: Union[str, pd.DataFrame] = "",
                 down: str = "Linear",
                 R2ADJ: float = 0.7,
                 MW: float = 0,
                 SS: bool = False,
                 Keystring: str = "",
                 excludeDelta: float = 1) -> Dict[str, float]:

    # Input validation
    if not (isinstance(x, (np.ndarray, list)) and isinstance(y, (np.ndarray, list)) and
            isinstance(dose, (int, float)) and isinstance(dur, (int, float)) and
            isinstance(adm, str) and isinstance(down, str)):
        raise ValueError("Check input types!")

    if adm.upper().strip() == "INFUSION" and not (dur > 0):
        raise ValueError("Infusion mode should have dur larger than 0!")

    # Remove NA points
    mask = ~(np.isnan(x) | np.isnan(y))
    x = x[mask]
    y = y[mask]

    if not np.array_equal(x, np.sort(x)):
        raise ValueError("Check if the x is sorted in order!")

    n = len(x)

    # Initialize result dictionary
    RetNames1 = ["b0", "CMAX", "CMAXD", "TMAX", "TLAG", "CLST", "CLSTP", "TLST",
                 "LAMZHL", "LAMZ", "LAMZLL", "LAMZUL", "LAMZNPT", "CORRXY", "R2",
                 "R2ADJ", "AUCLST", "AUCALL", "AUCIFO", "AUCIFOD", "AUCIFP",
                 "AUCIFPD", "AUCPEO", "AUCPEP", "AUMCLST", "AUMCIFO", "AUMCIFP",
                 "AUMCPEO", "AUMCPEP"]

    if adm.upper().strip() == "BOLUS":
        RetNames1.extend(["C0", "AUCPBEO", "AUCPBEP"])

    if adm.upper().strip() == "EXTRAVASCULAR":
        RetNames1.extend(["VZFO", "VZFP", "CLFO", "CLFP", "MRTEVLST", "MRTEVIFO", "MRTEVIFP"])
    else:
        RetNames1.extend(["VZO", "VZP", "CLO", "CLP", "MRTIVLST", "MRTIVIFO", "MRTIVIFP", "VSSO", "VSSP"])

    Res = {name: np.nan for name in RetNames1}

    if n == 0 or n != len(y) or any(y < 0):
        Res["LAMZNPT"] = 0
        return Res

    Units = Unit(doseUnit=doseUnit, timeUnit=timeUnit, concUnit=concUnit, MW=MW)

    uY = np.unique(y)

    if len(uY) == 1:
        Res["CMAX"] = uY[0]
        if dose > 0:
            Res["CMAXD"] = uY[0] / dose
        Res["TMAX"] = x[y == uY[0]][0]
        if uY[0] == 0:
            Res["TLAG"] = np.nan
            Res["AUCALL"] = 0
        elif np.argmax(y == uY[0]) > 0:
            Res["TLAG"] = x[np.argmax(y == uY[0]) - 1]
        else:
            Res["TLAG"] = 0
        Res["CLST"] = uY[0] if uY[0] != 0 else np.nan
        Res["TLST"] = x[y == uY[0]][0] if uY[0] != 0 else np.nan
        Res["LAMZNPT"] = 0
        Res["b0"] = uY[0]

        if isinstance(iAUC, pd.DataFrame) and not iAUC.empty:
            niAUC = len(iAUC)
            if niAUC > 0:
                RetNames1.extend(iAUC['Name'].astype(str))
                for _, row in iAUC.iterrows():
                    if all(y == 0) and min(x, key=lambda x: x or float('inf')) <= min(0, row['Start']) and max(x) >= row['End']:
                        Res[row['Name']] = 0
                    elif adm.upper().strip() == "BOLUS":
                        if sum(x == 0) == 0:
                            x2 = np.concatenate(([0], x))
                            y2 = np.concatenate(([uY[0]], y))
                        Res[row['Name']] = IntAUC(x2, y2, row['Start'], row['End'], Res, down=down)
                    else:
                        Res[row['Name']] = IntAUC(x, y, row['Start'], row['End'], Res, down=down)
                    Units = Units.append(pd.Series(Units.loc['AUCLST'], name=row['Name']))
        else:
            niAUC = 0

        for i, val in enumerate(Res.values()):
            Res[RetNames1[i]] = val * Units.loc[RetNames1[i], 2]

        return Res

    iLastNonZero = np.max(np.where(y > 0)[0])
    x0 = x[:iLastNonZero+1]
    y0 = y[:iLastNonZero+1]
    x1 = x0[y0 != 0]
    y1 = y0[y0 != 0]

    if adm.upper().strip() == "BOLUS":
        if y[0] > y[1] > 0:
            C0 = np.exp(-x[0] * (np.log(y[1]) - np.log(y[0]))/(x[1] - x[0]) + np.log(y[0]))
        else:
            C0 = y[x == np.min(x[y > 0])][0]
        x2 = np.concatenate(([0], x))
        y2 = np.concatenate(([C0], y))
        x3 = np.concatenate(([0], x0))
        y3 = np.concatenate(([C0], y0))
    else:
        if np.isnan(x[x == 0][0] if len(x[x == 0]) > 0 else np.nan):
            x2 = np.concatenate(([0], x))
            y2 = np.concatenate(([0], y))
            x3 = np.concatenate(([0], x0))
            y3 = np.concatenate(([0], y0))
        else:
            x2 = x
            y2 = y
            x3 = x0
            y3 = y0

    tRes = BestSlope(x1, y1, adm, excludeDelta=excludeDelta)
    if R2ADJ > 0:
        if tRes["LAMZNPT"] < 2:
            tRes = DetSlope(x1, y1, SubTitle=Keystring)
        elif tRes["R2ADJ"] < R2ADJ:
            tRes = DetSlope(x1, y1, SubTitle=Keystring, sel_1=np.where(x1 == tRes["LAMZLL"])[0][0], sel_2=np.where(x1 == tRes["LAMZUL"])[0][0])

    tRes["UsedPoints"] = tRes["UsedPoints"] + np.where(x == tRes["LAMZLL"])[0][0] - np.where(x1 == tRes["LAMZLL"])[0][0]

    for key in ["R2", "R2ADJ", "LAMZNPT", "LAMZ", "b0", "CORRXY", "LAMZLL", "LAMZUL", "CLSTP"]:
        Res[key] = tRes[key]

    tabAUC = AUC(x3, y3, down)
    Res["AUCLST"], Res["AUMCLST"] = tabAUC[-1]
    Res["AUCALL"] = AUC(x2, y2, down)[-1, 0]
    Res["LAMZHL"] = np.log(2) / Res["LAMZ"]
    Res["TMAX"] = x[np.argmax(y)]
    Res["CMAX"] = np.max(y)
    Res["TLST"] = x[iLastNonZero]
    Res["CLST"] = y[iLastNonZero]
    Res["AUCIFO"] = Res["AUCLST"] + Res["CLST"] / Res["LAMZ"]
    Res["AUCIFP"] = Res["AUCLST"] + Res["CLSTP"] / Res["LAMZ"]
    Res["AUCPEO"] = (1 - Res["AUCLST"] / Res["AUCIFO"]) * 100
    Res["AUCPEP"] = (1 - Res["AUCLST"] / Res["AUCIFP"]) * 100
    Res["AUMCIFO"] = Res["AUMCLST"] + Res["CLST"] * Res["TLST"] / Res["LAMZ"] + Res["CLST"] / Res["LAMZ"]**2
    Res["AUMCIFP"] = Res["AUMCLST"] + Res["CLSTP"] * Res["TLST"] / Res["LAMZ"] + Res["CLSTP"] / Res["LAMZ"]**2
    Res["AUMCPEO"] = (1 - Res["AUMCLST"] / Res["AUMCIFO"]) * 100
    Res["AUMCPEP"] = (1 - Res["AUMCLST"] / Res["AUMCIFP"]) * 100

    if dose is not None and dose > 0:
        Res["CMAXD"] = Res["CMAX"] / dose
        Res["AUCIFOD"] = Res["AUCIFO"] / dose
        Res["AUCIFPD"] = Res["AUCIFP"] / dose

    if adm.upper().strip() == "BOLUS":
        Res["C0"] = C0
        Res["AUCPBEO"] = tabAUC[1, 0] / Res["AUCIFO"] * 100
        Res["AUCPBEP"] = tabAUC[1, 0] / Res["AUCIFP"] * 100
    else:
        if np.sum(y0 == 0) > 0:
            Res["TLAG"] = x0[np.max(np.where(y0 == 0)[0])]
        else:
            Res["TLAG"] = 0
        if not np.isnan(x0[x0 == 0][0] if len(x0[x0 == 0]) > 0 else np.nan):
            if y0[x0 == 0][0] > 0:
                Res["TLAG"] = 0

    if adm.upper().strip() == "EXTRAVASCULAR":
        if SS:
            Res["VZFO"] = dose / Res["AUCLST"] / Res["LAMZ"]
            Res["VZFP"] = np.nan
            Res["CLFO"] = dose / Res["AUCLST"]
            Res["CLFP"] = np.nan
            Res["MRTEVLST"] = Res["AUMCLST"] / Res["AUCLST"]
            Res["MRTEVIFO"] = np.nan
            Res["MRTEVIFP"] = np.nan
        else:
            Res["VZFO"] = dose / Res["AUCIFO"] / Res["LAMZ"]
            Res["VZFP"] = dose / Res["AUCIFP"] / Res["LAMZ"]
            Res["CLFO"] = dose / Res["AUCIFO"]
            Res["CLFP"] = dose / Res["AUCIFP"]
            Res["MRTEVLST"] = Res["AUMCLST"] / Res["AUCLST"]
            Res["MRTEVIFO"] = Res["AUMCIFO"] / Res["AUCIFO"]
            Res["MRTEVIFP"] = Res["AUMCIFP"] / Res["AUCIFP"]
    else:
        if SS:
            Res["VZO"] = dose / Res["AUCLST"] / Res["LAMZ"]
            Res["VZP"] = np.nan
            Res["CLO"] = dose / Res["AUCLST"]
            Res["CLP"] = np.nan
            Res["MRTIVLST"] = Res["AUMCLST"] / Res["AUCLST"] - dur / 2
            Res["MRTIVIFO"] = np.nan
            Res["MRTIVIFP"] = np.nan
            Res["VSSO"] = Res["MRTIVLST"] * Res["CLO"]
            Res["VSSP"] = np.nan
        else:
            Res["VZO"] = dose / Res["AUCIFO"] / Res["LAMZ"]
            Res["VZP"] = dose / Res["AUCIFP"] / Res["LAMZ"]
            Res["CLO"] = dose / Res["AUCIFO"]
            Res["CLP"] = dose / Res["AUCIFP"]
            Res["MRTIVLST"] = Res["AUMCLST"] / Res["AUCLST"] - dur / 2
            Res["MRTIVIFO"] = Res["AUMCIFO"] / Res["AUCIFO"] - dur / 2
            Res["MRTIVIFP"] = Res["AUMCIFP"] / Res["AUCIFP"] - dur / 2
            Res["VSSO"] = Res["MRTIVIFO"] * Res["CLO"]
            Res["VSSP"] = Res["MRTIVIFP"] * Res["CLP"]

    if isinstance(iAUC, pd.DataFrame) and not iAUC.empty:
        niAUC = len(iAUC)
        if niAUC > 0:
            RetNames1.extend(iAUC['Name'].astype(str))
            for _, row in iAUC.iterrows():
                if adm.upper().strip() == "BOLUS":
                    Res[row['Name']] = IntAUC(x2, y2, row['Start'], row['End'], Res, down=down)
                else:
                    Res[row['Name']] = IntAUC(x, y, row['Start'], row['End'], Res, down=down)
                Units = Units.append(pd.Series(Units.loc['AUCLST'], name=row['Name']))
    else:
        niAUC = 0

    for key in Res:
        if key in Units.index:
            Res[key] *= Units.loc[key, 2]

    Res['units'] = Units.loc[RetNames1, 1].tolist()
    Res['UsedPoints'] = tRes["UsedPoints"]

    return Res


def Interpol(x, y, xnew, Slope=0, b0=0, down="Linear"):
    Result = [x, y]
    n = len(x)

    if n != len(y):
        warnings.warn("Interpol: Length of x and y are different!")
        newN = min(n, len(y))
        x = x[:newN]
        y = y[:newN]

    if not (isinstance(x, (list, np.ndarray)) and isinstance(y, (list, np.ndarray)) and isinstance(down, str)):
        return Result

    if xnew in x:
        return Result

    LEFT = np.sum(x < xnew) > 0
    RIGHT = np.sum(x > xnew) > 0

    if LEFT:
        idx = np.max(np.where(x < xnew))
        x1 = x[idx]
        y1 = y[idx]

    if RIGHT:
        idx = np.min(np.where(x > xnew))
        x2 = x[idx]
        y2 = y[idx]

    if LEFT and RIGHT:
        if down.strip().upper() == "LOG" and y2 < y1 and y2 > 0:
            ynew = np.exp(np.log(y1) + (np.log(y2) - np.log(y1)) / (x2 - x1) * (xnew - x1))
        else:
            ynew = y1 + (y2 - y1) / (x2 - x1) * (xnew - x1)
    elif LEFT and not RIGHT:
        ynew = np.exp(b0 - Slope * xnew)
    elif not LEFT and RIGHT:
        ynew = y2 / x2 * xnew
    else:
        return Result

    new_x = np.sort(np.append(x, xnew))
    new_y = np.array(y + [ynew])[np.argsort(np.append(x, xnew))]

    Result = [new_x, new_y]
    return Result


def LinAUC(x, y):
    """
    This function calculates the linear AUC.
    Actual implementation needed.
    """
    # Placeholder implementation
    auc = np.trapz(y, x)
    return np.array([auc])

def LogAUC(x, y):
    """
    This function calculates the logarithmic AUC.
    Actual implementation needed.
    """
    # Placeholder implementation
    log_y = np.log(y)
    auc = np.trapz(np.exp(log_y), x)
    return np.array([auc])


# 아래는 구현되지 않은 함수들의 placeholder입니다.
def BestSlope(x, y, adm, excludeDelta):
    # 이 함수는 실제로 구현되어야 합니다.
    return {"LAMZNPT": 0, "R2ADJ": 0, "LAMZLL": 0, "LAMZUL": 0, "UsedPoints": 0}


def DetSlope(x, y, SubTitle, sel_1=None, sel_2=None):
    # 이 함수는 실제로 구현되어야 합니다.
    return {"LAMZNPT": 0, "R2ADJ": 0, "LAMZLL": 0, "LAMZUL": 0, "UsedPoints": 0}


def AUC(x, y, down):
    n = len(x)
    Result = np.full((n, 2), np.nan)

    if n != len(y) or not isinstance(x, (list, np.ndarray)) or not isinstance(y, (list, np.ndarray)):
        return Result

    Res = np.zeros((n, 2))

    for i in range(1, n):
        if y[i] >= y[i - 1]:
            Res[i, 0] = (x[i] - x[i - 1]) * (y[i] + y[i - 1]) / 2
            Res[i, 1] = (x[i] - x[i - 1]) * (x[i] * y[i] + x[i - 1] * y[i - 1]) / 2
        elif down.strip().upper() == "LINEAR":
            Res[i, 0] = (x[i] - x[i - 1]) * (y[i] + y[i - 1]) / 2
            Res[i, 1] = (x[i] - x[i - 1]) * (x[i] * y[i] + x[i - 1] * y[i - 1]) / 2
        elif down.strip().upper() == "LOG":
            k = (np.log(y[i - 1]) - np.log(y[i])) / (x[i] - x[i - 1])
            Res[i, 0] = (y[i - 1] - y[i]) / k
            Res[i, 1] = (x[i - 1] * y[i - 1] - x[i] * y[i]) / k + (y[i - 1] - y[i]) / k / k
        else:
            Res[i, 0] = np.nan
            Res[i, 1] = np.nan

    Result = np.column_stack((np.cumsum(Res[:, 0]), np.cumsum(Res[:, 1])))
    return Result


def IntAUC(x, y, t1, t2, Res, down="Linear"):
        if all(y == 0) and min(x[~np.isnan(x)]) <= t1 and max(x[~np.isnan(x)]) >= t2:
            return 0

        n = len(x)
        if n != len(y) or not isinstance(x, (list, np.ndarray)) or not isinstance(y, (list, np.ndarray)):
            return np.nan

        if np.isnan(Res["TLST"]) or t1 > Res["TLST"]:
            return np.nan

        tL = Res["TLST"]

        if t2 > max(x[~np.isnan(y)]) and np.isnan(Res["LAMZ"]):
            return np.nan

        newSeries = Interpol(x, y, t1, Res["LAMZ"], Res["b0"], down=down)
        newSeries = Interpol(newSeries[0], newSeries[1], t2, Res["LAMZ"], Res["b0"], down=down)
        x = newSeries[0]
        y = newSeries[1]

        if down.strip().upper() == "LINEAR":
            if t2 <= tL:
                mask = (x >= t1) & (x <= t2)
                Result = LinAUC(x[mask], y[mask])[0]
            else:
                mask1 = (x >= t1) & (x <= tL)
                mask2 = (x >= tL) & (x <= t2)
                Result = LinAUC(x[mask1], y[mask1])[0] + LogAUC(x[mask2], y[mask2])[0]
        elif down.strip().upper() == "LOG":
            mask = (x >= t1) & (x <= t2)
            Result = LogAUC(x[mask], y[mask])[0]
        else:
            Result = np.nan

        return Result


def Unit(doseUnit, timeUnit, concUnit, MW):
    # 이 함수는 실제로 구현되어야 합니다.
    return pd.DataFrame(index=['AUCLST'], columns=[1, 2]).fillna(1)


# Note: Many helper functions (BestSlope, DetSlope, AUC, IntAUC, Unit)
# need to be implemented separately

def tbNCA(concData: pd.DataFrame, key: Union[str, List[str]] = "Subject", colTime: str = "Time", colConc: str = "conc",
          dose: Union[float, List[float]] = 0, adm: str = "Extravascular", dur: float = 0, doseUnit: str = "mg",
          timeUnit: str = "h", concUnit: str = "ug/L",down: str = "Linear", R2ADJ: float = 0, MW: float = 0,
          SS: bool = False, iAUC: str = "", excludeDelta: float = 1):

    """
    concData, key, colTime, colConc, dose, adm, dur, doseUnit = df, ["ID", "FEEDING"], "ATIME", "CONC", 100, "Extravascular", 0, "mg"
    timeUnit, concUnit, down, R2ADJ = "h", "ug/L", "Log", 0
    MW, SS, iAUC, excludeDelta = 0, False, "", 1
    """

    if isinstance(key, str):
        key = [key]
    nKey = len(key)

    for k in key:
        if concData[k].isna().sum() > 0:
            raise ValueError(f"{k} has NA value, which is not allowed!")

    IDs = concData[key].drop_duplicates()
    nID = len(IDs)

    if isinstance(dose, (int, float)):
        dose = [dose] * nID
    elif len(dose) != nID:
        raise ValueError("Count of dose does not match with number of NCAs!")

    Res = []
    for i, row in IDs.iterrows():
        strHeader = ", ".join([f"{k}={v}" for k, v in row.items()])

        mask = np.ones(len(concData), dtype=bool)
        for k, v in row.items():
            mask &= (concData[k] == v)

        tData = concData[mask]

        if len(tData) > 0:
            tRes = sNCA(tData[colTime], tData[colConc],
                        dose=dose[i], adm=adm, dur=dur, doseUnit=doseUnit,
                        timeUnit=timeUnit, concUnit=concUnit, R2ADJ=R2ADJ,
                        down=down, MW=MW, SS=SS, iAUC=iAUC,
                        Keystring=strHeader, excludeDelta=excludeDelta)
            Res.append(tRes)

    Res = pd.concat([IDs.reset_index(drop=True), pd.DataFrame(Res)], axis=1)
    Res.columns = key + list(Res.columns[nKey:])

    # Assuming sNCA returns a pandas Series with 'units' attribute
    units = [""] * nKey + tRes.attrs.get('units', [])
    Res.attrs['units'] = units

    return Res


# 작업 디렉토리 설정
os.chdir('C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK_analysis')

# CSV 파일 읽기
df = pd.read_csv('./CKD379_ConcPrep_Sitagliptin(R).csv')

# NCA 분석 수행
nca_result = tbNCA(df,
                     group_by=['ID', 'FEEDING'],
                     time_col='ATIME',
                     conc_col='CONC',
                     dose=100,
                     conc_unit='ug/L')




# Note: The sNCA function is not provided in the original code, so you'll need to implement or import it separately