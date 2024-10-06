# in this project we will upload picture of an invoice/bill and we will ask questions like address, date etc mentioned in the bill(it becomes easier to extract these info using gemini then using tesseract and ocr) 

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

## Function to load gemini pro vision
# ex: input:"act like an invoice extractor", image=image, prompt="what is the date"

########## any of these can be used ##############
# model=genai.GenerativeModel("gemini-1.5-flash")
model=genai.GenerativeModel("gemini-pro-vision")

#Inside the get_response function, image[0] accesses the first (and only) element in the image list, which is the dictionary containing the MIME type and image data.
def get_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response

## we will convert the image into bytes and take all information from that image in form of bytes itself
# This function returns a list containing one dictionary.
def input_image_details(upload_file):
    if upload_file is not None:
        bytes_data=upload_file.getvalue()

        image_parts=[
            {
                "mime_type":upload_file.type, ## get the mime type of uploaded file
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")


st.set_page_config(page_title="Multilangauge invoice extractor")
st.header("MultiLanguage Invoice Extractor")
input=st.text_input("Input: ",key="input")
upload_file=st.file_uploader("Upload an image of the invoice..",type=["png","jpg","jpeg"])

image=""
if upload_file is not None:
    image=Image.open(upload_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("Tell me about the invoice")
input_prompt="""
You are an expert in understanding invoices, we will upload an image of an invoice and you will have to answer amy questions based on uploaded invoice image only. Do not make up any answers.If the answer is not present in invoice image , then print "i dont know".
"""
if submit:
    image_data=input_image_details(upload_file)
    response=get_response(input_prompt,image_data,input)
    st.subheader("Response:")
    st.write(response.text)







