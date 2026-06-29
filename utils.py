import fitz
import easyocr
import os

reader = easyocr.Reader(['en'])


def extract_text_pymupdf(uploaded_file):

    text = ""

    pdf = fitz.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def extract_text_ocr(uploaded_file):

    text = ""

    pdf = fitz.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf"
    )

    os.makedirs("temp", exist_ok=True)

    for page_number, page in enumerate(pdf):

        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))

        image_path = f"temp/page_{page_number}.png"

        pix.save(image_path)

        result = reader.readtext(image_path, detail=0)

        page_text = "\n".join(result)

        text += page_text + "\n"

        os.remove(image_path)
    pdf.close()

    return text

def extract_text_from_pdf(uploaded_file):

    text = extract_text_pymupdf(uploaded_file)

    if text.strip():
        return text

    return extract_text_ocr(uploaded_file)