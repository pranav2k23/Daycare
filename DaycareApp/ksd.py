import pdfplumber
from docx import Document



def extract_text_from_pdf(pdf_path):

    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])


def process_file(file_path, file_type):
    text=""
    """Extract and summarize text based on file type."""
    if file_type == "pdf":
        text = extract_text_from_pdf(file_path)
    elif file_type == "docx":
        text = extract_text_from_docx(file_path)
    else:
        return "Unsupported file type!"

    return text

def exracttext(pdfordocx):
    file_path = pdfordocx  # Change to your file path
    file_type = "pdf"

    if file_path.endswith(".docx"):
        file_type="docx"



    # Change to "docx" if processing a DOCX file
    text = process_file(file_path, file_type)
    from transformers import pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
    print(summary[0]['summary_text'])

exracttext(r"C:\Users\prana\Downloads\Preschool\Preschool\a.pdf")
