from __future__ import annotations

from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.extract import extract_email_text
from app.services.llm_openai import analyse_with_openai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MailSense AI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": None, "email_preview": ""},
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyse(
    request: Request,
    email_file: UploadFile | None = File(default=None),
    email_text: str | None = Form(default=None),
):
    email_raw = await extract_email_text(email_file, email_text)

    if not email_raw.strip():
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "error": "Envie um arquivo .txt/.pdf ou cole o texto do e-mail.",
                "email_preview": "",
            },
        )

    result = analyse_with_openai(email_raw)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "error": None,
            "result": result,
            "email_preview": email_raw[:1500],
        },
    )
