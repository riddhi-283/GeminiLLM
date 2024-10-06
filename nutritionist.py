## give the photo of food and app responds how much calories are we eating 
# this is a self made project

import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
load_dotenv()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def get_response(image,prompt):
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([image[0],prompt])
    return response

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # read the file into bytes
        bytes_data=uploaded_file.getvalue()
        # below(image_parts) is the format specificaly required by google gemini pro
        image_parts=[
            {
                "mime_type":uploaded_file.type, ## get the mime type of uploaded file
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File uploaded")


st.set_page_config(page_title="CALORIES TRACKER")
st.title("CALORIES TRACKER")
upload_file=st.file_uploader("Upload the picture of food...",type=["png","jpg","jpeg"])
submit=st.button("Check Calories")

image=""
if upload_file is not None:
    image=Image.open(upload_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

# input_prompt="""
# You are an experienced and skilled nutritionist and your job is to assist the user to balance their diet by telling them how many calories does the food shown in the provided picture by listing all food items along with the calories they contain . Do not count healthy food items such as raw fruits,milk and vegetables; only consider junk food items .Also show how much workout user has to do in order to burn this much calories. Try to answer with your best accuracy.
# """

input_prompt="""
You are an expert nutritionist and you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
You can also tell whether the food is healthy or not and also mention the percentage split of the ration of carbohydrates,fats,fibres,sugar and other important things required in our diet

Also tell how much workout (in hours or minutes) is required to burn all those calories, also suggest what type of exercises they must do.

"""
if submit:
    image_data=input_image_details(upload_file)
    response=get_response(image_data,input_prompt)
    st.subheader("Response:")
    st.write(response.text)

