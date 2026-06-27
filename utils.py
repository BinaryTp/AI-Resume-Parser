import fitz
import easyocr
from PIL import Image
import os


reader = easyocr.Reader(['en'])


def extract_text_from_pdf(uploaded_file):

    text = ""

    pdf = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")

    os.makedirs("temp", exist_ok=True)

    for page_number, page in enumerate(pdf):

        mat = fitz.Matrix(3, 3)
        pix = page.get_pixmap(matrix=mat)

        image_path = f"temp/page_{page_number}.png"

        pix.save(image_path)

        result = reader.readtext(image_path, detail=0)

        page_text = "\n".join(result)

        text += page_text + "\n"

    pdf.close()

    return text