import csv
from datetime import datetime, timezone
from pathlib import Path


FEEDBACK_LOG_PATH = Path("logs/feedback.csv")
FIELD_NAMES = [
    "created_at",
    "password_length",
    "rule_level",
    "ml_prediction",
    "is_correct",
    "comment",
]


def save_feedback(
    password: str,
    rule_level: str,
    ml_prediction: str | None,
    is_correct: bool,
    comment: str = "",
) -> dict[str, str | int | bool | None]:
    FEEDBACK_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "password_length": len(password),
        "rule_level": rule_level,
        "ml_prediction": ml_prediction,
        "is_correct": is_correct,
        "comment": comment,
    }

    file_exists = FEEDBACK_LOG_PATH.exists()
    with FEEDBACK_LOG_PATH.open("a", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    return row


def feedback_summary() -> dict[str, int | str]:
    if not FEEDBACK_LOG_PATH.exists():
        return {
            "feedback_count": 0,
            "log_path": str(FEEDBACK_LOG_PATH),
        }

    with FEEDBACK_LOG_PATH.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        feedback_count = sum(1 for _ in reader)

    return {
        "feedback_count": feedback_count,
        "log_path": str(FEEDBACK_LOG_PATH),
    }
