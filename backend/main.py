from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from file_parser import extract_docx, extract_pdf
from resume_analyzer import analyze_match
import os

port = int(os.environ.get("PORT", 8000))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://resume-reviewer-pied.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/match-job")
async def match_job(
    resume: UploadFile = File(...),
    job_text: str = Form(...)
):
    try:
        if resume.filename.lower().endswith(".pdf"):
            resume_text = extract_pdf(resume.file)
        else:
            resume_text = extract_docx(resume.file)

        result = analyze_match(resume_text, job_text)

        return {
            "filename": resume.filename,
            "match": result
        }

    except Exception as e:
        return {
            "filename": resume.filename,
            "match": None,
            "error": str(e)
        }