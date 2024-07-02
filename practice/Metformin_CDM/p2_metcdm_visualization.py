import sys, os
sys.path.append(os.path.dirname(os.path.abspath("__file__")))

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

output_mode = 'Paper'
output_mode = 'Poster_horizontal'
output_mode = 'Poster_vertical'

group_name = 'SNUH'
group_name = 'SNUBH'

outcome_name = 'HbA1c_delta'

input_dir = '/resource/MET_CDM'
df = pd.read_csv(f"{input_dir}/{group_name}.csv")
gdf = df[['pt_type','HbA1C_start_value','HbA1C_delta','HbA1C_pct_delta']].copy()
# gdf['pt_type_new'] = gdf['pt_type'].map({'HIPT': 'Target Cohort', 'NMPT': 'Control Cohort'})
gdf['pt_type_new'] = gdf['pt_type'].map({'HIPT': 'Target', 'NMPT': 'Control'})
# gdf = gdf[['pt_type_new','HbA1C_pct_delta']].copy()
gdf = gdf[['pt_type_new','HbA1C_delta']].copy()
gdf.columns = ['pt_type_new',outcome_name]

g_palette='Dark2'
g_palette_colors = sns.color_palette('Dark2')
sns.set_style("whitegrid", {'grid.linestyle': ':',
                                })

# gdf.iloc[:50].to_csv(f'{input_dir}/example_data.csv', index=False)
#
# gdf['HbA1C_delta'].max()
# gdf['HbA1C_delta'].min()

# SNUH : (-8.5, 4.6)
# SNUBH : (-6.0, 4.2)

# Seaborn boxplot 생성
# plt.figure(figsize=(10, 10))
# sns.boxplot(x='pt_type_new', y='HbA1C_pct_delta', data=gdf, order=["Target Cohort", "Control Cohort"], palette={'Target Cohort': 'darkgrey', 'Control Cohort': 'white'})
if output_mode == 'Poster_horizontal':
    plt.figure(figsize=(25, 10))
    g = sns.boxplot(x=outcome_name, y='pt_type_new', data=gdf, order=["Target", "Control"], palette={'Target': g_palette_colors[1], 'Control': g_palette_colors[0]})
    plt.xlabel('HbA1C Change (%)', fontsize=30)
    plt.ylabel('', fontsize=18, labelpad=20)

    # plt.xlim(-55, 71)
    # plt.xlim(-71, 71)
    plt.xlim(-9, 5)

    # y=0에 대한 대시 스타일 수평선 추가
    plt.axvline(0, color='black', linestyle='--')

    # 얇은 대시 스타일의 수평 그리드 추가
    plt.grid(axis='x', linestyle='--', linewidth=0.3)

    # xtick과 ytick의 글자 폰트 사이즈를 18로 설정
    # plt.xticks(fontsize=18)
    # plt.yticks(fontsize=18)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
else:
    plt.figure(figsize=(15, 10))
    g = sns.boxplot(x='pt_type_new', y=outcome_name, data=gdf, order=["Target", "Control"], palette={'Target': g_palette_colors[1], 'Control': g_palette_colors[0]})

    # x, y축 라벨 및 범위 설정
    # plt.xlabel(group_name, fontsize=18, labelpad=5)
    # plt.ylabel('HbA1C % Change (%)', fontsize=18)
    plt.xlabel('', fontsize=18, labelpad=5)
    plt.ylabel('HbA1C Change (%)', fontsize=30)
    # plt.ylim(-75, 75)
    # plt.ylim(-52, 71)
    plt.ylim(-9, 5)

    # y=0에 대한 대시 스타일 수평선 추가
    plt.axhline(0, color='black', linestyle='--')

    # 얇은 대시 스타일의 수평 그리드 추가
    plt.grid(axis='y', linestyle='--', linewidth=0.3)


    # xtick과 ytick의 글자 폰트 사이즈를 18로 설정
    # plt.xticks(fontsize=18)
    # plt.yticks(fontsize=18)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

# tight_layout
plt.tight_layout(pad=3.5)

# x축과 y축 선의 두께 설정
g.spines['top'].set_linewidth(2)
g.spines['bottom'].set_linewidth(2)
g.spines['left'].set_linewidth(2)
g.spines['right'].set_linewidth(2)

# 그래프 표시 (제목 생략)
# plt.show()

# plt.savefig(f"{input_dir}/{group_name}.png", dpi=600)
plt.savefig(f"{input_dir}/{group_name}_{output_mode}.png", dpi=600)
plt.cla()
plt.clf()
plt.close()


"""
from PIL import Image

# 이미지 파일 로드
image1 = Image.open('/mnt/data/SNUH.png')
image2 = Image.open('/mnt/data/SNUBH.png')

# 이미지를 가로로 나란히 배치하기 위해 각 이미지의 사이즈 확인
width1, height1 = image1.size
width2, height2 = image2.size

# 새 이미지의 캔버스 크기를 두 이미지의 가로 사이즈의 합과 세로 사이즈 중 더 큰 값으로 설정
total_width = width1 + width2
max_height = max(height1, height2)

# 새로운 이미지 캔버스 생성
new_image = Image.new('RGB', (total_width, max_height), (255, 255, 255))

# 새 이미지 캔버스에 이미지들을 붙임
new_image.paste(image1, (0, 0))
new_image.paste(image2, (width1, 0))

# 새 이미지 저장
new_image_path = '/mnt/data/combined_image.png'
new_image.save(new_image_path)

# 새 이미지 경로 반환
new_image_path
"""
# gdf[gdf['pt_type']=='HIPT']['HbA1C_delta'].median()
#
# gdf[gdf['pt_type']=='NMPT']['HbA1C_delta'].median()
#
# gdf[gdf['pt_type']=='HIPT']['HbA1C_pct_delta'].median()
#
# gdf[gdf['pt_type']=='NMPT']['HbA1C_pct_delta'].median()

# gdf['HbA1C_pct_delta'].min()
#
# gdf['HbA1C_pct_delta'].max()