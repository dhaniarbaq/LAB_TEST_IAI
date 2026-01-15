import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import re

st.set_page_config(page_title="Text Chunking Tool", layout="wide")
st.title("Text Chunking Web App")
st.caption("Sentence-level chunking from PDF using regex tokenizer")

pdf_filename = "Z-TOPSIS_approach_for_performance_assessment_using_fuzzy_similarity.pdf"

try:
    reader = PdfReader(pdf_filename)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + " "

    st.success("PDF text successfully extracted!")

    # Regex-based sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', full_text.strip())

    st.subheader("Preview of Extracted Sentences (Index 10–20)")
    if len(sentences) >= 21:
        for i, s in enumerate(sentences[10:21], start=10):
            st.write(f"{i}: {s}")
    else:
        st.warning("Not enough sentences for preview.")

    st.subheader("All Sentence Chunks")
    df = pd.DataFrame({"Sentence Index": range(len(sentences)), "Sentence Text": sentences})
    st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.error(f"PDF file '{pdf_filename}' not found. Please check the file location.")
