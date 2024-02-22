import sys, os
sys.path.append(os.path.dirname(os.path.abspath("__file__")))

from project_tools import *

result_type = 'Phoenix'
result_type = 'R'
drug_list = ['Sitagliptin', 'Empagliflozin', 'Metformin']
input_file_dir_path = 'C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK분석'
result_file_dir_path = 'C:/Users/ilma0/PycharmProjects/pynca/resource/CKD379-FDI/PK분석/Figures'

drug_prep_df_dict = load_data_dict(drug_list=drug_list, filename_format=f"CKD379_ConcPrep_[drug]({result_type}).csv", input_file_dir_path=input_file_dir_path)

############################

# gdf = drug_prep_df_dict['Sitagliptin']
# gdf = drug_prep_df_dict['Empagliflozin']
# gdf = drug_prep_df_dict['Metformin']
# drug = 'Metformin'
# drug='Sitagliptin'
# sid_list = ['A001']
hue = 'FEEDING'
hue_order = ['FASTED','FED']
estimator=np.mean
# errorbar=("sd",1)
# err_style='bars'
# yscale = 'log'
# yscale = 'linear'

for yscale in ['linear','log']:
    for drug in drug_list:

        gdf = drug_prep_df_dict[drug]

        ## Population

        time_to_conc_graph_ckd(gdf=gdf, sid_list=list(gdf['ID'].unique()), drug=drug, hue=hue, result_file_dir_path=result_file_dir_path, hue_order=hue_order, estimator=estimator, yscale=yscale)

        plt.cla()
        plt.clf()
        plt.close()

        ## Individual

        for sid in gdf['ID'].unique():

            time_to_conc_graph_ckd(gdf=gdf, sid_list=[sid,], drug=drug, hue=hue, result_file_dir_path=result_file_dir_path, hue_order=hue_order, estimator=estimator, yscale=yscale)

            plt.cla()
            plt.clf()
            plt.close()
############################

# fig, axes = plt.subplots(nrows=2,ncols=2, figsize=(20, 40))
# sns.relplot(data=gdf[gdf['ID'].isin(['A001'])],x='ATIME',y='CONC', ax=axes)


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
