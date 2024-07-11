import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from scipy.stats import linregress

def tblNCA(concData, key="Subject", colTime="Time", colConc="conc", dose=0, adm="Extravascular", dur=0, doseUnit="mg", timeUnit="h", concUnit="ug/L", down="Linear", R2ADJ=0, MW=0, SS=False, iAUC="", excludeDelta=1):
    concData = pd.DataFrame(concData)
    nKey = len(key)

    for i in range(nKey):
        if concData[key[i]].isna().sum() > 0:
            raise ValueError(f"{key[i]} has NA value, which is not allowed!")

    IDs = concData[key].drop_duplicates().reset_index(drop=True)
    nID = len(IDs)

    if isinstance(dose, (int, float)):
        dose = [dose] * nID
    elif len(dose) != nID:
        raise ValueError("Count of dose does not match with number of NCAs!")

    Res = []

    for i in range(nID):
        strHeader = f"{key[0]}={IDs.loc[i, key[0]]}"
        strCond = f"concData[concData['{key[0]}'] == '{IDs.loc[i, key[0]]}']"

        if nKey > 1:
            for j in range(1, nKey):
                strCond += f" & (concData['{key[j]}'] == '{IDs.loc[i, key[j]]}')"
                strHeader += f", {key[j]}={IDs.loc[i, key[j]]}"

        tData = concData.query(strCond)

        if not tData.empty:
            tRes = sNCA(tData[colTime], tData[colConc],
                        dose=dose[i], adm=adm, dur=dur, doseUnit=doseUnit,
                        timeUnit=timeUnit, concUnit=concUnit, R2ADJ=R2ADJ,
                        down=down, MW=MW, SS=SS, iAUC=iAUC,
                        Keystring=strHeader, excludeDelta=excludeDelta)
            Res.append(tRes)

    Res = pd.concat(Res, ignore_index=True)
    Res = pd.concat([IDs, Res], axis=1)

    units = [""] * nKey + list(getattr(tRes, 'units', []))
    Res.attrs['units'] = units

    return Res


