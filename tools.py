import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from scipy.stats import linregress
import seaborn as sns

## For Visualization

def g_mean(x):
    return np.exp((x.map(np.log)).mean())

def load_data_dict(drug_list, filename_format, input_file_dir_path):
    drug_prep_df_dict = dict()
    for drug in drug_list:
        result_file_path = f"{input_file_dir_path}/" + filename_format.replace('[drug]',drug)
        if filename_format.split('.')[-1]=='csv':
            drug_prep_df_dict[drug] = pd.read_csv(result_file_path)
        if filename_format.split('.')[-1] == 'xls':
            drug_prep_df_dict[drug] = pd.read_excel(result_file_path)
        drug_prep_df_dict[drug]['FEEDING'] = drug_prep_df_dict[drug]['FEEDING'].replace('FASTING','FASTED')
        # drug_prep_df_dict[drug]['Subject'] = drug_prep_df_dict[drug].apply(lambda row:f'{row["ID"]}|{row["FEEDING"]}',axis=1)
    return drug_prep_df_dict

def time_to_conc_graph_ckd(gdf, sid_list, drug, hue, result_file_dir_path, hue_order=None, file_format='png', dpi=300, estimator=np.mean, yscale='linear', save_fig=True):

    g_palette = 'Dark2'
    g_palette_colors = sns.color_palette('Dark2')
    sns.set_style("whitegrid", {'grid.linestyle': ':',
                                })

    mode = 'Individual' if len(sid_list)==1 else 'Population'
    if mode=='Individual':
        title_str = sid_list[0]
        last_tag = '('+sid_list[0]+')'
        time_col = 'ATIME'
    else:
        # if errorbar[0]=='sd':
        #     if errorbar[1]==1: errorbar_str = f' ({errorbar[0].upper()})'
        #     else: errorbar_str = f' ({errorbar[1]} {errorbar[0].upper()})'
        # elif errorbar[0]=='ci':
        #     errorbar_str = f' ({errorbar[1]}% {errorbar[0].upper()})'
        # else:
        #     errorbar_str = ''
        # title_str = f'Sample Mean{errorbar_str}'
        # last_tag = 'sample'+str(tuple(sid_list)).replace(",)",")").replace("'","")
        last_tag = 'sample'
        time_col = 'NTIME'
    filename = f'{mode}_{drug}_{last_tag}'

    act_gdf = gdf[gdf['ID'].isin(sid_list)].copy()

    marker_list = ['o', '^', 'v','<', '>', 's', 'p', '*', 'h', 'H', 'D', 'd', '+', 'x', '|', '_']
    # g = sns.relplot(data=act_gdf, x=time_col,y='CONC', palette=g_palette, marker='o',hue=hue, hue_order=hue_order, markersize=7, markeredgecolor='white', markeredgewidth=1, kind='line', linewidth=1.5, linestyle='--', errorbar=errorbar, estimator=estimator, err_style=err_style)
    g = sns.relplot(data=act_gdf, x=time_col, y='CONC', palette=g_palette, markers=marker_list[:len(hue_order)], hue=hue, hue_order=hue_order, style=hue, style_order=hue_order, markersize=10, markeredgecolor='white', markeredgewidth=1, kind='line', linewidth=2, estimator=estimator, errorbar=None)
    # g = sns.relplot(data=act_gdf, x=time_col, y='CONC', palette=g_palette, marker='o', hue=hue, hue_order=hue_order, markersize=7, markeredgecolor='white', markeredgewidth=1, kind='line', linewidth=1.5, linestyle='--', estimator=estimator, errorbar=None)
    # errorbar = ("sd", 2), err_style = 'band',
    # plt.setp(plt.gca().get_lines()[1], fillstyle='none')

    if mode=='Population':

        ## 에러바 데이터 생성

        eb_df_dict = dict()
        for hue_inx, hue_act_gdf in act_gdf.groupby(hue):
            for_eb_df = hue_act_gdf.groupby('NTIME')['CONC'].agg([np.nanmean, np.nanstd]).reset_index(drop=False)
            eb_x = tuple(for_eb_df['NTIME'])
            eb_y = tuple(for_eb_df['nanmean'])
            eb_y_errbar = tuple(for_eb_df['nanstd'])

            eb_df_dict[hue_inx] = {'for_eb_df':for_eb_df,'eb_x':eb_x, 'eb_y':eb_y, 'eb_y_errbar':eb_y_errbar}

        hue_order_dict = dict([(ho,i) for i, ho in enumerate(hue_order)])
        for hue_eb_key, hue_eb_val in eb_df_dict.items():
            g.ax.errorbar(hue_eb_val['eb_x'], hue_eb_val['eb_y'], yerr=[tuple(np.zeros(len(eb_y))), hue_eb_val['eb_y_errbar']], fmt='o', ecolor=g_palette_colors[hue_order_dict[hue_eb_key]], capsize=2.5, capthick=2,barsabove=True)


    # eb.get_children()[3].set_linestyle('--')  ## 에러 바 라인 스타일
    # eb.get_children()[1].set_marker('v') ## 에러 바 아래쪽 마커 스타일
    # eb.get_children()[2].set_marker('^') ## 에러 바 위쪽 마커 스타일
    # palette = sns.color_palette('Dark2')


    # g.fig.set_size_inches(15,11)
    g.fig.set_size_inches(15, 11)
    # g.fig.subplots_adjust(left=0.1, right=0.1)

    if yscale=="log": g.set(yscale="log")
    else: pass
    # g.set_axis_labels('Time (hr)', 'Concentration (mg/L)')
    # sns.move_legend(g, 'upper right', frameon=True)
    # g.fig.subplots_adjust(top=0.85)
    sns.move_legend(g, 'center right', title=None, frameon=False, fontsize=18)
    # sns.move_legend(g, 'upper center', ncol=2, title=None, frameon=False, fontsize=15)
    # g.fig.suptitle("A001", fontsize=20, fontweight='bold')
    # plt.title(title_str, fontsize=20)
    plt.tight_layout(pad=3.5)

    plt.xlabel('Time (h)', fontsize=20, labelpad=8)
    plt.ylabel(f'{drug} plasma concentration (μg/L)', fontsize=20, labelpad=8)

    plt.xticks(np.arange(-6,54, step=6), fontsize=18)
    plt.xlim(-1,54)

    if drug=='Metformin':
        if yscale=='linear':
            plt.yticks(np.linspace(0, 2500, 11, endpoint=True), fontsize=18)
            plt.ylim(-50, 2500)
        elif yscale=='log':
            plt.yticks([0,1,10,100,1000,3500], fontsize=18)
            plt.ylim(1, 3500)
    else:
        if yscale == 'linear':
            plt.yticks(np.linspace(0, 650, 11, endpoint=True), fontsize=18)
            plt.ylim(-10,650)
        elif yscale=='log':
            plt.yticks([0,1,10,100,1000], fontsize=18)
            plt.ylim(1, 1000)


    if save_fig:
        if not os.path.exists(f"{result_file_dir_path}"): os.mkdir(f"{result_file_dir_path}")
        if not os.path.exists(f"{result_file_dir_path}/{yscale}"): os.mkdir(f"{result_file_dir_path}/{yscale}")
        if not os.path.exists(f"{result_file_dir_path}/{yscale}/{mode}"): os.mkdir(f"{result_file_dir_path}/{yscale}/{mode}")
        if not os.path.exists(f"{result_file_dir_path}/{yscale}/{mode}/{drug}"): os.mkdir(f"{result_file_dir_path}/{yscale}/{mode}/{drug}")
        plt.savefig(f"{result_file_dir_path}/{yscale}/{mode}/{drug}/{filename}.{file_format}", dpi=dpi)


