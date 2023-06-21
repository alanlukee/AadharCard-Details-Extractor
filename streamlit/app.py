from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from paddleocr import PaddleOCR
import tempfile

st.title('Text Recognition')

# Create a file uploader input field
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Process the uploaded image if available
if uploaded_file is not None:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())

    # Use the uploaded file
    image = Image.open(uploaded_file)

    # Display the uploaded image
    st.image(image, caption='Uploaded Image')

    # Perform further processing on the image as needed
    
    # Your code here for processing the image
    ocr = PaddleOCR(lang = 'en')
    print(temp_file)
    result = ocr.ocr(temp_file.name)
    print("Result: ",result)
    # Display the detected text
    st.subheader("Detected Text:")
    for res in result:
        for i in range(0,len(result[0]),1):
            st.write(res[i][1][0])