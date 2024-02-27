# import sys, os
# sys.path.append('C:/Program Files/Tesseract-OCR')

import pytesseract
from PIL import Image
import pandas as pd

# Load the image from file
img = Image.open("C:/Users/ilma0/PycharmProjects/pynca/resource/pt_type.png")

# Use tesseract to do OCR on the image
text = pytesseract.image_to_string(img)

# Since the data is structured as a table, let's first split the text into lines
lines = text.split('\n')

pt_type = ''.join(lines).replace('K','X').replace('Q','O')
len(pt_type)/2