def Unit(code="", timeUnit="h", concUnit="ng/mL", doseUnit="mg", MW=0):
    result = {"Unit": np.nan, "Factor": np.nan}

    if len(doseUnit.split("/")) != 1:
        return result

    if not isinstance(MW, (int, float)):
        return result

    if MW < 0:
        return result

    rGram = {"g": 1, "mg": 1000, "ug": 1e6, "ng": 1e9, "pg": 1e12}
    rMol = {"mol": 1, "mmol": 1000, "umol": 1e6, "nmol": 1e9, "pmol": 1e12}

    doseUnit = doseUnit.lower()
    timeUnit = timeUnit.lower()
    concUnit = concUnit.lower()

    concUnit_map = {
        "mg/ml": "g/l",
        "ug/ml": "mg/l",
        "ng/ml": "ug/l",
        "pg/ml": "ng/l",
        "mmol/ml": "mol/l",
        "umul/ml": "mmol/l",
        "nmol/ml": "umol/l",
        "pmol/ml": "nmol/l"
    }

    concUnit = concUnit_map.get(concUnit.lower(), concUnit)

    tConc = concUnit.split("/")
    uAmt = tConc[0]
    uVol = tConc[1]

    if ((uAmt in rMol and doseUnit in rGram) or (uAmt in rGram and doseUnit in rMol)):
        if MW == 0:
            print("Warning: Molecular weight should be given for more informative results!")

    TestCD = ["b0", "CMAX", "CMAXD", "TMAX", "TLAG", "CLST",
              "CLSTP", "TLST", "LAMZHL", "LAMZ", "LAMZLL", "LAMZUL",
              "LAMZNPT", "CORRXY", "R2", "R2ADJ", "C0", "AUCLST",
              "AUCALL", "AUCIFO", "AUCIFOD", "AUCIFP", "AUCIFPD",
              "AUCPEO", "AUCPEP", "AUCPBEO", "AUCPBEP", "AUMCLST",
              "AUMCIFO", "AUMCIFP", "AUMCPEO", "AUMCPEP", "MRTIVLST",
              "MRTIVIFO", "MRTIVIFP", "MRTEVLST", "MRTEVIFO", "MRTEVIFP",
              "VZO", "VZP", "VZFO", "VZFP", "CLO", "CLP", "CLFO",
              "CLFP", "VSSO", "VSSP"]

    nTestCD = len(TestCD)
    Res = pd.DataFrame({"Unit": [""] * nTestCD, "Factor": [1] * nTestCD}, index=TestCD)

    for i in range(nTestCD):
        Code = TestCD[i]
        if Code in ["CMAX", "CLST", "CLSTP", "C0"]:
            Res.loc[Code, "Unit"] = concUnit
        if Code == "CMAXD":
            Res.loc[Code, "Unit"] = f"{concUnit}/{doseUnit}"
        if Code in ["TMAX", "TLAG", "TLST", "LAMZHL", "LAMZLL", "LAMZUL",
                    "MRTIVLST", "MRTIVIFO", "MRTIVIFP", "MRTEVLST",
                    "MRTEVIFO", "MRTEVIFP"]:
            Res.loc[Code, "Unit"] = timeUnit
        if Code == "LAMZ":
            Res.loc[Code, "Unit"] = f"/{timeUnit}"
        if Code in ["b0", "LAMZNPT", "CORRXY", "R2", "R2ADJ"]:
            Res.loc[Code, "Unit"] = ""
        if Code in ["AUCLST", "AUCALL", "AUCIFO", "AUCIFP"]:
            Res.loc[Code, "Unit"] = f"{timeUnit}*{concUnit}"
        if Code in ["AUCIFOD", "AUCIFPD"]:
            Res.loc[Code, "Unit"] = f"{timeUnit}*{concUnit}/{doseUnit}"
        if Code in ["AUCPEO", "AUCPEP", "AUCPBEO", "AUCPBEP",
                    "AUMCPEO", "AUMCPEP"]:
            Res.loc[Code, "Unit"] = "%"
        if Code in ["AUMCLST", "AUMCIFO", "AUMCIFP"]:
            Res.loc[Code, "Unit"] = f"{timeUnit}^2*{concUnit}"
        if Code in ["VZO", "VZP", "VZFO", "VZFP", "VSSO", "VSSP"]:
            if uAmt in rMol and doseUnit in rGram:
                Res.loc[Code, ["Unit", "Factor"]] = [uVol, rMol[uAmt] / rGram[doseUnit] / MW]
            elif uAmt in rGram and doseUnit in rMol:
                Res.loc[Code, ["Unit", "Factor"]] = [uVol, rGram[uAmt] / rMol[doseUnit] * MW]
            elif uAmt in rGram and doseUnit in rGram:
                Res.loc[Code, ["Unit", "Factor"]] = [uVol, rGram[uAmt] / rGram[doseUnit]]
            else:
                Res.loc[Code, ["Unit", "Factor"]] = [uVol, rMol[uAmt] / rMol[doseUnit]]
        if Code in ["CLO", "CLP", "CLFO", "CLFP"]:
            if uAmt in rMol and doseUnit in rGram:
                Res.loc[Code, ["Unit", "Factor"]] = [f"{uVol}/{timeUnit}", rMol[uAmt] / rGram[doseUnit] / MW]
            elif uAmt in rGram and doseUnit in rMol:
                Res.loc[Code, ["Unit", "Factor"]] = [f"{uVol}/{timeUnit}", rGram[uAmt] / rMol[doseUnit] * MW]
            elif uAmt in rGram and doseUnit in rGram:
                Res.loc[Code, ["Unit", "Factor"]] = [f"{uVol}/{timeUnit}", rGram[uAmt] / rGram[doseUnit]]
            else:
                Res.loc[Code, ["Unit", "Factor"]] = [f"{uVol}/{timeUnit}", rMol[uAmt] / rMol[doseUnit]]

    Res["Factor"] = pd.to_numeric(Res["Factor"], errors='coerce')
    Res.loc[Res["Factor"] == 0, "Factor"] = np.nan
    Res.loc[Res["Factor"] == np.inf, "Factor"] = np.nan

    if code == "":
        result = Res
    else:
        result = Res.loc[code, :].to_dict()

    return result


