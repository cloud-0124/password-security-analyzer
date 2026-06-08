import argparse
import csv
import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.features import FEATURE_NAMES, password_features


def load_dataset(data_path: Path) -> tuple[list[list[float]], list[str]]:
    features: list[list[float]] = []
    labels: list[str] = []

    with data_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            features.append(password_features(row["password"]))
            labels.append(row["label"])

    return features, labels


def train(data_path: Path, model_path: Path, experiment_name: str) -> dict[str, object]:
    mlflow.set_experiment(experiment_name)
    features, labels = load_dataset(data_path)

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.3,
        random_state=42,
        stratify=labels,
    )

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )

    with mlflow.start_run(run_name="password-strength-logistic-regression") as run:
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions, output_dict=True)

        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("feature_count", len(FEATURE_NAMES))
        mlflow.log_param("train_size", len(x_train))
        mlflow.log_param("test_size", len(x_test))
        mlflow.log_metric("accuracy", accuracy)

        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, model_path)

        metadata = {
            "run_id": run.info.run_id,
            "experiment_name": experiment_name,
            "model_path": str(model_path),
            "features": FEATURE_NAMES,
            "accuracy": accuracy,
            "classification_report": report,
        }
        metadata_path = model_path.with_suffix(".metadata.json")
        metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        mlflow.sklearn.log_model(model, artifact_path="model")
        mlflow.log_artifact(str(model_path))
        mlflow.log_artifact(str(metadata_path))

    return metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train password strength ML model.")
    parser.add_argument("--data", default="data/password_samples.csv")
    parser.add_argument("--model", default="models/password_strength_model.joblib")
    parser.add_argument("--experiment", default="password-security-analyzer")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = train(Path(args.data), Path(args.model), args.experiment)
    print(json.dumps(result, indent=2))