## For NCA Core

def tblNCA(concData, key="Subject", colTime="Time", colConc="conc", dose=0, tau=0, adm="Extravascular", dur=0, doseUnit="mg",
           timeUnit="h", concUnit="ug/L", down="Linear", R2ADJ=0, MW=0, SS=False, iAUC="", excludeDelta=1, slopeMode='BEST'):
    """
    slopeMode : 'Best', 'SNUHCPT', 'Det'

    concData, key, colTime, colConc, dose, adm, dur, doseUnit = df, ["ID", "FEEDING"], "ATIME", "CONC", 100, "Extravascular", 0, "mg"
    timeUnit, concUnit, down, R2ADJ = "h", "ug/L", "Log", 0
    MW, SS, iAUC, excludeDelta = 0, False, "", 1
    dose='DOSE'
    slopeMode='SNUHCPT'
    tau=np.nan

    """

    concData = pd.DataFrame(concData)
    nKey = len(key)

    if type(key) == str:
        if concData[key].isna().sum() > 0:
            raise ValueError(f"{key} has NA value, which is not allowed!")
        key = [key, ]
    else:
        for idcol in key:
            if concData[idcol].isna().sum() > 0:
                raise ValueError(f"{idcol} has NA value, which is not allowed!")

    IDs = concData[key].drop_duplicates().reset_index(drop=True)
    nID = len(IDs)

    # Tau와 관련하여 (multiple / single 투여 구분)

    if isinstance(tau, (int, float)):
        if np.isnan(tau) or tau <= 0:
            tau = [np.nan] * nID
        else:
            tau = [tau] * nID
    elif isinstance(tau, (str,)):
        if isinstance(dose, (str,)):
            tau_df = concData.drop_duplicates(subset=key + [dose], ignore_index=True)[tau]
        else:
            tau_df = concData.drop_duplicates(subset=key, ignore_index=True)[tau]
        if len(tau_df) != nID:
            raise ValueError(
                "Count of dose does not match with number of NCAs. Unique dose should be applied to each ID")
        tau = list(tau_df[tau])
    elif isinstance(list(tau), (list,)):
        if len(tau) != nID:
            raise ValueError("Count of dose does not match with number of NCAs!")
        tau = list(tau)
    IDs['TAU'] = tau
    if np.any(tau == 0) or np.any(np.isnan(tau)):
        ms_type = 'single'
    else:
        ms_type = 'multiple'

    # Dose와 관련하여

    if isinstance(dose, (int, float)):
        dose = [dose] * nID
        # IDs['PyNCA_Dose_Col'] = dose
    elif isinstance(dose, (str,)):
        dose_df = concData[key + [dose]].drop_duplicates(ignore_index=True)
        if len(dose_df) != nID:
            raise ValueError("Count of dose does not match with number of NCAs. Unique dose should be applied to each ID")
        dose = list(dose_df[dose])
    elif isinstance(list(dose), (list,)):
        if len(dose) != nID:
            raise ValueError("Count of dose does not match with number of NCAs!")
        dose = list(dose)
    IDs['DOSE'] = dose

    Res = []

    # 군별 NCA 시행
    # i=0
    for i in range(nID):
        strHeader = f"{key[0]}={IDs.loc[i, key[0]]}"
        cond = (concData[key[0]] == IDs.loc[i, key[0]])
        grp_dict = {key[0]: IDs.loc[i, key[0]]}

        if nKey > 1:
            for j in range(1, nKey):
                cond &= (concData[key[j]] == IDs.loc[i, key[j]])
                strHeader += f", {key[j]}={IDs.loc[i, key[j]]}"
                grp_dict[key[j]] = IDs.loc[i, key[j]]

        tData = concData[cond]

        if not tData.empty:
            # individual subject에서 NCA 시행

            tRes = sNCA(tData[colTime].values, tData[colConc].values,
                        dose=dose[i], tau=tau[i], adm=adm, dur=dur, doseUnit=doseUnit,
                        timeUnit=timeUnit, concUnit=concUnit, R2ADJ=R2ADJ,
                        down=down, MW=MW, SS=SS, iAUC=iAUC,
                        Keystring=strHeader, excludeDelta=excludeDelta, slopeMode=slopeMode)
            # grp_dict.update(tRes)
            # Res.append(grp_dict)

            Res.append(tRes)

        # if i==0: print(f'({0}) ', tRes.keys())
        # print(f'({i}) ', tRes.values())
        # print(f'({i}) ', tRes)
        # print(f'({i}) ',tRes['UsedPoints'])
    Res = pd.DataFrame(Res)
    Res = pd.concat([IDs, Res], axis=1)

    Res['units'] = Res['units'].map(lambda x: [""] * nKey + x)

    NCAR_single = ['NSAMPLES', 'DOSE', 'R2', 'R2ADJ', 'CORRXY', 'LAMZNPT', 'LAMZ', 'b0', 'LAMZLL', 'LAMZUL',
                   'LAMZHL', 'SPAN', 'TLAG', 'TMAX', 'CMAX', 'CMAXD', 'TLST', 'CLST', 'CLSTP', 'AUCLST', 'AUCLSTD',
                   'AUCALL', 'AUCIFO', 'AUCIFOD', 'AUCPEO', 'VZFO', 'CLFO', 'AUCIFP', 'AUCIFPD', 'AUCPEP', 'VZFP',
                   'CLFP', 'AUMCLST', 'AUMCIFO', 'AUMCPEO', 'AUMCIFP', 'AUMCPEP', 'MRTLST', 'MRTIFO', 'MRTIFP']
    NCAR_multiple = ['NSAMPLES', 'DOSE', 'R2', 'R2ADJ', 'CORRXY', 'LAMZNPT', 'LAMZ', 'b0', 'LAMZLL', 'LAMZUL',
                     'LAMZHL', 'SPAN', 'TLAG', 'TMAX', 'CMAX', 'CMAXD', 'TLST', 'CLST', 'CLSTP', 'AUCLST',
                     'AUCLSTD', 'AUCALL', 'AUCIFO', 'AUCIFOD', 'AUCPEO', 'AUCIFP', 'AUCIFPD', 'AUCPEP', 'TMIN',
                     'CMIN', 'CTAU', 'CAVG', 'SWINGTAU', 'FLUCTP', 'FLUCTPTAU', 'CLSSF', 'MRTIVIFO', 'MRTIVIFP',
                     'VZF', 'ACCIDX', 'AUCTAU', 'AUCTAUD', 'AUCTAUPE', 'AUMCTAU']

    if ms_type == 'single':
        Res = Res[key + NCAR_single + ['units','UsedPoints']].copy()
    elif ms_type == 'multiple':
        Res = Res[key + NCAR_multiple + ['units','UsedPoints']].copy()
    Res = Res.loc[:, ~Res.columns.duplicated(keep='first')]

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

    TestCD = ["NSAMPLES", "SPAN", "b0", "CMAX", "CMIN", "CMAXD", "TMAX", "TMIN", "TLAG", "CLST",
              "CLSTP", "TLST", "LAMZHL", "LAMZ", "LAMZLL", "LAMZUL",
              "LAMZNPT", "CORRXY", "R2", "R2ADJ", "C0", "AUCLST", "AUCLSTD",
              "AUCALL", "AUCIFO", "AUCIFOD", "AUCIFP", "AUCIFPD",
              "AUCPEO", "AUCPEP", "AUCPBEO", "AUCPBEP", "AUMCLST",
              "AUMCIFO", "AUMCIFP", "AUMCPEO", "AUMCPEP", "MRTLST", "MRTIFO", "MRTIFP", "MRTIVLST",
              "MRTIVIFO", "MRTIVIFP", "MRTEVLST", "MRTEVIFO", "MRTEVIFP",
              "VZO", "VZP", "VZFO", "VZFP", "CLO", "CLP", "CLFO",
              "CLFP", "VSSO", "VSSP"]

    nTestCD = len(TestCD)
    Res = pd.DataFrame({"Unit": [""] * nTestCD, "Factor": [1] * nTestCD}, index=TestCD)

    for i in range(nTestCD):
        Code = TestCD[i]
        if Code in ["CMIN", "CMAX", "CLST", "CLSTP", "C0"]:
            Res.loc[Code, "Unit"] = concUnit
        if Code == "CMAXD":
            Res.loc[Code, "Unit"] = f"{concUnit}/{doseUnit}"
        if Code in ["TMIN","TMAX", "TLAG", "TLST", "LAMZHL", "LAMZLL", "LAMZUL", "MRTLST", "MRTIFO", "MRTIFP"
                    "MRTIVLST", "MRTIVIFO", "MRTIVIFP", "MRTEVLST",
                    "MRTEVIFO", "MRTEVIFP"]:
            Res.loc[Code, "Unit"] = timeUnit
        if Code == "LAMZ":
            Res.loc[Code, "Unit"] = f"/{timeUnit}"
        if Code in ["NSAMPLES", "b0", "LAMZNPT", "CORRXY", "R2", "R2ADJ", "SPAN"]:
            Res.loc[Code, "Unit"] = ""
        if Code in ["AUCLST", "AUCALL", "AUCIFO", "AUCIFP"]:
            Res.loc[Code, "Unit"] = f"{timeUnit}*{concUnit}"
        if Code in ["AUCIFOD", "AUCIFPD", "AUCLSTD"]:
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


