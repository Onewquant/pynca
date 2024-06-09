import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd
import seaborn as sns
import matplotlib.font_manager as fm

# Seaborn 팔레트 생성
palette = sns.color_palette('Blues_d')
# palette = ListedColormap(["#87CEEB", "#4682B4", "#4169E1", "#0000CD","#00008B"])

# Function to create pie charts for each sheet
def create_pie_charts(excel_data, output_dir='/mnt/data/'):

    # Pretendard 폰트 파일 경로 설정
    font_path = 'C:/Windows/Fonts/Pretendard-Regular.ttf'  # Pretendard-Regular.ttf 파일 경로를 입력하세요
    fontprop = fm.FontProperties(fname=font_path)


    sheet_names = {'Drugs':palette,}
    # 'sequential5blau'
    # 'sequential5petrol'
    # sheet='Sheet3'
    chart_paths = []
    for sheet, color_p in sheet_names.items():
        # Load data from the current sheet
        df = pd.read_excel(excel_data, sheet_name=sheet)

        # Assuming the first column is the category and the second column is the value
        categories = df.iloc[:, 0]
        values = df.iloc[:, 1]

        # Create a pie chart
        # plt.figure(figsize=(10, 10))

        # 파이 차트 그리기
        fig, ax = plt.subplots(figsize=(10, 10))
        wedges, texts, autotexts = ax.pie(values, labels=categories, colors=palette, autopct='%1.1f%%', startangle=140)

        # # Equal aspect ratio ensures that pie is drawn as a circle.
        # ax.axis('equal')

        # 파이 차트 안의 텍스트 폰트를 변경
        for text in texts + autotexts:
            text.set_fontproperties(fontprop)

        # plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140, colors=nation4.colors)
        # plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140, colors=palette)
        # plt.title(f'Pie Chart for {sheet} Sheet')

        # Save the pie chart as an image file
        chart_path = f'{output_dir}/TDM_{sheet}.png'
        plt.savefig(chart_path, bbox_inches='tight', dpi=300)
        plt.close()

        chart_paths.append(chart_path)

    return chart_paths


# Create pie charts for each sheet
project_dir = 'C:/Users/ilma0/PycharmProjects/pynca/resource/piechart'
excel_data=f'{project_dir}/TDM_drugs.xlsx'

chart_paths = create_pie_charts(excel_data=excel_data, output_dir=project_dir)
chart_paths
