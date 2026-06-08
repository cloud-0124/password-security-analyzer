from pathlib import Path
from typing import Any

from app.features import FEATURE_NAMES, password_features


MODEL_PATH = Path("models/password_strength_model.joblib")


class PasswordStrengthModel:
    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = model_path
        self.model: Any | None = None
        self.load_error: str | None = None
        self.load()

    def load(self) -> None:
        if not self.model_path.exists():
            self.model = None
            self.load_error = f"Model file not found: {self.model_path}"
            return

        try:
            import joblib

            self.model = joblib.load(self.model_path)
            self.load_error = None
        except Exception as exc:
            self.model = None
            self.load_error = str(exc)

    def predict(self, password: str) -> dict[str, Any]:
        features = password_features(password)
        feature_map = dict(zip(FEATURE_NAMES, features, strict=True))

        if self.model is None:
            return {
                "available": False,
                "prediction": None,
                "confidence": None,
                "features": feature_map,
                "message": self.load_error or "Model is not loaded.",
            }

        prediction = self.model.predict([features])[0]
        confidence = None

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba([features])[0]
            confidence = float(max(probabilities))

        return {
            "available": True,
            "prediction": prediction,
            "confidence": confidence,
            "features": feature_map,
            "message": "Model prediction completed.",
        }


model_service = PasswordStrengthModel()
