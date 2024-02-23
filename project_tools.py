import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