def BestSlope(x, y, adm="Extravascular", TOL=1e-04, excludeDelta=1):
    # x, y, adm, TOL, excludeDelta = x1, y1, adm, 1e-04, excludeDelta

    result = {
        'R2': np.nan, 'R2ADJ': np.nan, 'LAMZNPT': 0, 'LAMZ': np.nan,
        'b0': np.nan, 'CORRXY': np.nan, 'LAMZLL': np.nan, 'LAMZUL': np.nan, 'CLSTP': np.nan
    }
    if excludeDelta < 0:
        raise ValueError("Option excludeDelta should be non-negative!")

    n = len(x)
    if n == 0 or n != len(y) or not np.issubdtype(x.dtype, np.number) or not np.issubdtype(y.dtype, np.number) or np.any(y < 0):
        result['LAMZNPT'] = 0
        return result

    if len(np.unique(y)) == 1:
        result['LAMZNPT'] = 0
        result['b0'] = np.unique(y)[0]
        return result

    # (Cmax 의 index 위치, Conc이 0이 아닌 끝나는 지점 index 위치) 찾기

    r0 = result.copy()
    loc_start = np.argmax(y) if adm.upper().strip() == "BOLUS" else np.argmax(y) + 1
    loc_last = np.max(np.where(y > 0)[0])

    if np.isnan(loc_start) or np.isnan(loc_last):
        result['LAMZNPT'] = 0
        return result

    if loc_last - loc_start < 2:
        r0['LAMZNPT'] = 0
    else:
        tmp_mat = np.full((loc_last - loc_start - 1, len(r0)), np.nan)
        res_columns = list(r0.keys())

        for i in range(loc_start, loc_last - 1):
            # i=10
            # i=11
            # slope, intercept, r_value, p_value, std_err = linregress(x[i:], np.log(y[i:loc_last + 1]))
            slope, intercept, r_value, p_value, std_err = linregress(x[i:loc_last+1], np.log(y[i:loc_last + 1]))
            n_reg = len(x[i:])

            tmp_mat[i - loc_start, :8] = [r_value ** 2, (1 - (1 - r_value ** 2) * (n_reg - 1) / (n_reg - 2)), loc_last - i + 1, -slope, intercept, r_value, x[i], x[loc_last]]

        tmp_mat = tmp_mat[np.isfinite(tmp_mat[:, 1]) & (tmp_mat[:, 2] > 2), :]

        if tmp_mat.shape[0] > 0:
            max_adj_rsq = np.max(tmp_mat[:, 1])
            oks = np.abs(max_adj_rsq - tmp_mat[:, 1]) < TOL
            n_max = np.max(tmp_mat[oks, 2])
            r0 = tmp_mat[oks & (tmp_mat[:, 2] == n_max), :][0]
            r0[8] = np.exp(r0[4] - r0[3] * np.max(x[np.isfinite(y)]))
            r0 = dict(zip(res_columns, list(r0)))
        else:
            r0['LAMZNPT'] = 0

    if excludeDelta < 1:
        x1 = x[:-1]
        y1 = y[:-1]
        r1 = result.copy()
        loc_start = np.argmax(y1) if adm.upper().strip() == "BOLUS" else np.argmax(y1) + 1
        loc_last = np.max(np.where(y1 > 0)[0])

        if loc_last - loc_start < 2:
            r1['LAMZNPT'] = 0
        else:
            tmp_mat = np.full((loc_last - loc_start - 1, len(r1)), np.nan)
            res_columns = list(r1.keys())

            for i in range(loc_start, loc_last - 1):
                # i=9
                slope, intercept, r_value, p_value, std_err = linregress(x1[i:loc_last], np.log(y1[i:loc_last]))
                n_reg = len(x1[i:loc_last])
                tmp_mat[i - loc_start, :8] = [r_value ** 2, (1 - (1 - r_value ** 2) * (n_reg - 1) / (n_reg - 2)),
                                              loc_last - i, -slope, intercept, r_value, x1[i], x1[loc_last - 1]]

            tmp_mat = tmp_mat[tmp_mat[:, 2] > 2, :]

            if tmp_mat.shape[0] > 0:
                max_adj_rsq = np.max(tmp_mat[:, 1])
                oks = np.abs(max_adj_rsq - tmp_mat[:, 1]) < TOL
                n_max = np.max(tmp_mat[oks, 2])
                r1 = tmp_mat[oks & (tmp_mat[:, 2] == n_max), :][0]
                r1[8] = np.exp(r1[4] - r1[3] * np.max(x[np.isfinite(y)]))
                r1 = dict(zip(res_columns, list(r1)))
            else:
                r1['LAMZNPT'] = 0

        if np.isnan(r1[1]):
            result = r0
        elif np.isnan(r0[1]):
            result = r1
        elif r1[1] - r0[1] > excludeDelta:
            result = r1
        else:
            result = r0
    else:
        result = r0

    # if type(result)==dict: result = result.values()

    # result = dict(zip(res_columns, list(result)))
    if result['LAMZNPT'] > 0:
        result['UsedPoints'] = list(
            range(np.where(x == result['LAMZLL'])[0][0], np.where(x == result['LAMZUL'])[0][0] + 1))
    else:
        result['UsedPoints'] = list()

    return result


