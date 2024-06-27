import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


outcome_name='HbA1c_delta'

# 데이터 파일 로드
resource_dir = 'C:/Users/ilma0/PycharmProjects/pynca/resource/MET_CDM'

snuh_df = pd.read_csv(f'{resource_dir}/SNUH.csv')[['pt_type','HbA1C_start_value','HbA1C_delta','HbA1C_pct_delta']].copy()
snubh_df = pd.read_csv(f'{resource_dir}/SNUBH.csv')[['pt_type','HbA1C_start_value','HbA1C_delta','HbA1C_pct_delta']].copy()
snuh_df['pt_type_new'] = snuh_df['pt_type'].map({'HIPT': 'Case', 'NMPT': 'Control'})
snubh_df['pt_type_new'] = snubh_df['pt_type'].map({'HIPT': 'Case', 'NMPT': 'Control'})
snuh_df = snuh_df[['pt_type_new','HbA1C_delta']].copy()
snubh_df = snubh_df[['pt_type_new','HbA1C_delta']].copy()
snuh_df.columns = ['pt_type_new',outcome_name]
snubh_df.columns = ['pt_type_new',outcome_name]

# 시각화 시작
# sns.set(style="whitegrid")
g_palette='Dark2'
g_palette_colors = sns.color_palette('Dark2')
sns.set_style("whitegrid", {'grid.linestyle': ':',
                                })

fig, axes = plt.subplots(1, 2, sharey=True, figsize=(7, 7))

# SNUH 데이터 시각화
sns.boxplot(x='pt_type_new', y=outcome_name, data=snuh_df, ax=axes[0], order=["Case", "Control"], palette={'Case': g_palette_colors[1], 'Control': g_palette_colors[0]})
axes[0].set_title('(A) SNUH',fontsize=13)
axes[0].axhline(0, color='black', linestyle='--')
axes[0].tick_params(axis='x', labelsize=13)
axes[0].tick_params(axis='y', labelsize=13)


# SNUBH 데이터 시각화
sns.boxplot(x='pt_type_new', y=outcome_name, data=snubh_df, ax=axes[1], order=["Case", "Control"], palette={'Case': g_palette_colors[1], 'Control': g_palette_colors[0]})
axes[1].set_title('(B) SNUBH',fontsize=13)
axes[1].axhline(0, color='black', linestyle='--')
axes[1].tick_params(axis='x', labelsize=13)

# 공통 y축 레이블 설정
axes[0].set_ylabel('HbA1c change (%)', fontsize=13, labelpad=8)
axes[1].set_ylabel(None)
axes[0].set_xlabel(None)
axes[1].set_xlabel(None)

# plt.xlabel(None)
# plt.ylabel('', fontsize=18, labelpad=20)

# plt.xlim(-55, 71)
# plt.xlim(-71, 71)
plt.ylim(-9, 5)

plt.tight_layout(pad=3.5)
# plt.show()

plt.savefig(f"{resource_dir}/Integrated_Efficacy({outcome_name}).png", dpi=600)
plt.cla()
plt.clf()
plt.close()