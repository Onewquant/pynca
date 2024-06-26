import pandas as pd
import numpy as np
from pymare import MetaAnalysis

# 데이터 로드
file_path = '/mnt/data/meta_test.csv'
data = pd.read_csv(file_path)

# 각 그룹 및 병원별 평균 및 표준편차 계산
stats_summary = data.groupby(['pt_type', 'hospital']).agg(
    mean_HbA1C_delta=('HbA1C_delta', 'mean'),
    std_HbA1C_delta=('HbA1C_delta', 'std'),
    count=('HbA1C_delta', 'size')
).reset_index()

import ace_tools as tools; tools.display_dataframe_to_user(name="Summary Statistics", dataframe=stats_summary)

# 메타분석을 위한 데이터 준비
meta_data = []
for _, row in stats_summary.iterrows():
    effect_size = row['mean_HbA1C_delta']
    variance = (row['std_HbA1C_delta'] ** 2) / row['count']
    meta_data.append([effect_size, variance])

# numpy 배열로 변환
meta_data = np.array(meta_data)

# 메타분석 수행
meta_analysis = MetaAnalysis(effect_sizes=meta_data[:, 0], variances=meta_data[:, 1])
random_effects_result = meta_analysis.fit(random_effects=True)

# 결과 출력
print("Random Effects Meta-Analysis Results")
print(random_effects_result.summary())
