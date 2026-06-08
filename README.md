# Password Security Analyzer

FastAPI 기반 비밀번호 보안 분석 서비스입니다. 기존 규칙 기반 비밀번호 분석기에 ML 기반 비밀번호 강도 예측, MLflow 실험 관리, Docker 패키징, GitHub Actions 자동화, 모델 재로드/롤백 기능을 추가하여 기말 프로젝트 요구사항에 맞는 MLOps 파이프라인으로 확장했습니다.

## 주요 기능

- 규칙 기반 비밀번호 강도 분석: `/analyze`
- ML 기반 비밀번호 강도 예측: `/predict`
- 운영 모델 상태 및 메타데이터 조회: `/model/status`, `/model/metadata`
- 운영 중 모델 재로드: `/model/reload`
- 서비스 상태 확인: `/health`
- 사용자 피드백 로그 저장: `/feedback`
- MLflow 기반 실험 기록 관리: parameter, metric, artifact 저장
- Docker 기반 실행 환경 구성
- GitHub Actions 기반 테스트, 모델 학습, artifact 업로드, Docker 빌드 자동화

## 프로젝트 구조

```text
app/
  analyzer.py       # 규칙 기반 비밀번호 분석
  features.py       # ML 입력용 비밀번호 특징 추출
  feedback.py       # 사용자 피드백 로그 저장
  main.py           # FastAPI 애플리케이션
  ml_model.py       # 모델 로딩, 예측, 메타데이터 조회
data/
  password_samples.csv
models/
  password_strength_model.joblib
  password_strength_model.metadata.json
scripts/
  train_model.py    # MLflow 기반 모델 학습 스크립트
  model_ops.py      # 모델 백업 및 롤백 유틸리티
tests/
  test_api.py
  test_features.py
  test_model_ops.py
```

## 로컬 실행 방법

의존성 설치:

```bash
pip install -r requirements.txt
```

테스트 실행:

```bash
python -m pytest -q
```

FastAPI 서버 실행:

```bash
uvicorn app.main:app --reload
```

API 문서:

```text
http://127.0.0.1:8000/docs
```

## MLflow 모델 학습

모델을 학습하고 MLflow 실험 기록을 생성합니다.

```bash
python scripts/train_model.py
```

학습 스크립트가 기록하는 항목:

- Parameter: 모델 종류, 특징 개수, 학습/테스트 데이터 크기
- Metric: accuracy
- Artifact: 학습된 모델 파일, 모델 메타데이터 JSON

MLflow UI 실행:

```bash
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root mlruns --port 5000
```

MLflow UI 주소:

```text
http://127.0.0.1:5000
```

## 모델 운영 관리

현재 운영 모델 백업:

```bash
python scripts/model_ops.py backup
```

백업 목록 확인:

```bash
python scripts/model_ops.py list
```

최신 백업 모델로 롤백:

```bash
python scripts/model_ops.py rollback
```

서버 재시작 없이 모델 재로드:

```bash
curl -X POST http://127.0.0.1:8000/model/reload
```

## Docker 실행

Docker 이미지 빌드:

```bash
docker build -t password-security-analyzer:ci .
```

컨테이너 실행:

```bash
docker run --rm -p 8000:8000 password-security-analyzer:ci
```

컨테이너 실행 후 API 문서:

```text
http://127.0.0.1:8000/docs
```

## CI/CD

GitHub Actions workflow는 `.github/workflows/ci.yml`에 정의되어 있습니다.

`main` 브랜치 push 또는 pull request 발생 시 다음 단계가 자동으로 실행됩니다.

1. 의존성 설치
2. pytest 테스트 실행
3. MLflow 기반 모델 학습 실행
4. 학습된 모델 artifact 업로드
5. Docker 이미지 빌드

## Git에서 제외되는 로컬 산출물

다음 파일과 폴더는 로컬 실행/운영 중 생성되는 산출물이므로 GitHub에 업로드하지 않습니다.

- `logs/`
- `mlruns/`
- `mlflow.db`
- `models/backups/`
- `report_assets/`
