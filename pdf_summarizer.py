import streamlit as st
import pdfplumber
from transformers import pipeline
import speak

# Initialize the summarizer
summarizer = pipeline("summarization")

# Define the summarization function
def summarize_text(text):
    try:
        # Split the text into chunks to avoid exceeding the model's input limit
        chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
        summary = ''
        for chunk in chunks:
            summarized_chunk = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
            summary += summarized_chunk[0]['summary_text'] + ' '
        return summary.strip()
    except Exception as e:
        return f"An error occurred during summarization: {str(e)}"

# PDF upload and summarization
def upload_and_summarize_pdf():
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        try:
            with pdfplumber.open(uploaded_file) as book:
                full_text = ""
                for page in book.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + " "
                if full_text:
                    st.text_area("Extracted Text:", full_text, height=300)
                    summary = summarize_text(full_text)
                    st.text_area("Summary:", summary, height=150)
                    speak.speak(summary)
                else:
                    st.write("The document is empty or could not be read.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            