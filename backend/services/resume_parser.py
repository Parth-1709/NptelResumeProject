import pdfplumber
from io import BytesIO
from fastapi import UploadFile

async def resume_parser(file: UploadFile) -> str:
    text = ""

    contents = await file.read()  

    with pdfplumber.open(BytesIO(contents)) as pdf:
        for page in pdf.pages:   
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.lower()
