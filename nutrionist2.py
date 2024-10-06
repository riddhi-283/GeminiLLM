# everything else is same , just that prompt is different 
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
load_dotenv()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def get_response(input_prompt,image):
    model=genai.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input_prompt,image[0]])
    return response.text

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
uploaded_file=st.file_uploader("Upload the picture of food...",type=["png","jpg","jpeg"])
submit=st.button("Check Calories")

image=""
if uploaded_file is not None:
    # as soon as we upload a file, image should get uploaded below
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
You can also tell whether the food is healthy or not and also mention the percentage split of the ration of carbohydrates,fats,fibres,sugar and other important things required in our diet

Also tell how much workout (in hours or minutes) is required to burn all those calories, also suggest what type of exercises they must do.

"""

## If submit button is clicked

if submit:
    image_data=input_image_details(uploaded_file)
    response=get_response(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)