from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.analyzer import analyze_password

app = FastAPI()

class PasswordRequest(BaseModel):
    password: str

@app.get("/")
def root():
    return FileResponse("app/static/index.html")

@app.post("/analyze")
def analyze(req: PasswordRequest):
    return analyze_password(req.password)