# import sys, os
# sys.path.append('C:/Program Files/Tesseract-OCR')

import pytesseract
from PIL import Image
import pandas as pd

# Load the image from file
img = Image.open("C:/Users/ilma0/PycharmProjects/pynca/resource/00.png")

# Use tesseract to do OCR on the image
text = pytesseract.image_to_string(img)

# Since the data is structured as a table, let's first split the text into lines
lines = text.split('\n')

# Now we process each line into a list of values assuming that spaces are used to separate the columns
# We need to determine if the data is separated by a fixed width or spaces
# We'll start by assuming spaces and adjust if needed

# Let's find the number of columns by looking at the first non-empty line which should be the header
headers = []
for line in lines:
    if line.strip():  # This finds the first non-empty line
        headers = line.split()
        break

# Check if we have found a header
if headers:
    # Now we create a list of lists from the lines of text
    data = []
    for line in lines:
        if line.strip():  # This ignores empty lines
            row = line.split()
            if len(row) == len(headers):  # This ensures that the row has the right number of columns
                data.append(row)

    # Convert to a DataFrame
    df = pd.DataFrame(data[1:], columns=headers)  # Exclude the header from the data

    # Save the DataFrame to a CSV file
    csv_file_path = "/mnt/data/extracted_data.csv"
    df.to_csv(csv_file_path, index=False)
else:
    csv_file_path = "Failed to extract headers, OCR may not have read the image correctly."

csv_file_path