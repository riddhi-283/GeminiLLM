## this chatbot is able to remember context as well so its a better one
import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv
load_dotenv()

# importing generative model and other required components
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Function to get the model's response including previous context
def get_gemini_response(question, history):
    # Construct the conversation history
    conversation = "\n".join(f"{speaker}: {message}" for speaker, message in history)
    conversation += f"\nYou: {question}"
    
    # Send the complete conversation to the model
    response = chat.send_message(conversation, stream=True)
    return response

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input, st.session_state['chat_history'])
    
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    complete_response=""
    for chunk in response:
        complete_response+=chunk.text
        st.write(chunk.text)
    st.session_state['chat_history'].append(("Bot", complete_response))

st.subheader("The Chat History is")
for speaker, message in st.session_state['chat_history']:
    st.write(f"{speaker}: {message}")
