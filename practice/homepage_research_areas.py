import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 예제 데이터 프레임 생성

df = pd.read_csv('C:/Users/ilma0/PycharmProjects/pynca/resource/piechart/ResearchAreas_PKPD.csv')
# new_df = pd.DataFrame(list(df['NTIME'].unique()), columns=['time'])
# for inx, frag in df.groupby(by='ID'):
#     new_df[''] frag[['NTIME','CONC']]
#
# np.random.seed(42)
# time_points = list(range(11))
# data = {'time': time_points}
# for i in range(10):
#     data[f'concentration_{i}'] = np.random.normal(loc=5, scale=2, size=11).tolist()
df = df[df['ID'].map(lambda x:x[0])=='A']
df['time']=df['NTIME'].copy()
df['concentration']=df['CONC'].copy()/15
df['subject']=df['ID'].copy()
df_long = df[['subject', 'time', 'concentration']].copy()
time_points = list(df['time'].unique())
# df = pd.DataFrame(data)

# 데이터 프레임을 long 형식으로 변환
# df_long = pd.melt(df, id_vars=['time'], var_name='subject', value_name='concentration')

# Seaborn 스타일 설정
sns.set(style="whitegrid")
# sns.set(style="white")

# 그래프 그리기
plt.figure(figsize=(15, 13))
lineplot = sns.lineplot(x='time', y='concentration', data=df_long, hue='subject',
                        palette=['grey']*len(df['subject'].unique()), legend=False, alpha=0.6)

# 평균 값 계산 및 추가
df_mean = list(df[['time','concentration']].groupby(by='time').mean()['concentration'])
plt.plot(time_points, df_mean, color='darkred', marker='o', label='Population Concentration')

# 그래프 제목 및 레이블 설정
# plt.title('Individual and Mean Time to Concentration Curves', fontsize=20, pad=8)
plt.xlabel('Time (hours)', fontsize=20, labelpad=8)
plt.ylabel('Concentration (mg/L)', fontsize=20, labelpad=8)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(frameon=False, fontsize=20)

# 그리드를 점선으로 설정
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.tight_layout(pad=3.5)

# 그래프 보이기
# plt.show()

plt.savefig('C:/Users/ilma0/PycharmProjects/pynca/resource/piechart/ResearchAreas_PKPD.png', bbox_inches='tight', dpi=300)