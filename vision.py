import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

##function to load genai flash model and get responses
## this gemini-1.5-flash does not produce images, it a text-ai model

#------- works excellent----------
model=genai.GenerativeModel('gemini-1.5-flash-001')

# model=genai.GenerativeModel('gemini-pro-vision') ---------also works good

def get_response(input,image):
    if input !="":
        response=model.generate_content([input,image])
    else:
        response=model.generate_content(image)
    return response.text

##initialise streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Image Application")
input=st.text_input("Input: ",key="input")

## take image as input 
upload_file=st.file_uploader("Choose an image to upload...",type=["jpg","jpeg","png"])
image=""

if upload_file is not None:
    image=Image.open(upload_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("Provide Description About Image")

## if submit is done:
if submit:
    response=get_response(input,image)
    st.subheader("Description:")
    st.write(response)