def slope(x, y):
    result = {
        "R2": np.nan,
        "R2ADJ": np.nan,
        "LAMZNPT": 0,
        "LAMZ": np.nan,
        "b0": np.nan,
        "CORRXY": np.nan,
        "LAMZLL": np.nan,
        "LAMZUL": np.nan
    }

    finite_mask = np.isfinite(x) & np.isfinite(y)
    x = x[finite_mask]
    y = y[finite_mask]
    n = len(x)

    if n == 1 or n != len(y) or not np.issubdtype(x.dtype, np.number) or not np.issubdtype(y.dtype, np.number):
        return result

    mx = np.mean(x)
    my = np.mean(y)
    Sxx = np.sum((x - mx) ** 2)
    Sxy = np.sum((x - mx) * (y - my))
    Syy = np.sum((y - my) ** 2)
    b1 = Sxy / Sxx

    if np.isnan(b1) or b1 > 0:
        return result

    result["LAMZNPT"] = n
    result["LAMZ"] = -b1
    result["b0"] = my - b1 * mx
    result["R2"] = b1 * Sxy / Syy
    result["R2ADJ"] = 1 - (1 - result["R2"]) * (n - 1) / (n - 2)
    result["CORRXY"] = np.sign(b1) * np.sqrt(result["R2"])
    result["LAMZLL"] = x[0]
    result["LAMZUL"] = x[-1]

    return result


def BestSlope(x, y, adm="Extravascular", TOL=1e-4, excludeDelta=1):
    result = {"R2": np.nan, "R2ADJ": np.nan, "LAMZNPT": 0, "LAMZ": np.nan,
              "b0": np.nan, "CORRXY": np.nan, "LAMZLL": np.nan, "LAMZUL": np.nan, "CLSTP": np.nan}

    if excludeDelta < 0:
        raise ValueError("Option excludeDelta should be non-negative!")

    n = len(x)
    if n == 0 or n != len(y) or not np.issubdtype(x.dtype, np.number) or not np.issubdtype(y.dtype,
                                                                                           np.number) or np.any(y < 0):
        result["LAMZNPT"] = 0
        return result

    if len(np.unique(y)) == 1:
        result["LAMZNPT"] = 0
        result["b0"] = np.unique(y)[0]
        return result

    r0 = result.copy()

    if adm.strip().upper() == "BOLUS":
        loc_start = np.argmax(y)
    else:
        loc_start = np.argmax(y) + 1

    loc_last = np.max(np.where(y > 0))

    if np.isnan(loc_start) or np.isnan(loc_last):
        result["LAMZNPT"] = 0
        return result

    if loc_last - loc_start < 2:
        r0["LAMZNPT"] = 0
    else:
        tmp_mat = np.full((loc_last - loc_start - 1, len(r0)), np.nan)
        for i in range(loc_start, loc_last - 1):
            tmp_mat[i - loc_start, :8] = slope(x[i:loc_last + 1], np.log(y[i:loc_last + 1]))

        tmp_mat = tmp_mat[np.isfinite(tmp_mat[:, 1]) & (tmp_mat[:, 2] > 2)]

        if tmp_mat.shape[0] > 0:
            max_adj_rsq = np.max(tmp_mat[:, 1])
            OKs = np.abs(max_adj_rsq - tmp_mat[:, 1]) < TOL
            n_max = np.max(tmp_mat[OKs, 2])
            r0 = tmp_mat[OKs & (tmp_mat[:, 2] == n_max)][0]
            r0["CLSTP"] = np.exp(r0[4] - r0[3] * np.max(x[np.isfinite(y)]))
        else:
            r0["LAMZNPT"] = 0

    if excludeDelta < 1:
        x1 = x[:-1]
        y1 = y[:-1]
        r1 = result.copy()

        if adm.strip().upper() == "BOLUS":
            loc_start = np.argmax(y1)
        else:
            loc_start = np.argmax(y1) + 1

        loc_last = np.max(np.where(y1 > 0))

        if loc_last - loc_start < 2:
            r1["LAMZNPT"] = 0
        else:
            tmp_mat = np.full((loc_last - loc_start - 1, len(r1)), np.nan)
            for i in range(loc_start, loc_last - 1):
                tmp_mat[i - loc_start, :8] = slope(x1[i:loc_last + 1], np.log(y1[i:loc_last + 1]))

            tmp_mat = tmp_mat[tmp_mat[:, 2] > 2]

            if tmp_mat.shape[0] > 0:
                max_adj_rsq = np.max(tmp_mat[:, 1])
                OKs = np.abs(max_adj_rsq - tmp_mat[:, 1]) < TOL
                n_max = np.max(tmp_mat[OKs, 2])
                r1 = tmp_mat[OKs & (tmp_mat[:, 2] == n_max)][0]
                r1["CLSTP"] = np.exp(r1[4] - r1[3] * np.max(x[np.isfinite(y)]))
            else:
                r1["LAMZNPT"] = 0

        if np.isnan(r1["R2ADJ"]):
            result = r0
        elif np.isnan(r0["R2ADJ"]):
            result = r1
        elif r1["R2ADJ"] - r0["R2ADJ"] > excludeDelta:
            result = r1
        else:
            result = r0
    else:
        result = r0

    if result["LAMZNPT"] > 0:
        result["UsedPoints"] = list(
            range(np.where(x == result["LAMZLL"])[0][0], np.where(x == result["LAMZUL"])[0][0] + 1))
    else:
        result["UsedPoints"] = None

    return result



