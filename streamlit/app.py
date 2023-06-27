import zipfile
from PIL import Image
import streamlit as st
import os
import pandas as pd
import numpy as np
from paddleocr import PaddleOCR
import tempfile
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm


nlp = spacy.load('en_core_web_trf')

st.title('Text Recognition')

# Create a folder uploader input field
uploaded_folder = st.file_uploader("Upload a folder of images", type=["zip"], accept_multiple_files=False)

# Process the uploaded folder if available
if uploaded_folder is not None:
    # Create a temporary directory to extract the uploaded folder
    temp_folder = tempfile.TemporaryDirectory()
    
    # Extract the uploaded folder to the temporary directory
    with zipfile.ZipFile(uploaded_folder) as zip_ref:
        zip_ref.extractall(temp_folder.name)
    
    # Get the list of image files in the extracted folder
    image_files = [os.path.join(temp_folder.name, filename) for filename in os.listdir(temp_folder.name) if filename.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Process each image in the folder
    for image_file in image_files:
        # Use the image file
        image = Image.open(image_file)

        # Display the image
        st.image(image, caption='Uploaded Image')

        # Perform further processing on the image as needed
        
        # Your code here for processing the image
        ocr = PaddleOCR(lang='en')
        print(image_file)
        result = ocr.ocr(image_file)
        print("Result: ", result)
        
        # Display the detected text
        st.subheader("Detected Text:")
        text = []
        for res in result:
            for i in range(0, len(result[0]), 1):
                if res[i][1][1]>0.88:
                    text.append(res[i][1][0])

        # print("TEXT: ",text)
        string = ' '.join(map(str, text))
        clean_sentence = ' '.join(string.split())

        temp = []
        for string in text:
            doc = nlp(string)
            temp.append([(X.text, X.label_) for X in doc.ents])
            print([(X.text, X.label_) for X in doc.ents])
            # displacy.render(doc, style='ent')
        
        st.write("IDENTIFIED NAMES: ")
        for i in temp:
            if i:
                if i[0][1] == "PERSON" or i[0][1]=="GPE":
                    st.write(i[0][0])
