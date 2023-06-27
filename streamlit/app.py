import zipfile
from PIL import Image
import streamlit as st
import os
import re
import pandas as pd
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
import tempfile
import base64

ocr = PaddleOCR(lang = 'en')

def extract_aadhar_info(confidence_threshold,img_path):
        name_num = []
        result = ocr.ocr(img_path)
        extracted_numbers = [] 
        for res in result:
            for line in res:
                text = line[1][0]
                confidence = line[1][1]
                
                matches = re.findall(r'\b(\d{4}\s?\d{4}\s?\d{4}|\d{8}\s?\d{4}|\d{4}\s?\d{8}|\d{12})\b', text)
                if matches:
                    extracted_numbers.extend(matches)
        
        
        result = ocr.ocr(img_path)
        extracted_names = [res[i][1][0] for i in range(0, len(result[0]), 1) for res in result if res[i][1][1] >= confidence_threshold]
        
        
        if len(extracted_names) >= 2:
            name_num.append({"Name": extracted_names[1], "Number": extracted_numbers[-1]})

        return name_num


st.title('Aadhar Name & Number Recognition')
final_list = {}
id = 1
multiple_images = st.checkbox("Upload Multiple Images as Zip")
if multiple_images:
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
            title_msg = "Card "+str(id)
            st.title(title_msg)
            # Display the image
            st.image(image, caption='Uploaded Image')

            # Perform further processing on the image as needed
            
            # Your code here for processing the image
            name_num = extract_aadhar_info(0.83,image_file)
            
            # Display the detected text
            st.subheader("Detected Text:")
            for item in name_num:
                st.write("Name:", item["Name"])
                st.write("Aadhar Number:", item["Number"])
                final_list[id] = [item["Name"],item["Number"]]
                id+=1
        print(final_list)
        temp_folder.cleanup()

else:
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

    if uploaded_file is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())

        # Use the uploaded file
        image = Image.open(uploaded_file)
        # Process the image and display the result
        title_msg = "Card "+str(id)
        st.title(title_msg)
        # Display the image
        st.image(image, caption='Uploaded Image')

        # Perform further processing on the image as needed
        
        # Your code here for processing the image
        name_num = extract_aadhar_info(0.83,temp_file.name)
        
        # Display the detected text
        st.subheader("Detected Text:")
        for item in name_num:
            st.write("Name:", item["Name"])
            st.write("Aadhar Number:", item["Number"])
            final_list[id] = [item["Name"],item["Number"]]
            id+=1
        print(final_list)
        temp_file.close()
    

# Create a download button for the CSV file
df = pd.DataFrame.from_dict(final_list,orient='index',columns=['Name','Aadhaar Number'])
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
filename = "Aadhaar.csv"
button_label = "Download Data as CSV"
download_link = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{button_label}</a>'
st.download_button(
    label=button_label,
    data=csv,
    file_name=filename,
    mime='text/csv'
) 