def SnuhcptSlope(x, y, adm="Extravascular", TOL=1e-04, excludeDelta=1):
    # x, y, adm, TOL, excludeDelta = x1, y1, adm, 1e-04, excludeDelta
    """
    x = np.array([ 1.66666667,  2.66666667,  3.66666667,  4.66666667,  5.66666667,
        6.66666667,  7.66666667,  8.66666667, 10.66666667, 12.66666667,
       24.66666667, 47.93333333])
    y = np.array([  44.7,  247. ,  581. ,  890. , 1150. , 1140. , 1240. , 1330. ,
        958. ,  649. ,   77.1,   39.4])
    """

    result = {
        'R2': np.nan, 'R2ADJ': np.nan, 'LAMZNPT': 0, 'LAMZ': np.nan,
        'b0': np.nan, 'CORRXY': np.nan, 'LAMZLL': np.nan, 'LAMZUL': np.nan, 'CLSTP': np.nan
    }
    if excludeDelta < 0:
        raise ValueError("Option excludeDelta should be non-negative!")

    n = len(x)
    if n == 0 or n != len(y) or not np.issubdtype(x.dtype, np.number) or not np.issubdtype(y.dtype, np.number) or np.any(y < 0):
        result['LAMZNPT'] = 0
        return result

    if len(np.unique(y)) == 1:
        result['LAMZNPT'] = 0
        result['b0'] = np.unique(y)[0]
        return result

    # (Cmax 의 index 위치, Conc이 0이 아닌 끝나는 지점 index 위치) 찾기

    r0 = result.copy()
    loc_cmax = np.argmax(y)
    loc_start = np.argmax(y) if adm.upper().strip() == "BOLUS" else np.argmax(y) + 1
    loc_last = np.max(np.where(y > 0)[0])

    if np.isnan(loc_start) or np.isnan(loc_last):
        result['LAMZNPT'] = 0
        return result

    if loc_last - loc_cmax < 2:
        # Cmax 포함하여 총 2개 미만의 농도값만 존재
        r0['LAMZNPT'] = 0
    elif loc_last - loc_cmax == 2:
        # Cmax 포함하여 총 3개 농도값만 존재
        r0['LAMZNPT'] = 0
        tmp_mat = np.full((1, len(r0)), np.nan)

        slope, intercept, r_value, p_value, std_err = linregress(x[loc_cmax:loc_last + 1], np.log(y[loc_cmax:loc_last + 1]))
        n_reg = len(x[loc_cmax:])

        tmp_mat[0, :8] = [r_value ** 2, (1 - (1 - r_value ** 2) * (n_reg - 1) / (n_reg - 2)), loc_last - loc_cmax + 1, -slope, intercept, r_value, x[loc_cmax], x[loc_last]]
        tmp_mat[0, 8:] = [np.exp(intercept + slope * x[loc_last])]

        # R2ADJ 값이 존재하며, LAMZNPT(point 수) 가 3이상이어야 인정
        tmp_mat = tmp_mat[np.isfinite(tmp_mat[:, 1]) & (tmp_mat[:, 2] > 2), :]

        # [추후예외처리] R2ADJ 값이 <0 일때의 예외처리
        if (len(np.where(tmp_mat[:, 1] < 0)[0]) > 0) or (slope >= 0):
            # (terminal slope 가 양의 값을 갖거나 adjusted R2 수치가 undefined 또는 음수가 되는 등 타당성이 인정되는 경우 마지막 농도 point 에 한하여 제외할 수 있다.)
            raise ValueError(f"adjusted R2 수치가 undefined 또는 음수 / terminal slope : {slope}")

    elif loc_last - loc_cmax > 2:
        # Cmax 포함하지 않아도 3개 이상의 농도값 존재
        tmp_mat = np.full((loc_last - loc_start - 1, len(r0)), np.nan)
        res_columns = list(r0.keys())

        for i in range(loc_start, loc_last - 1):
            # i=8
            # i=9
            slope, intercept, r_value, p_value, std_err = linregress(x[i:loc_last+1], np.log(y[i:loc_last+1]))
            n_reg = len(x[i:])

            tmp_mat[i - loc_start, :8] = [r_value ** 2, (1 - (1 - r_value ** 2) * (n_reg - 1) / (n_reg - 2)), loc_last - i + 1, -slope, intercept, r_value, x[i], x[loc_last]]
            tmp_mat[i - loc_start, 8:] = [np.exp(intercept + slope * x[loc_last])]

        # R2ADJ 값이 존재하며, LAMZNPT(point 수) 가 3이상이어야 인정
        tmp_mat = tmp_mat[np.isfinite(tmp_mat[:, 1]) & (tmp_mat[:, 2] > 2), :]

        # [추후예외처리] R2ADJ 값이 <0 일때의 예외처리
        if (len(np.where(tmp_mat[:, 1] < 0)[0]) > 0) or (slope >= 0):
            # (terminal slope 가 양의 값을 갖거나 adjusted R2 수치가 undefined 또는 음수가 되는 등 타당성이 인정되는 경우 마지막 농도 point 에 한하여 제외할 수 있다.)
            raise ValueError(f"adjusted R2 수치가 undefined 또는 음수 / terminal slope : {slope}")

        if tmp_mat.shape[0] > 0:

            # final_rsq = np.nan
            prev_inx = np.nan
            prev_rsq = 0
            for inx, rsq_cand in enumerate(reversed(list(tmp_mat[:,1]))):
                rsq_cand_inx = len(tmp_mat)-inx-1
                rsq_delta = rsq_cand - prev_rsq
                if (rsq_delta < TOL):
                    # final_rsq = prev_rsq
                    final_inx = prev_inx
                    # print(prev_inx)
                    break
                elif (inx==len(tmp_mat)-1):
                    # final_rsq = rsq_cand
                    final_inx = rsq_cand_inx
                else:
                    prev_rsq = rsq_cand
                    prev_inx = rsq_cand_inx
                # print(f'{inx} / {prev_rsq} / {rsq_cand} / {final_rsq}')
            r0 = dict(zip(res_columns, list(tmp_mat[final_inx])))
        else:
            r0['LAMZNPT'] = 0

    else:
        # [추후예외처리] 그 외 다른 경우
        raise ValueError("그 외 다른 에러")


    if excludeDelta < 1:
        x1 = x[:-1]
        y1 = y[:-1]
        r1 = result.copy()
        loc_start = np.argmax(y1) if adm.upper().strip() == "BOLUS" else np.argmax(y1) + 1
        loc_last = np.max(np.where(y1 > 0)[0])

        if loc_last - loc_start < 2:
            r1['LAMZNPT'] = 0
        else:
            tmp_mat = np.full((loc_last - loc_start - 1, len(r1)), np.nan)
            res_columns = list(r1.keys())

            for i in range(loc_start, loc_last - 1):
                # i=9
                slope, intercept, r_value, p_value, std_err = linregress(x1[i:loc_last], np.log(y1[i:loc_last]))
                n_reg = len(x1[i:loc_last])
                tmp_mat[i - loc_start, :8] = [r_value ** 2, (1 - (1 - r_value ** 2) * (n_reg - 1) / (n_reg - 2)), loc_last - i, -slope, intercept, r_value, x1[i], x1[loc_last - 1]]

            tmp_mat = tmp_mat[tmp_mat[:, 2] > 2, :]

            if tmp_mat.shape[0] > 0:
                max_adj_rsq = np.max(tmp_mat[:, 1])
                oks = np.abs(max_adj_rsq - tmp_mat[:, 1]) < TOL
                n_max = np.max(tmp_mat[oks, 2])
                r1 = tmp_mat[oks & (tmp_mat[:, 2] == n_max), :][0]
                r1[8] = np.exp(r1[4] - r1[3] * np.max(x[np.isfinite(y)]))
                r1 = dict(zip(res_columns, list(r1)))
            else:
                r1['LAMZNPT'] = 0

        if np.isnan(r1[1]):
            result = r0
        elif np.isnan(r0[1]):
            result = r1
        elif r1[1] - r0[1] > excludeDelta:
            result = r1
        else:
            result = r0
    else:
        result = r0

    # if type(result)==dict: result = result.values()

    # result = dict(zip(res_columns, list(result)))
    if result['LAMZNPT'] > 0:
        result['UsedPoints'] = list(
            range(np.where(x == result['LAMZLL'])[0][0], np.where(x == result['LAMZUL'])[0][0] + 1))
    else:
        result['UsedPoints'] = list()

    return result


