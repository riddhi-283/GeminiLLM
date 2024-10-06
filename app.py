import os
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

##function to load genai flash model and get responses
## this gemini-1.5-flash does not produce images, it a text-ai model
model=genai.GenerativeModel('gemini-1.5-flash')
def get_response(question):
    response=model.generate_content(question)
    return response.text

##initialise streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

input=st.text_input("Input: ",key="input")
submit=st.button("Generate response")

## when submit is clicked
if submit:
    response=get_response(input)
    st.subheader("Response: ")
    st.write(response)


