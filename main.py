import streamlit as st
from chatbot import chat_with_bot
from pdf_summarizer import upload_and_summarize_pdf
import speak

# Streamlit App Layout
st.title("Healthcare Chatbot")
st.write("This chatbot can assist you with basic medical advice and summarize PDF documents.")

# User Input for Chatbot
st.subheader("Chat with the bot")
user_input = st.text_input("You: ", "")

if user_input:
    response = chat_with_bot(user_input)
    st.text_area("Bot:", response, height=150)
    speak.speak(response)

# PDF Upload and Processing
st.subheader("PDF Text Extraction & Summarization")
st.image("pdf_icon.png", caption="Upload a PDF file", width=100)
upload_and_summarize_pdf()
