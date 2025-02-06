
# nym_assignment

This package is a solution for the Nym home assignment. It parses PDF documents using pdfplumber, extracts text along with layout and font details, and structures the content into usable objects.

## Overview

The assignment consists of four main tasks:

1. **PDF to Dictionary (`pdf_to_dict`):**  
   Converts a PDF into a dictionary where keys are page numbers and values are lists of `TextualWord` objects.
    Each `TextualWord` includes the word's text and its horizontal positions (`x0` and `x1`).

2. **Populate the Chart Object (`populate_chart`):**  
   Extracts patient data (name, date of birth, and EKG validity) from the PDF's text and populates a `Chart` object.
    It also calculates the patient’s age based on the date of birth.

3. **Bonus 1 - Extra Textual Words (`pdf_to_extra_dict`):**  
   Similar to task 1, but uses an `ExtraTextualWord` class (which inherits from `TextualWord`) to also extract font information such as `fontname` and `size`. 
   The `is_bold` property indicates if the text is bold.

4. **Bonus 2 - Split into Sections (`split_to_sections`):**  
   Splits a flat list of `ExtraTextualWord` tokens into sections. 
   Each section starts with a bold token (indicating a section title).

## Requirements

- Python 3.8 or higher
- [pdfplumber](https://github.com/jsvine/pdfplumber)

## Installation

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install pdfplumber:

   ```bash
   pip install pdfplumber
   ```

## Package Structure

```
nym_assignment/
├── assignment_api.py   # Main module containing all functions and classes
├── chart1.pdf          # Example PDF file 1
├── chart2.pdf          # Example PDF file 2
├── chart3.pdf          # Example PDF file 3
└── chart_example.pdf   # Example PDF file for testing different output structure
```

## Usage

All main functions and objects are imported in `assignment_api.py`.

To test the functionality on all PDF files, simply run:

```bash
python assignment_api.py
```

This will process `chart1.pdf`, `chart2.pdf`, `chart3.pdf`, and `chart_example.pdf`, and print:
- The pages-to-words mapping
- The populated Chart info (where applicable)
- The extra textual words with font info and bold flag
- The sections split based on bold titles

## Explanation

- **pdf_to_dict:**  
  Extracts words from each page and returns a dictionary mapping page numbers to lists of `TextualWord`.

- **populate_chart:**  
  Flattens the words across pages, extracts the patient name, DOB, and EKG validity, and returns a `Chart` object.

- **pdf_to_extra_dict:**  
  Similar to `pdf_to_dict` but uses `ExtraTextualWord` to include font details.

- **split_to_sections:**  
  Groups a list of extra words into sections based on the appearance of bold tokens.

## Contact

For any questions or clarifications, please feel free to reach out.

---

This README provides an overview of the assignment, how to set up the package, and how to run and test the functionality.