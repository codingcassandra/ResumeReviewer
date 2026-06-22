
# reads Word documents 
from docx import Document

# reads PDF documents
import pdfplumber

# extract text from a Word document
def extract_docx(file):

    # open the doc
    doc = Document(file)

    #extract text from each paragraph and join them with newlines
    return "\n".join([p.text for p in doc.paragraphs])

# extract text from a PDF document
def extract_pdf(file):

    # starts with an empty string
    text = ""

    # loads the PDF
    with pdfplumber.open(file) as pdf:

        # loops through each page and extracts text
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text