import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader
import os

st.title("Text Chunking Web App using NLTK")

# Make sure the NLTK data folder exists
nltk_data_dir = "nltk_data"
os.makedirs(nltk_data_dir, exist_ok=True)

# Download 'punkt' to the local nltk_data folder
nltk.download("punkt", download_dir=nltk_data_dir)

# Tell NLTK to look in this local folder
nltk.data.path.append(nltk_data_dir)

# Load PDF
pdf_filename = "Z-TOPSIS_approach_for_performance_assessment_using_fuzzy_similarity.pdf"

try:
    pdf_reader = PdfReader(pdf_filename)
    full_text = ""
    for page in pdf_reader.pages:
        full_text += page.extract_text() + " "

    # Tokenize sentences
    sentences = sent_tokenize(full_text)

    st.subheader("Sample Extracted Sentences (Index 58 to 68)")
    start_index = 58
    end_index = 68
    if len(sentences) < start_index:
        st.write("Not enough sentences in the PDF for this index range.")
    else:
        sample_sentences = sentences[start_index-1:end_index]
        for i, s in enumerate(sample_sentences, start=start_index):
            st.write(f"{i}. {s}")

    st.subheader("All Tokenized Sentences")
    for i, s in enumerate(sentences, start=1):
        st.write(f"{i}. {s}")

except FileNotFoundError:
    st.error(f"PDF file '{pdf_filename}' not found. Please check the file location.")
