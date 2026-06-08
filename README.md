# Password Security Analyzer

FastAPI-based password security analysis service. The project extends the original rule-based password analyzer with ML-based strength prediction, MLflow experiment tracking, Docker packaging, GitHub Actions automation, and model operation utilities.

## Features

- Rule-based password strength analysis: `/analyze`
- ML-based password strength prediction: `/predict`
- Model status and metadata monitoring: `/model/status`, `/model/metadata`
- Runtime model reload: `/model/reload`
- Service health check: `/health`
- User feedback logging: `/feedback`
- MLflow experiment tracking with metrics, parameters, and artifacts
- Docker-based execution environment
- GitHub Actions CI for tests, model training, artifact upload, and Docker build

## Project Structure

```text
app/
  analyzer.py       # Rule-based password analyzer
  features.py       # Password feature extraction for ML
  feedback.py       # Feedback log management
  main.py           # FastAPI application
  ml_model.py       # Model loading, prediction, and metadata access
data/
  password_samples.csv
models/
  password_strength_model.joblib
  password_strength_model.metadata.json
scripts/
  train_model.py    # MLflow training script
  model_ops.py      # Model backup and rollback utility
tests/
  test_api.py
  test_features.py
  test_model_ops.py
```

## Local Setup

```bash
pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest -q
```

Start the API server:

```bash
uvicorn app.main:app --reload
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## MLflow Training

Train the model and record the experiment:

```bash
python scripts/train_model.py
```

The training script records:

- Parameters: model type, feature count, train/test size
- Metric: accuracy
- Artifacts: trained model and metadata JSON

Start MLflow UI:

```bash
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root mlruns --port 5000
```

MLflow UI:

```text
http://127.0.0.1:5000
```

## Model Operation

Back up the current production model:

```bash
python scripts/model_ops.py backup
```

List model backups:

```bash
python scripts/model_ops.py list
```

Rollback to the latest backup:

```bash
python scripts/model_ops.py rollback
```

Reload the model without restarting the service:

```bash
curl -X POST http://127.0.0.1:8000/model/reload
```

## Docker

Build the Docker image:

```bash
docker build -t password-security-analyzer:ci .
```

Run the container:

```bash
docker run --rm -p 8000:8000 password-security-analyzer:ci
```

## CI/CD

GitHub Actions workflow is defined in `.github/workflows/ci.yml`.

On push to `main` or pull request, it runs:

1. Dependency installation
2. Pytest
3. Model training with MLflow
4. Trained model artifact upload
5. Docker image build

## Runtime Data

The following local runtime artifacts are excluded from Git:

- `logs/`
- `mlruns/`
- `mlflow.db`
- `models/backups/`
- `report_assets/`
