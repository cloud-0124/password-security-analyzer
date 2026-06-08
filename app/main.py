from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.analyzer import analyze_password
from app.feedback import feedback_summary, save_feedback
from app.ml_model import model_service

app = FastAPI()

class PasswordRequest(BaseModel):
    password: str

class FeedbackRequest(BaseModel):
    password: str
    is_correct: bool
    comment: str = ""

@app.get("/")
def root():
    return FileResponse("app/static/index.html")

@app.post("/analyze")
def analyze(req: PasswordRequest):
    return analyze_password(req.password)

@app.post("/predict")
def predict(req: PasswordRequest):
    return model_service.predict(req.password)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_available": model_service.model is not None,
        "feedback": feedback_summary(),
    }

@app.get("/model/status")
def model_status():
    return {
        "available": model_service.model is not None,
        "model_path": str(model_service.model_path),
        "message": model_service.load_error or "Model is loaded.",
    }

@app.post("/model/reload")
def model_reload():
    model_service.load()
    return model_status()

@app.post("/feedback")
def feedback(req: FeedbackRequest):
    rule_result = analyze_password(req.password)
    prediction_result = model_service.predict(req.password)
    row = save_feedback(
        password=req.password,
        rule_level=rule_result["level"],
        ml_prediction=prediction_result["prediction"],
        is_correct=req.is_correct,
        comment=req.comment,
    )
    return {
        "saved": True,
        "feedback": row,
    }