def DetSlope(x, y, SubTitle="", sel_1=0, sel_2=0):
    def onpick(event):
        ind = event.ind[0]
        if not selected[ind]:
            selected[ind] = True
            ax.plot(x[ind], y[ind], 'o', color='red')
        else:
            selected[ind] = False
            ax.plot(x[ind], y[ind], 'o', color='blue')
        update_plot()

    def update_plot():
        ax.cla()
        ax.plot(x, y, 'o', picker=5)
        sel_indices = np.where(selected)[0]
        if len(sel_indices) > 1:
            slope, intercept, r_value, p_value, std_err = linregress(x[sel_indices], y[sel_indices])
            line = slope * x + intercept
            ax.plot(x, line, color='green')
            ax.legend([f'Adj. R-square={r_value ** 2:.3f}'], loc='upper right')
        fig.canvas.draw()

    x = np.array(x)
    y = np.array(y)
    finite_mask = np.isfinite(x) & np.isfinite(y) & (y != 0)
    x = x[finite_mask]
    y = np.log(y[finite_mask])

    if len(x) != len(y):
        raise ValueError("Length of A and B should be same.")
    if np.any(np.isnan(x)) or np.any(np.isnan(y)):
        raise ValueError("NAs are not allowed.")
    if not (np.issubdtype(x.dtype, np.number) and np.issubdtype(y.dtype, np.number)):
        raise ValueError("Only numeric vectors are allowed")

    selected = np.zeros(len(x), dtype=bool)

    fig, ax = plt.subplots()
    cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
    ax.plot(x, y, 'o', picker=5)
    ax.set_title("Choose points for terminal slope")
    ax.set_xlabel("Time")
    ax.set_ylabel("log(Concentration)")
    fig.suptitle(SubTitle)
    fig.canvas.mpl_connect('pick_event', onpick)
    plt.show()

    sel_indices = np.where(selected)[0]
    if len(sel_indices) < 2:
        return {"R2": np.nan, "R2ADJ": np.nan, "LAMZNPT": 0, "LAMZ": np.nan,
                "b0": np.nan, "CORRXY": np.nan, "LAMZLL": np.nan, "LAMZUL": np.nan, "CLSTP": np.nan}

    slope, intercept, r_value, p_value, std_err = linregress(x[sel_indices], y[sel_indices])

    result = {
        "R2": r_value ** 2,
        "R2ADJ": 1 - (1 - r_value ** 2) * (len(sel_indices) - 1) / (len(sel_indices) - 2),
        "LAMZNPT": len(sel_indices),
        "LAMZ": -slope,
        "b0": intercept,
        "CORRXY": r_value,
        "LAMZLL": x[sel_indices[0]],
        "LAMZUL": x[sel_indices[-1]],
        "CLSTP": np.exp(intercept - slope * np.max(x[np.isfinite(y)]))
    }
    result["UsedPoints"] = sel_indices

    return result


def AUC(x, y, down="Linear"):
    n = len(x)
    result = {"AUC": np.full(n, np.nan), "AUMC": np.full(n, np.nan)}

    if n != len(y) or not np.issubdtype(x.dtype, np.number) or not np.issubdtype(y.dtype, np.number):
        return result

    res = np.zeros((n, 2))
    res[0, :] = [0, 0]

    for i in range(1, n):
        if y[i] >= y[i - 1]:
            res[i, 0] = (x[i] - x[i - 1]) * (y[i] + y[i - 1]) / 2
            res[i, 1] = (x[i] - x[i - 1]) * (x[i] * y[i] + x[i - 1] * y[i - 1]) / 2
        elif down.strip().upper() == "LINEAR":
            res[i, 0] = (x[i] - x[i - 1]) * (y[i] + y[i - 1]) / 2
            res[i, 1] = (x[i] - x[i - 1]) * (x[i] * y[i] + x[i - 1] * y[i - 1]) / 2
        elif down.strip().upper() == "LOG":
            k = (np.log(y[i - 1]) - np.log(y[i])) / (x[i] - x[i - 1])
            res[i, 0] = (y[i - 1] - y[i]) / k
            res[i, 1] = (x[i - 1] * y[i - 1] - x[i] * y[i]) / k + (y[i - 1] - y[i]) / (k * k)
        else:
            res[i, :] = [np.nan, np.nan]

    result["AUC"] = np.cumsum(res[:, 0])
    result["AUMC"] = np.cumsum(res[:, 1])

    return result


