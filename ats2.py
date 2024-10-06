# in this project we will take a pdf and directly extract text from it without converting it into an image (so there is no need to install poppler)
# so this time we will not be using pdf2mage instead we will use pypdf2 
import streamlit as st
import os 
import PyPDF2 as pdf
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def get_response(pdf_text,input,prompt):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([pdf_text,input,prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

input_prompt="""
You have to act like a very skilled or experienced ATS(Application Tracking System) with a deep understanding of all technical fields like software engineer,data scientist, data analyst, NLP enginner, AI/ML engineer. Your task is to evaluate the resume based on the given job description . You must consider that the market is highly competetive so you must provide the best assistance you can. Once you have evalauted the provided resume you have to tell all these things : percentage match of the resume based on the job description, what is the current resume score and what keywords are missing with high accuracy. Also suggest the how can the score of provided resume be increased under the heading "Suggestions to improve score"
resume{text}
description:{jd}


"""

st.title("SMART ATS")
st.text("Improve your Resume ATS")

jd=st.text_area("Paste the job description")
uploaded_file=st.file_uploader("Upload your resume...",type="pdf")

submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_response(text,jd,input_prompt)
        st.subheader("Response:")
        st.write(response)

# I want answer in a single string having structure
# {{"JD Match":"%","Missing Keywords:[]","Profile Summary":""}}

