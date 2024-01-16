import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gmean

def time_to_conc_graph_ckd(gdf, sid_list, drug, result_file_dir_path, file_format='png', dpi=300, estimator=np.mean, errorbar=("sd",2), err_style='band'):

    g_palette = 'Dark2'
    sns.set_style("whitegrid", {'grid.linestyle': ':',
                                })

    mode = 'Individual' if len(sid_list)==1 else 'Population'
    if mode=='Individual':
        title_str = sid_list[0]
        last_tag = '('+sid_list[0]+')'
        time_col = 'ATIME'
    else:
        if errorbar[0]=='sd':
            if errorbar[1]==1: errorbar_str = f' ({errorbar[0].upper()})'
            else: errorbar_str = f' ({errorbar[1]} {errorbar[0].upper()})'
        elif errorbar[0]=='ci':
            errorbar_str = f' ({errorbar[1]}% {errorbar[0].upper()})'
        else:
            errorbar_str = ''
        title_str = f'Sample Mean{errorbar_str}'
        last_tag = 'sample'+str(tuple(sid_list)).replace(",)",")").replace("'","")
        time_col = 'NTIME'
    filename = f'{mode}_{drug}_{last_tag}'

    g = sns.relplot(data=gdf[gdf['ID'].isin(sid_list)], hue='FEEDING', hue_order=['FASTING', 'FED'], x=time_col,y='CONC', palette=g_palette, marker='o', markersize=7, markeredgecolor='white', markeredgewidth=1, kind='line', linewidth=1.5, linestyle='--', errorbar=errorbar, estimator=estimator, err_style=err_style)
    # g.ax.errorbar(x)
    g.fig.set_size_inches(14,10)

    # g.set_axis_labels('Time (hr)', 'Concentration (mg/L)')
    # sns.move_legend(g, 'upper right', frameon=True)
    # g.fig.subplots_adjust(top=0.85)
    sns.move_legend(g, 'center right', title=None, frameon=False, fontsize=15)
    # sns.move_legend(g, 'upper center', ncol=2, title=None, frameon=False, fontsize=15)
    # g.fig.suptitle("A001", fontsize=20, fontweight='bold')
    plt.title(title_str, fontsize=20)
    plt.tight_layout(pad=2.5)

    plt.xlabel('Time (h)', fontsize=15)
    plt.ylabel(f'{drug} plasma concentration (mg/L)', fontsize=15)

    plt.xticks(np.arange(-5,55, step=5), fontsize=15)
    plt.xlim(-1,55)

    if drug=='Metformin':
        plt.yticks(np.linspace(0, 2500, 11, endpoint=True), fontsize=15)
        plt.ylim(-50, 2500)
    else:
        plt.yticks(np.linspace(0, 650, 11, endpoint=True), fontsize=15)
        plt.ylim(-10,650)

    if not os.path.exists(f"{result_file_dir_path}"): os.mkdir(f"{result_file_dir_path}")
    if not os.path.exists(f"{result_file_dir_path}/{mode}"): os.mkdir(f"{result_file_dir_path}/{mode}")
    if not os.path.exists(f"{result_file_dir_path}/{mode}/{drug}"): os.mkdir(f"{result_file_dir_path}/{mode}/{drug}")
    plt.savefig(f"{result_file_dir_path}/{mode}/{drug}/{filename}.{file_format}", dpi=dpi)

