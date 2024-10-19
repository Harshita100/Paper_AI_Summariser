import streamlit as st
import pdfplumber
import requests
import os
from groq import Groq

def add_custom_css():
    st.markdown("""
    <style>
        .body {
            background-image: url('images.jpeg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 15px 40px;
            font-size: 18px;
            display: block;
            margin: 0 auto;
        }
        .stTextArea>div>textarea {
            border: 2px solid #4CAF50;
            border-radius: 8px;
            padding: 10px;
            font-size: 18px;
        }
        .title h1 {
            text-align: center;
            font-family: 'Arial Black', sans-serif;
            text-transform: uppercase;
            font-size: 48px;
            color: #4CAF50;
        }
    </style>
    """, unsafe_allow_html=True)

add_custom_css()

# Summarize the full text using Groq's Mistral model
def summarize_text(client, text):
    try:
        chat = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Summarize the following text: {text}"
            }],
            model="mixtral-8x7b-32768"
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

st.markdown('<div class="title"><h1>PDF Extractor</h1></div>', unsafe_allow_html=True)

# File uploader to select the PDF
file = st.file_uploader("Choose a PDF file:", type="pdf")

# Extract text from the uploaded PDF
text = ""
if file is not None:
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'

# Initialize Groq client
client = Groq(api_key="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")

# Button to trigger summarization
if st.button("Summarize"):
    if text:
        # Summarize the entire text
        summary = summarize_text(client, text)

        # Display the summary
        st.subheader("Summary:")
        st.text_area("Summarized Text:", summary, height=300)
