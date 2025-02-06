from dataclasses import dataclass
from datetime import date, datetime
import pdfplumber
from typing import List, Dict

# Task 1: PDF to Dictionary

@dataclass
class TextualWord:
    x0: float
    x1: float
    text: str

PagesToWords = Dict[int, List[TextualWord]]

def pdf_to_dict(pdfplumber_pdf: pdfplumber.PDF) -> PagesToWords:
    result: PagesToWords = {}
    for page_num, page in enumerate(pdfplumber_pdf.pages):
        words = page.extract_words()
        word_list = [
            TextualWord(
                x0=float(word["x0"]),
                x1=float(word["x1"]),
                text=word["text"]
            )
            for word in words
        ]
        result[page_num] = word_list
    return result

# Task 2: Populate the Chart Object

@dataclass
class Chart:
    name: str
    dob: date
    has_valid_ekg: bool

    @property
    def age(self) -> float:
        today = date.today()
        days = (today - self.dob).days
        return round(days / 365.25, 2)

def populate_chart(page_to_words: PagesToWords) -> Chart:
    all_words = []
    for words in page_to_words.values():
        all_words.extend(words)
    tokens = [w.text for w in all_words]

    name = ""
    dob = date.today()
    has_valid_ekg = False

    try:
        idx_patient = tokens.index("Patient")
        if tokens[idx_patient + 1].startswith("Name"):
            idx_dob = tokens.index("DOB:")
            name = " ".join(tokens[idx_patient + 2: idx_dob])
    except ValueError:
        pass

    try:
        idx_dob = tokens.index("DOB:")
        dob_str = tokens[idx_dob + 1]
        dob = datetime.strptime(dob_str, "%m/%d/%Y").date()
    except (ValueError, IndexError):
        dob = date.today()

    try:
        idx_ekg = tokens.index("EKG")
        if idx_ekg + 2 < len(tokens):
            has_valid_ekg = tokens[idx_ekg + 2].lower() == "valid"
    except ValueError:
        has_valid_ekg = False

    return Chart(name=name, dob=dob, has_valid_ekg=has_valid_ekg)

# Bonus 1: PDF to Extra Dictionary

@dataclass
class ExtraTextualWord(TextualWord):
    fontname: str
    size: float

    @property
    def is_bold(self) -> bool:
        return 'Bold' in self.fontname

PagesToExtraWords = Dict[int, List[ExtraTextualWord]]

def pdf_to_extra_dict(pdfplumber_pdf: pdfplumber.PDF) -> PagesToExtraWords:
    result: PagesToExtraWords = {}
    for page_num, page in enumerate(pdfplumber_pdf.pages):
        words = page.extract_words()
        extra_words = []
        for word in words:
            x0 = float(word["x0"])
            x1 = float(word["x1"])
            text = word["text"]
            top = float(word.get("top", 0))
            bottom = float(word.get("bottom", 0))
            chars = [
                char for char in page.chars
                if float(char["x0"]) >= x0 and float(char["x1"]) <= x1 and
                   float(char["top"]) >= top and float(char["bottom"]) <= bottom
            ]
            if chars:
                fontname = chars[0].get("fontname", "")
                size = float(chars[0].get("size", 0))
            else:
                fontname = ""
                size = 0.0
            extra_words.append(ExtraTextualWord(x0, x1, text, fontname, size))
        result[page_num] = extra_words
    return result

# Bonus 2: Split into Sections

PDFSection = List[List[ExtraTextualWord]]

def split_to_sections(extra_words: List[ExtraTextualWord]) -> PDFSection:
    sections: PDFSection = []
    current = []
    for word in extra_words:
        if word.is_bold:
            if current and not current[-1].is_bold:
                sections.append(current)
                current = [word]
            else:
                current.append(word)
        else:
            current.append(word)
    if current:
        sections.append(current)
    return sections

# Testing all files

if __name__ == "__main__":
    pdf_files = ["chart1.pdf", "chart2.pdf", "chart3.pdf", "chart_example.pdf"]

    for pdf_file in pdf_files:
        print(f"--- Processing {pdf_file} ---")
        with pdfplumber.open(pdf_file) as pdf:
            pages = pdf_to_dict(pdf)
            print("Pages to Words:")
            for page, words in pages.items():
                print(f"Page {page}: {[w.text for w in words]}")
        
        # Try populating chart if the tokens are as expected
        try:
            chart = populate_chart(pages)
            print("Chart Info:")
            print(f"  Name: {chart.name}")
            print(f"  DOB: {chart.dob.strftime('%m/%d/%Y')}")
            print(f"  Age: {chart.age}")
            print(f"  has_valid_ekg: {chart.has_valid_ekg}")
        except Exception as e:
            print("Chart info could not be populated:", e)

        with pdfplumber.open(pdf_file) as pdf:
            extra_pages = pdf_to_extra_dict(pdf)
            print("Extra Textual Words:")
            for page, words in extra_pages.items():
                word_texts = [f"{w.text}({'B' if w.is_bold else 'NB'})" for w in words]
                print(f"Page {page}: {word_texts}")
            # Split sections for page 0 if available
            if 0 in extra_pages:
                sections = split_to_sections(extra_pages[0])
                print("Sections (from page 0):")
                for i, sec in enumerate(sections, start=1):
                    sec_text = " ".join(w.text for w in sec)
                    print(f"  Section {i}: {sec_text}")
        print("\n")
