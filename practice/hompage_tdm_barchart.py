import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Load the Excel file
file_dir = 'C:/Users/ilma0/PycharmProjects/pynca/resource/piechart'
file_path = f'{file_dir}/TDM_barchart.xlsx'
chart_path = f'{file_dir}/TDM_barchart.png'
excel_data = pd.ExcelFile(file_path)

# Load the data from the first sheet
df = pd.read_excel(excel_data, sheet_name=excel_data.sheet_names[0])

# Set the style of the visualization
sns.set(style="whitegrid")
# font_path = 'C:/Users/ilma0/PycharmProjects/pynca/resource/piechart/Pretendard-1.3.9/public/variable/PretendardVariable.ttf' # 예시 경로
# fontprop = fm.FontProperties(fname=font_path)
# plt.rc('font', family=fontprop.get_name())

# font_path = 'C:/Windows/Fonts/Pretendard-Regular.ttf'  # Pretendard-Regular.ttf 파일 경로를 입력하세요
font_path = 'C:/Windows/Fonts/Pretendard-Bold.ttf'  # Pretendard-Regular.ttf 파일 경로를 입력하세요
fm.fontManager.addfont(font_path)
fontprop = fm.FontProperties(fname=font_path)
# plt.rcParams['font.family'] = 'NanumGothic'
#
for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
   if 'Pretendard' in font:
       print(font)
#
# # Pretendard 폰트 파일 경로 설정
# font_path = 'C:/Windows/Fonts/Pretendard-Regular.ttf'  # Pretendard-Regular.ttf 파일 경로를 입력하세요
#
# # 폰트를 설정합니다.
# fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()

# plt.rcParams['font.family'] = 'Pretendard'
# font_list = [font.name for font in fm.fontManager.ttflist if font.name[0]=='P']
# font_list
# 팔레트 생성 및 역순 적용
palette = sns.color_palette('Blues_d', n_colors=len(df['Year']))
reversed_palette = list(reversed(palette))

# Create a bar plot
plt.figure(figsize=(20, 10))
sns.barplot(x='Year', y='TDM', data=df, palette=reversed_palette, width=0.5)
# sns.barplot(x='Year', y='TDM', data=df, palette='Blues_d', width=0.5)
# sns.barplot(x='Year', y='TDM', data=df, palette='Blues', width=0.5)
# sns.barplot(x='Year', y='TDM', data=df, color='deepskyblue', width=0.5)

# Add title and labels



plt.title('연도별 TDM 건수', fontsize=30, pad=30, loc='left', fontweight='bold')
# plt.legend(title='', loc='upper right', labels=['SNUBH'], fontsize='large', bbox_to_anchor=(1, 1),
#            frameon=False, framealpha=0.9, edgecolor='black', facecolor='lightgrey',
#            title_fontsize='13', ncol=1, borderpad=1, labelspacing=0.5, handlelength=2,
#            handletextpad=0.5)

plt.tight_layout(pad=3.5)

plt.xlabel('Year', fontsize=20, labelpad=8)
plt.ylabel(None, fontsize=20, labelpad=8)

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylim(0, int(df['TDM'].max()*1.2/100)*100)

# 배경을 투명하게
fig = plt.gcf()
fig.patch.set_alpha(0.0)

# Display the plot
plt.savefig(chart_path)
plt.close()

