# AadharCard-Details-Extractor

### Details:
This repository provides a program that can read an Aadhaar card and provide the corresponding name and Aadhaar number. It can run with the help of a web-based GUI locally host using the streamlit package.
### Steps:
1. Fork the repository.
2. Clone it into your local system using the `git clone` command or the web GUI. 
### Setting up and using the application:
1. Install the following packages: `pandas`, `numpy`, `Pillow ( For Python Image Library (PIL) )`, `streamlit`,`openCV`, `paddlepaddle`, `paddleocr`.
2. Change directory to the streamlit folder and run the command
   `streamlit run app.py`
for the GUI.
3. If you want the code, open the ipynb file and click on the hyperlink provided to go to the cell with the coressponding function code.
4. `streamlit` is only required if you want the GUI else it is not required

> Note: Ensure that the python version is >=3.9 and <=3.10.12 . Also ensure that the images are properly taken such that the Government of India heading (in Aadhaar cards) is the first sentence visible.
> Make sure that the image must be upright and should not be rotated to the left or right.
> Ensure that there are no background text in the image (the image should only contain the details of the aadhar card you want to scan).

### Screenshots:


![ss1](https://github.com/alanlukee/AadharCard-Details-Extractor/assets/73834506/1d88104b-ac01-480e-8547-ece32281e644)
![ss2](https://github.com/alanlukee/AadharCard-Details-Extractor/assets/73834506/702778ac-3358-4366-9641-3f745a8e36f7)
