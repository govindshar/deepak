from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from app.summarizer import read_excel
from app.groq_api import call_groq
from app.utils import export_to_pdf
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print("🔑 Loaded GROQ key is:", os.getenv("GROQ_API_KEY"))  # Debug

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

history = []

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "history": history
    })

@app.post("/summarize", response_class=HTMLResponse)
async def summarize(
    request: Request,
    file: UploadFile,
    style: str = Form("Summarize the Excel data"),
    word_limit: int = Form(300)
):
    excel_text = read_excel(await file.read())

    prompt = (
        f"You are a highly skilled analyst.\n\n"
        f"Analyze the following Excel table:\n\n{excel_text}\n\n"
        f"{style}. The summary should be detailed and around {word_limit} words."
    )

    output = call_groq(prompt)

    entry = {"id": len(history), "summary": output}
    history.insert(0, entry)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "summary": output,
        "history": history
    })

@app.get("/pdf/{summary_id}")
def download_pdf(summary_id: int):
    summary_text = history[summary_id]["summary"]
    pdf_path = export_to_pdf(summary_text, summary_id)
    return FileResponse(pdf_path, filename=f"summary_{summary_id}.pdf", media_type='application/pdf')
