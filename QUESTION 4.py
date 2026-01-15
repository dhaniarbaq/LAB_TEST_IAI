import streamlit as st
import re
from PyPDF2 import PdfReader

st.title("Text Chunking Web App without NLTK Download Issues")

# Step 1: Load PDF directly
pdf_filename = "Z-TOPSIS_approach_for_performance_assessment_using_fuzzy_similarity.pdf"

try:
    pdf_reader = PdfReader(pdf_filename)
    full_text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + " "

    # Step 2: Custom sentence tokenizer using regex
    # Split on '.', '?', '!', followed by space and capital letter
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', full_text.strip())

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