def DetSlope(x, y, SubTitle="", sel1=0, sel2=0):
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


def sNCA(x, y, dose=0, tau=np.nan ,adm="Extravascular", dur=0, doseUnit="mg", timeUnit="h", concUnit="ug/L", iAUC=None,
         down="Linear", R2ADJ=0.7, MW=0, SS=False, Keystring="", excludeDelta=1, slopeMode='BEST'):
    """
    x, y, adm, dur, doseUnit, timeUnit, concUnit = tData[colTime].values, tData[colConc].values, adm, dur, doseUnit, timeUnit, concUnit
    R2ADJ, down, MW, SS, iAUC, Keystring, excludeDelta = R2ADJ, down, MW, SS, iAUC, strHeader, excludeDelta
    dose = dose[0]
    slopeMode
    """

    """
    x = [0.        ,  0.91666667,  1.16666667,  1.66666667,  2.16666667,
         2.66666667,  3.16666667,  3.66666667,  4.66666667,  6.66666667, 8.66666667, 12.66666667, 24.66666667]
    y = [0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   1.23,   2.63,   6.35, 72.4 , 470.  , 268.  , 124.  ,  37.4]


    x=[0.        ,  0.91666667,  1.16666667,  1.66666667,  2.16666667,
       2.66666667,  3.16666667,  3.66666667,  4.66666667,  6.66666667,
       8.66666667, 12.66666667, 24.66666667, 48.55]
    y=[0.  ,   0.  ,   0.  ,   1.  ,   1.87,   2.47,   4.17,  27.7, 100.  , 147.  , 126.  , 173.  ,  80.1 ,  12.9]

    """

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
    RetNames1 = ["b0", "CMAX", "CMIN", "CMAXD", "TMAX", "TLAG", "CLST",
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

    # unique한 conc 값이 1개만있을때 (==Cmax, Cmin)

    if len(uY) == 1:
        Res["CMAX"] = uY[0]
        Res["CMIN"] = uY[0]
        if dose > 0:
            Res["CMAXD"] = uY[0] / dose
        Res["TMAX"] = x[np.where(y == uY)[0][0]]
        Res["TMIN"] = x[np.where(y == uY)[0][0]]

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

        for k in Res.keys():
            Res[k] *= Units.loc[k, 1]

        Res["units"] = list(Units.loc[RetNames1, 0]) + [Units.loc["AUCLST", 0]] * niAUC
        return Res

    # unique한 y값이 1개 이상일때

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

    # Slope 찾기 (Best Fit)
    if slopeMode=='SNUHCPT':
        tRes = SnuhcptSlope(x1, y1, adm, excludeDelta=excludeDelta)
    else:
        tRes = BestSlope(x1, y1, adm, excludeDelta=excludeDelta)

    # Slope 찾기 (Pick the slope)

    if R2ADJ > 0:
        if tRes["LAMZNPT"] < 2:
            tRes = DetSlope(x1, y1, Keystring)
        elif tRes["R2ADJ"] < R2ADJ:
            tRes = DetSlope(x1, y1, Keystring, sel1=np.where(x1 == tRes["LAMZLL"])[0], sel2=np.where(x1 == tRes["LAMZUL"])[0])

    # Slope 찾기 (Pick the slope)

    tRes["UsedPoints"] = list(tRes.get("UsedPoints", list()) + np.where(x == tRes["LAMZLL"])[0][0] - np.where(x1 == tRes["LAMZLL"])[0][0]) if not np.isnan(tRes["LAMZLL"]) else list()
    for key in ["R2", "R2ADJ", "LAMZNPT", "LAMZ", "b0", "CORRXY", "LAMZLL", "LAMZUL", "CLSTP"]:
        Res[key] = tRes[key]

    tab_auc = AUC(x3, y3, down)
    Res["NSAMPLES"] = len(y)
    Res["AUCLST"], Res["AUMCLST"] = tab_auc['AUC'][-1], tab_auc['AUMC'][-1]
    Res["AUCALL"] = AUC(x2, y2, down)['AUC'][-1]
    Res["LAMZHL"] = np.log(2) / Res["LAMZ"]
    Res["SPAN"] = (Res["LAMZUL"]-Res["LAMZLL"])/Res["LAMZHL"]
    Res["TMAX"] = x[np.argmax(y)]
    Res["CMAX"] = np.max(y)
    Res["TMIN"] = x[np.argmin(y)]
    Res["CMIN"] = np.min(y)
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




    if adm.strip().upper()=="INFUSION":
        infusion_time = np.nan               # 추후 input으로 추가 필요
        Res["MRTIFO"] -= infusion_time / 2
        Res["MRTIFP"] -= infusion_time / 2

    if not np.isnan(dose) and dose > 0:
        Res["CMAXD"] = Res["CMAX"] / dose
        Res['AUCLSTD'] = Res['AUCLST'] / dose
        Res["AUCIFOD"] = Res["AUCIFO"] / dose
        Res["AUCIFPD"] = Res["AUCIFP"] / dose

    if adm.strip().upper() == "BOLUS":
        Res["C0"] = C0
        # Res["AUCPBEO"] = tab_auc[1, 0] / Res["AUCIFO"] * 100
        # Res["AUCPBEP"] = tab_auc[1, 0] / Res["AUCIFP"] * 100
        Res["AUCPBEO"] = tab_auc['AUC'][-1] / Res["AUCIFO"] * 100
        Res["AUCPBEP"] = tab_auc['AUC'][-1] / Res["AUCIFP"] * 100
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

        Res["MRTLST"] = Res["MRTEVLST"]
        Res["MRTIFO"] = Res["MRTEVIFO"]
        Res["MRTIFP"] = Res["MRTEVIFP"]
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

        Res["MRTLST"] = Res["MRTIVLST"]
        Res["MRTIFO"] = Res["MRTIVIFO"]
        Res["MRTIFP"] = Res["MRTIVIFP"]

    if isinstance(iAUC, pd.DataFrame):
        niAUC = len(iAUC)
        if niAUC > 0:
            RetNames1 = list(set(RetNames1).union(iAUC["Name"]))
            for i in range(niAUC):
                if adm.strip().upper() == "BOLUS":
                    Res[iAUC.loc[i, "Name"]] = IntAUC(x2, y2, iAUC.loc[i, "Start"], iAUC.loc[i, "End"], Res, down=down)
                else:
                    Res[iAUC.loc[i, "Name"]] = IntAUC(x, y, iAUC.loc[i, "Start"], iAUC.loc[i, "End"], Res, down=down)
                Units = Units.append(Units.loc["AUCLST", :], ignore_index=True)
                Units.index = list(Units.index[:-1]) + [iAUC.loc[i, "Name"]]
    else:
        niAUC = 0

    for key in Res.keys():
        Res[key] *= Units.loc[key, 'Factor']
        # Units.loc[key]
    # len(RetNames1)
    # len(Units)
    Res["NSAMPLES"] = Res["NSAMPLES"].astype(int)
    Res["units"] = Units.loc[RetNames1, 'Unit'].values.tolist() + [Units.loc["AUCLST", 'Unit']] * niAUC
    Res["UsedPoints"] = tRes.get("UsedPoints", [])
    return Res
