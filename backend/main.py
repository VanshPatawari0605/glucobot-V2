import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from utils.predict import load_model, run_prediction
from utils.pdf_gen import generate_report_pdf
from utils.pdf_reader import extract_pdf_values
from utils.chat import ask_gemini

load_dotenv()

app = FastAPI(title="GlucoBot API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model, scaler = load_model()


# ── Schemas ──────────────────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    pregnancies: float
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    dpf: float
    age: float

class ReportRequest(BaseModel):
    inputs: dict
    probability: float
    label: str

class ChatRequest(BaseModel):
    message: str
    history: list = []


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "GlucoBot API v2 running"}


@app.post("/predict")
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Run train.py first.")
    result = run_prediction(model, scaler, req.dict())
    return result


@app.post("/report")
def report(req: ReportRequest):
    buf = generate_report_pdf(req.inputs, req.probability, req.label)
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=GlucoBot_Report.pdf"}
    )


@app.post("/chat")
async def chat(req: ChatRequest):
    reply = await ask_gemini(req.message, req.history)
    return {"reply": reply}


@app.post("/parse-pdf")
async def parse_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    values, error = extract_pdf_values(contents)
    if error:
        return {"success": False, "error": error, "values": {}}
    return {"success": True, "error": None, "values": values}
