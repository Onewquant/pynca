import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Excel file
file_dir = 'C:/Users/ilma0/PycharmProjects/pynca/resource/piechart'
file_path = f'{file_dir}/TDM.xlsx'
chart_path = f'{file_dir}/TDM.png'
excel_data = pd.ExcelFile(file_path)

# Load the data from the first sheet
df = pd.read_excel(excel_data, sheet_name=excel_data.sheet_names[0])

# Set the style of the visualization
sns.set(style="whitegrid")

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

plt.tight_layout(pad=3.5)

# plt.title('TDM Cases Over Years', fontsize=20)
plt.legend(title='', loc='upper right', labels=['SNUBH'], fontsize='large', bbox_to_anchor=(1, 1),
           frameon=False, framealpha=0.9, edgecolor='black', facecolor='lightgrey',
           title_fontsize='13', ncol=1, borderpad=1, labelspacing=0.5, handlelength=2,
           handletextpad=0.5)
plt.xlabel('Year', fontsize=20, labelpad=8)
plt.ylabel(None, fontsize=20, labelpad=8)

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.ylim(0, int(df['TDM'].max()*1.2/100)*100)

# Display the plot
plt.savefig(chart_path)
plt.close()

