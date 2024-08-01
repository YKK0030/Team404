import streamlit as st
import chatbot
from pdf_summarizer import upload_and_summarize_pdf
import speak
import speech_recognition as sr

# Streamlit App Layout
st.set_page_config(page_title="Healthcare Chatbot", page_icon="🩺", layout="wide")

st.title("Healthcare Chatbot 🩺")
st.write("""
    Welcome to the Healthcare Chatbot! This bot can assist you with basic medical advice and 
    also summarize PDF documents. Please note that this is not a substitute for professional 
    medical advice.
""")

# Initialize speech recognizer
listener = sr.Recognizer()

def take_command():
    """Listen for voice input and return it as text."""
    try:
        with sr.Microphone() as source:
            st.write('Listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            st.write('You:', command)
            return command
    except sr.RequestError:
        st.write("Sorry, I couldn't reach the Google API.")
        return "error"
    except sr.UnknownValueError:
        st.write("Sorry, I did not understand that.")
        return "error"
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
        return "error"

# Chatbot Interaction
st.subheader("Chat with the Bot")
input_mode = st.radio("Choose input mode:", ("Text", "Voice"))

user_input = ""

if input_mode == "Text":
    user_input = st.text_input("Type your message here...", key="text_input")
elif input_mode == "Voice":
    if st.button("Start Listening"):
        user_input = take_command()
        if user_input == "start":
            st.write("Voice command mode activated. Please say your command.")
            user_input = take_command()

if user_input and user_input != "error":
    response = chatbot.chat_with_bot(user_input)
    st.write(f"<div class='user chat'><strong>You:</strong> {user_input}</div>", unsafe_allow_html=True)
    st.write(f"<div class='bot chat'><strong>Bot:</strong> {response}</div>", unsafe_allow_html=True)
    speak.speak(response)

# PDF Upload and Processing
st.subheader("PDF Text Extraction & Summarization")
st.write("Upload a PDF file to extract and summarize its text.")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    summary = upload_and_summarize_pdf()
    st.write("Summary of the PDF:")
    st.text_area("Summary:", speak.speak(summary), height=150)

# Footer
st.write("---")
st.write("Created by [Your Name](https://github.com/your-github-profile)")
