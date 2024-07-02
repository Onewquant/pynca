import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터프레임 생성
file_dir = '/resource/piechart'
file_path = f'{file_dir}/Consultation_barchart.xlsx'
chart_path = f'{file_dir}/Consultation_barchart.png'
excel_data = pd.ExcelFile(file_path)

# Load the data from the first sheet
df = pd.read_excel(excel_data, sheet_name=excel_data.sheet_names[0])

# Seaborn 스타일 설정
sns.set(style="white")

# 플롯을 위한 Figure 생성
plt.figure(figsize=(16, 9))

# 각 Drug에 대해 누적 데이터를 위해 DataFrame을 준비
df['Busulfan_bottom'] = 0
df['Others_bottom'] = df['Busulfan']

# Busulfan 막대 그래프 그리기
sns.barplot(x='Year', y='Busulfan', data=df, color='steelblue', label='Busulfan', width=0.25)

# Others 막대 그래프를 Busulfan 위에 누적하여 그리기
sns.barplot(x='Year', y='Others', data=df, bottom=df['Others_bottom'], color='skyblue', label='Others', width=0.25)

# 연도별 총합을 계산하고 그래프에 표시
df['Total'] = df['Busulfan'] + df['Others']
for index, row in df.iterrows():
    plt.text(row['Year']-2021, row['Total'] + 1, f'{int(row["Total"])}', color='black', ha="center")

# 그래프 제목 및 레이블 설정
# plt.title('Yearly Count of Busulfan and Others', fontsize=16)
plt.xlabel('Year', fontsize=16, labelpad=8)
plt.ylabel('Count', fontsize=16, labelpad=8)
plt.ylim(0, int(df['Total'].max() * 1.2) )

# 범례 설정
plt.legend(title='Drug', frameon=False, loc='best')
plt.grid(True, which='both', linestyle='--', linewidth=0.5, axis='y')

plt.tight_layout(pad=3.5)

# 배경을 투명하게
fig = plt.gcf()
fig.patch.set_alpha(0.0)

# 그래프 보이기
plt.savefig(chart_path, bbox_inches='tight', dpi=300)
plt.close()