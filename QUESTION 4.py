import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
from PyPDF2 import PdfReader
import pandas as pd

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="NLTK Text Chunking Tool",
    layout="wide"
)

st.title("Text Chunking Web App")
st.caption("Sentence-level chunking from PDF using NLTK")

# -------------------------------
# Download NLTK resources (cached)
# -------------------------------
@st.cache_resource
def download_nltk_data():
    nltk.download("punkt")

download_nltk_data()

# -------------------------------
# Load PDF directly by filename
# -------------------------------
pdf_filename = "Z-TOPSIS_approach_for_performance_assessment_using_fuzzy_similarity.pdf"

try:
    reader = PdfReader(pdf_filename)
    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + " "

    st.success("PDF text successfully extracted!")

    # -------------------------------
    # Step 3: Sentence tokenization
    # -------------------------------
    sentences = sent_tokenize(extracted_text)

    st.subheader("Preview of Extracted Sentences (Index 10–20)")

    if len(sentences) >= 21:
        preview = sentences[10:21]
        for i, sentence in enumerate(preview, start=10):
            st.write(f"{i}: {sentence}")
    else:
        st.warning("The document does not contain enough sentences for preview.")

    # -------------------------------
    # Step 4: Display all sentence chunks
    # -------------------------------
    st.subheader("Sentence Chunking Results")

    chunk_df = pd.DataFrame({
        "Sentence Index": range(len(sentences)),
        "Sentence Text": sentences
    })

    st.dataframe(chunk_df, use_container_width=True)

    st.info(
        "The NLTK sentence tokenizer splits large unstructured text into smaller, "
        "meaningful sentence chunks that are useful for semantic analysis, "
        "summarization, and NLP pipelines."
    )

except FileNotFoundError:
    st.error(f"PDF file '{pdf_filename}' not found. Please check the file location.")
