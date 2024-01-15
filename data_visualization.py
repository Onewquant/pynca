import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

result_type = 'Phoenix'
result_type = 'R'
drug_list = ['Sitagliptin', 'Empagliflozin', 'Metformin']
input_file_dir_path = 'C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK분석'
result_file_dir_path = 'C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK분석/Figures'

drug_prep_df_dict = dict()
for drug in drug_list:
    result_file_path = f"{input_file_dir_path}/" + f"CKD379_ConcPrep_{drug}({result_type}).csv"
    drug_prep_df_dict[drug] = pd.read_csv(result_file_path)
    # drug_prep_df_dict[drug]['Subject'] = drug_prep_df_dict[drug].apply(lambda row:f'{row["ID"]}|{row["FEEDING"]}',axis=1)

gdf = drug_prep_df_dict['Sitagliptin']
gdf = drug_prep_df_dict['Empagliflozin']
gdf = drug_prep_df_dict['Metformin']


# fig, axes = plt.subplots(nrows=2,ncols=2, figsize=(20, 40))
# sns.relplot(data=gdf[gdf['ID'].isin(['A001'])],x='ATIME',y='CONC', ax=axes)

############################

# max(gdf['CONC'])
# max(gdf['ATIME'])
# g_palette = 'Set2'
g_palette = 'Dark2'
g = sns.relplot(data=gdf, x='NTIME',y='CONC', marker='o', markersize=7, markeredgecolor='white', markeredgewidth=1, kind='line', linewidth=1.5, linestyle='-', errorbar="ci", estimator='mean')

for drug in drug_list:

    g_palette = 'Dark2'
    sns.set_style("whitegrid",{'grid.linestyle':':',
                 })

    gdf = drug_prep_df_dict[drug]
    # drug = gdf['DRUG'].iloc[0]
    # sid = 'A001'
    for sid in gdf['ID'].unique():

        g = sns.relplot(data=gdf[gdf['ID'].isin([sid])], hue='FEEDING', hue_order=['FASTING', 'FED'], x='ATIME',y='CONC', palette=g_palette, marker='o', markersize=7, markeredgecolor='white', markeredgewidth=1, kind='line', linewidth=1.5, linestyle='--')

        g.fig.set_size_inches(14,10)

        # g.set_axis_labels('Time (hr)', 'Concentration (mg/L)')
        # sns.move_legend(g, 'upper right', frameon=True)
        # g.fig.subplots_adjust(top=0.85)
        sns.move_legend(g, 'center right', title=None, frameon=False, fontsize=15)
        # sns.move_legend(g, 'upper center', ncol=2, title=None, frameon=False, fontsize=15)
        # g.fig.suptitle("A001", fontsize=20, fontweight='bold')

        plt.tight_layout(pad=2.5)
        plt.title(sid, fontsize=20)
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
        if not os.path.exists(f"{result_file_dir_path}/{drug}"): os.mkdir(f"{result_file_dir_path}/{drug}")

        plt.savefig(f"{result_file_dir_path}/{drug}/individual_{drug}_{sid}.png", dpi=300)
        plt.cla()
        plt.clf()
        plt.close()
############################


# g_palette = 'Set2'
# g_palette = ['']
# sns.set(rc= {'figure.figsize': (30,60),
#              'axes.labelsize' : 12,
#              })
#
# sns.set_style("whitegrid",{'grid.linestyle':':',
#              })

# g = sns.relplot(data=gdf[gdf['ID'].isin(['A001','A002'])], hue='FEEDING', hue_order=['FASTING', 'FED'], col='FEEDING',row='ID',x='ATIME',y='CONC', palette='Set2', marker='o', markersize=7, markeredgecolor='white', markeredgewidth=1, kind='line', linewidth=1, linestyle='--')
# g = sns.relplot(data=gdf[gdf['ID'].isin(['A001','A002'])], hue='FEEDING', hue_order=['FASTING', 'FED'], row='ID', col='FEEDING',x='ATIME',y='CONC', palette=g_palette, marker='o', markersize=7, markeredgecolor='white', markeredgewidth=1, kind='line', linewidth=1, linestyle='--', legend=False)

# g.axes[0,0].get_xticks()
# g.axes[0,0].set_xticklabels(list(g.axes[0,0].get_xticks()))
# g.axes[1,0].set_xticklabels(list(g.axes[0,0].get_xticks()))
# g.fig.suptitle("Individual Time to Concentration Graph",
#                fontsize='x-large',
#                fontweight='bold')

# g.fig.subplots_adjust(top=0.85,wspace=0.3,hspace=0.3)
# g.set_axis_labels('Time (hr)', 'Concentration (mg/L)')
# g.set(xlim=(0,55), ylim=(0,1200))

# fig, axes = plt.subplots(nrows=2,ncols=2, figsize=(20, 15))
# sns.relplot(ax=axes[0],data=gdf[gdf['ID'].isin(['A001'])], x='ATIME',y='CONC', hue='FEEDING', row='ID', palette='Set2', marker='o', markersize=7, markeredgecolor='white', markeredgewidth=2, kind='line', linewidth=2)

# fig, axes = plt.subplots(figsize=(20, 15))

# plt.legend(fontsize=15)
# plt.xlabel('Time (hr)', fontsize=15)
# plt.ylabel('Concentration (mg/L)', fontsize=15)
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)
# plt.show()
