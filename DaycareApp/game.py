import pdfplumber
from docx import Document
from transformers import pipeline
import random


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])


def process_file(file_path, file_type):
    text = ""
    if file_type == "pdf":
        text = extract_text_from_pdf(file_path)
    elif file_type == "docx":
        text = extract_text_from_docx(file_path)
    else:
        return "Unsupported file type!"
    return text


def play_puzzle_game():
    puzzles = [
        ("I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?",
         "echo"),
        ("The more you take, the more you leave behind. What am I?", "footsteps"),
        ("I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", "map")
    ]

    puzzle, answer = random.choice(puzzles)
    print("Puzzle:", puzzle)
    user_answer = input("Your answer: ").strip().lower()

    if user_answer == answer:
        print("Correct! You solved the puzzle.")
    else:
        print("Incorrect. The answer was:", answer)


def extract_and_summarize(file_path):
    file_type = "pdf" if file_path.endswith(".pdf") else "docx"
    text = process_file(file_path, file_type)

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=50, min_length=20, do_sample=False)

    print("Summary:", summary[0]['summary_text'])
    play_puzzle_game()

    return summary[0]['summary_text']

# Example usage
# extract_and_summarize("C:/Users/prana/Downloads/Preschool/Preschool/a.pdf")
