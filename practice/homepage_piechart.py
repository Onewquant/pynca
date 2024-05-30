import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import pandas as pd

nation4 = ListedColormap(["#87CEEB", "#4682B4", "#4169E1", "#0000CD","#00008B"])

# Function to create pie charts for each sheet
def create_pie_charts(excel_data, output_dir='/mnt/data/'):
    sheet_names = {'Sheet0':nation4,'Sheet1':nation4,'Sheet2':nation4}
    # 'sequential5blau'
    # 'sequential5petrol'
    chart_paths = []
    for sheet, color_p in sheet_names.items():
        # Load data from the current sheet
        df = pd.read_excel(excel_data, sheet_name=sheet)

        # Assuming the first column is the category and the second column is the value
        categories = df.iloc[:, 0]
        values = df.iloc[:, 1]

        # Create a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140, colors=nation4.colors)
        plt.title(f'Pie Chart for {sheet} Sheet')

        # Save the pie chart as an image file
        chart_path = f'{output_dir}{sheet}_pie_chart.png'
        plt.savefig(chart_path)
        plt.close()

        chart_paths.append(chart_path)

    return chart_paths


# Create pie charts for each sheet
project_dir = 'C:/Users/ilma0/PycharmProjects/pynca/resource/piechart'
excel_data=f'{project_dir}/통계수치.xlsx'

chart_paths = create_pie_charts(excel_data=excel_data, output_dir=project_dir)
chart_paths