def interpol(x, y, t, lamz, b0, down="Linear"):
    if t in x:
        return x, y

    new_x = np.append(x, t)
    if down.strip().upper() == "LINEAR":
        idx = np.argsort(new_x)
        new_y = np.interp(t, x, y)
    elif down.strip().upper() == "LOG":
        idx = np.argsort(new_x)
        new_y = np.exp(np.interp(t, x, np.log(y)))
    else:
        return x, y

    new_y = np.append(y, new_y)
    sorted_idx = np.argsort(new_x)
    return new_x[sorted_idx], new_y[sorted_idx]


def lin_auc(x, y):
    auc = np.trapz(y, x)
    return auc


def log_auc(x, y):
    k = (np.log(y[1:]) - np.log(y[:-1])) / (x[1:] - x[:-1])
    auc = np.sum((y[:-1] - y[1:]) / k)
    return auc


def IntAUC(x, y, t1, t2, Res, down="Linear"):
    if np.all(y == 0) and np.min(x) <= t1 and np.max(x) >= t2:
        return 0.0

    n = len(x)
    if n != len(y) or not np.issubdtype(x.dtype, np.number) or not np.issubdtype(y.dtype, np.number):
        return np.nan

    if np.isnan(Res.get("TLST")) or t1 > Res["TLST"]:
        return np.nan

    tL = Res["TLST"]
    if t2 > np.max(x[~np.isnan(y)]) and np.isnan(Res.get("LAMZ")):
        return np.nan

    x, y = interpol(x, y, t1, Res["LAMZ"], Res["b0"], down=down)
    x, y = interpol(x, y, t2, Res["LAMZ"], Res["b0"], down=down)

    if down.strip().upper() == "LINEAR":
        if t2 <= tL:
            result = lin_auc(x[(x >= t1) & (x <= t2)], y[(x >= t1) & (x <= t2)])
        else:
            result = (lin_auc(x[(x >= t1) & (x <= tL)], y[(x >= t1) & (x <= tL)]) +
                      log_auc(x[(x >= tL) & (x <= t2)], y[(x >= tL) & (x <= t2)]))
    elif down.strip().upper() == "LOG":
        result = log_auc(x[(x >= t1) & (x <= t2)], y[(x >= t1) & (x <= t2)])
    else:
        result = np.nan

    return result


