from PyPDF2 import PdfReader
import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

reader = PdfReader("Z-TOPSIS_approach_for_performance_assessment_using_fuzzy_similarity.pdf")

text = ""
for page in reader.pages:
    text += page.extract_text()

sentences = sent_tokenize(text)

chunk = sentences[58:69]

print("Semantic Sentence Chunk:")
for sentence in chunk:
    print(sentence)
