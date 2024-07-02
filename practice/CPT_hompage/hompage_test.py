import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 샘플 데이터 생성
data = {
    'Year': [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    '임상': [1000, 1200, 1100, 900, 800, 950, 1050, 1500],
    '진검': [1500, 1400, 1300, 1100, 1000, 1150, 1250, 1700],
    '약제': [2000, 1800, 1600, 1400, 1300, 1350, 1450, 2100]
}

df = pd.DataFrame(data)

# 데이터프레임을 길게 변환
df_melted = df.melt(id_vars='Year', var_name='Category', value_name='Count')

# 그래프 그리기
plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")

# 누적 막대 그래프
sns.barplot(data=df_melted, x='Year', y='Count', hue='Category')

# 제목 및 레이블 설정
plt.title('연도별 TDM 건수', fontsize=16)
plt.xlabel('')
plt.ylabel('')
plt.legend(title='', loc='upper right', labels=['임상', '진검', '약제'])
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.ylim(0, 2500)

# 그래프 표시
plt.show()