def sNCA(x, y, dose=0, adm="Extravascular", dur=0, doseUnit="mg",
         timeUnit="h", concUnit="ug/L", iAUC=None, down="Linear",
         R2ADJ=0.7, MW=0, SS=False, Keystring="", excludeDelta=1):


    if not (isinstance(x, (list, np.ndarray)) and isinstance(y, (list, np.ndarray)) and
            isinstance(dose, (int, float)) and isinstance(dur, (int, float)) and
            isinstance(adm, str) and isinstance(down, str)):
        raise ValueError("Check input types!")

    if adm.strip().upper() == "INFUSION" and not (dur > 0):
        raise ValueError("Infusion mode should have dur larger than 0!")

    x = np.array(x)
    y = np.array(y)

    NApoints = np.isnan(x) | np.isnan(y)
    x = x[~NApoints]
    y = y[~NApoints]

    if not np.all(np.diff(x) >= 0):
        raise ValueError("Check if the x is sorted in order!")

    n = len(x)
    RetNames1 = ["b0", "CMAX", "CMAXD", "TMAX", "TLAG", "CLST",
                 "CLSTP", "TLST", "LAMZHL", "LAMZ", "LAMZLL", "LAMZUL",
                 "LAMZNPT", "CORRXY", "R2", "R2ADJ", "AUCLST", "AUCALL",
                 "AUCIFO", "AUCIFOD", "AUCIFP", "AUCIFPD", "AUCPEO",
                 "AUCPEP", "AUMCLST", "AUMCIFO", "AUMCIFP", "AUMCPEO",
                 "AUMCPEP"]

    if adm.strip().upper() == "BOLUS":
        RetNames1.extend(["C0", "AUCPBEO", "AUCPBEP"])

    if adm.strip().upper() == "EXTRAVASCULAR":
        RetNames1.extend(["VZFO", "VZFP", "CLFO", "CLFP", "MRTEVLST",
                          "MRTEVIFO", "MRTEVIFP"])
    else:
        RetNames1.extend(["VZO", "VZP", "CLO", "CLP", "MRTIVLST",
                          "MRTIVIFO", "MRTIVIFP", "VSSO", "VSSP"])

    Res = {name: np.nan for name in RetNames1}

    if n == 0 or n != len(y) or np.any(y < 0):
        Res["LAMZNPT"] = 0
        return Res

    Units = Unit(doseUnit=doseUnit, timeUnit=timeUnit, concUnit=concUnit, MW=MW)
    uY = np.unique(y)

    if len(uY) == 1:
        Res["CMAX"] = uY[0]
        if dose > 0:
            Res["CMAXD"] = uY[0] / dose
        Res["TMAX"] = x[np.where(y == uY)[0][0]]

        if uY[0] == 0:
            Res["TLAG"] = np.nan
            Res["AUCALL"] = 0
        elif np.where(y == uY)[0][0] > 0:
            Res["TLAG"] = x[np.where(y == uY)[0][0] - 1]
        else:
            Res["TLAG"] = 0

        Res["CLST"] = np.nan if uY[0] == 0 else uY[0]
        Res["TLST"] = np.nan if uY[0] == 0 else x[np.where(y == uY)[0][0]]
        Res["LAMZNPT"] = 0
        Res["b0"] = uY[0]

        if isinstance(iAUC, pd.DataFrame):
            niAUC = len(iAUC)
            if niAUC > 0:
                RetNames1 = list(set(RetNames1).union(iAUC["Name"]))
                for i in range(niAUC):
                    if np.all(y == 0) and np.min(x) <= min(0, iAUC.loc[i, "Start"]) and np.max(x) >= iAUC.loc[i, "End"]:
                        Res[iAUC.loc[i, "Name"]] = 0
                    elif adm.strip().upper() == "BOLUS":
                        if np.sum(x == 0) == 0:
                            x2 = np.concatenate(([0], x))
                            y2 = np.concatenate(([uY[0]], y))
                        Res[iAUC.loc[i, "Name"]] = IntAUC(x2, y2, iAUC.loc[i, "Start"], iAUC.loc[i, "End"], Res,
                                                          down=down)
                    else:
                        Res[iAUC.loc[i, "Name"]] = IntAUC(x, y, iAUC.loc[i, "Start"], iAUC.loc[i, "End"], Res,
                                                          down=down)
                    Units = Units.append(Units.loc["AUCLST", :], ignore_index=True)
                    Units.index = list(Units.index[:-1]) + [iAUC.loc[i, "Name"]]
        else:
            niAUC = 0

        for key in Res.keys():
            Res[key] *= Units.loc[key, 1]

        Res["units"] = list(Units.loc[RetNames1, 0]) + [Units.loc["AUCLST", 0]] * niAUC
        return Res

    iLastNonZero = np.max(np.where(y > 0))
    x0 = x[:iLastNonZero + 1]
    y0 = y[:iLastNonZero + 1]
    x1 = x0[y0 != 0]
    y1 = y0[y0 != 0]

    if adm.strip().upper() == "BOLUS":
        if y[0] > y[1] and y[1] > 0:
            C0 = np.exp(-x[0] * (np.log(y[1]) - np.log(y[0])) / (x[1] - x[0]) + np.log(y[0]))
        else:
            C0 = y[np.where(x == np.min(x[y > 0]))[0][0]]
        x2 = np.concatenate(([0], x))
        y2 = np.concatenate(([C0], y))
        x3 = np.concatenate(([0], x0))
        y3 = np.concatenate(([C0], y0))
    else:
        if not np.any(x == 0):
            x2 = np.concatenate(([0], x))
            y2 = np.concatenate(([0], y))
            x3 = np.concatenate(([0], x0))
            y3 = np.concatenate(([0], y0))
        else:
            x2 = x
            y2 = y
            x3 = x0
            y3 = y0

    tRes = BestSlope(x, y, adm, excludeDelta=excludeDelta)

    if R2ADJ > 0:
        if tRes["LAMZNPT"] < 2:
            tRes = DetSlope(x1, y1, Keystring)
        elif tRes["R2ADJ"] < R2ADJ:
            tRes = DetSlope(x1, y1, Keystring, sel1=np.where(x1 == tRes["LAMZLL"])[0], sel2=np.where(x1 == tRes["LAMZUL"])[0])

    tRes["UsedPoints"] = tRes.get("UsedPoints", 0) + np.where(x == tRes["LAMZLL"])[0][0] - \
                          np.where(x1 == tRes["LAMZLL"])[0][0]
    for key in ["R2", "R2ADJ", "LAMZNPT", "LAMZ", "b0", "CORRXY", "LAMZLL", "LAMZUL", "CLSTP"]:
        Res[key] = tRes[key]

    tab_auc = AUC(x3, y3, down)
    Res["AUCLST"], Res["AUMCLST"] = tab_auc[-1]
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
    Res["AUMCIFO"] = Res["AUMCLST"] + Res["CLST"] * Res["TLST"] / Res["LAMZ"] + Res["CLST"] / Res["LAMZ"] ** 2
    Res["AUMCIFP"] = Res["AUMCLST"] + Res["CLSTP"] * Res["TLST"] / Res["LAMZ"] + Res["CLSTP"] / Res["LAMZ"] ** 2
    Res["AUMCPEO"] = (1 - Res["AUMCLST"] / Res["AUMCIFO"]) * 100
    Res["AUMCPEP"] = (1 - Res["AUMCLST"] / Res["AUMCIFP"]) * 100

    if not np.isnan(dose) and dose > 0:
        Res["CMAXD"] = Res["CMAX"] / dose
        Res["AUCIFOD"] = Res["AUCIFO"] / dose
        Res["AUCIFPD"] = Res["AUCIFP"] / dose

    if adm.strip().upper() == "BOLUS":
        Res["C0"] = C0
        Res["AUCPBEO"] = tab_auc[1, 0] / Res["AUCIFO"] * 100
        Res["AUCPBEP"] = tab_auc[1, 0] / Res["AUCIFP"] * 100
    else:
        if np.sum(y0 == 0) > 0:
            Res["TLAG"] = x0[np.max(np.where(y0 == 0))]
        else:
            Res["TLAG"] = 0
        if not np.isnan(x0[np.where(x0 == 0)][0]):
            if y0[np.where(x0 == 0)] > 0:
                Res["TLAG"] = 0

    if adm.strip().upper() == "EXTRAVASCULAR":
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

    if isinstance(iAUC, pd.DataFrame):
        niAUC = len(iAUC)
        if niAUC > 0:
            ret_names1 = list(set(RetNames1).union(iAUC["Name"]))
            for i in range(niAUC):
                if adm.strip().upper() == "BOLUS":
                    Res[iAUC.loc[i, "Name"]] = IntAUC(x2, y2, iAUC.loc[i, "Start"], iAUC.loc[i, "End"], Res, down=down)
                else:
                    Res[iAUC.loc[i, "Name"]] = IntAUC(x, y, iAUC.loc[i, "Start"], iAUC.loc[i, "End"], Res, down=down)
                units = units.append(units.loc["AUCLST", :], ignore_index=True)
                units.index = list(units.index[:-1]) + [iAUC.loc[i, "Name"]]
    else:
        niAUC = 0

    for key in Res.keys():
        Res[key] *= units.loc[key, 1]

    Res["units"] = units.loc[RetNames1, 0].values.tolist() + [units.loc["AUCLST", 0]] * niAUC
    Res["UsedPoints"] = tRes.get("UsedPoints", [])
    return Res


df=pd.read_csv('C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK_analysis/CKD379_ConcPrep_Sitagliptin(R).csv')

tblNCA(df, key=["ID","FEEDING"], colTime="ATIME", colConc="CONC",
             dose=100, adm="Extravascular", dur=0, doseUnit="mg",
             timeUnit="h", concUnit="ug/L", down="Log", R2ADJ=0,
             MW=0, SS=False, iAUC="", excludeDelta=1)