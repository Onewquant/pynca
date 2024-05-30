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

# Create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Year', y='TDM', data=df, palette='Blues_d')

# Add title and labels
plt.title('TDM Cases Over Years')
plt.xlabel('Year')
plt.ylabel('Number of TDM Cases')

# Display the plot
plt.savefig(chart_path)
plt.close()

