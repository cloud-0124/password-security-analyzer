import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ml_model import MODEL_PATH


METADATA_PATH = MODEL_PATH.with_suffix(".metadata.json")
BACKUP_DIR = Path("models/backups")


def backup_current_model(
    model_path: Path = MODEL_PATH,
    metadata_path: Path = METADATA_PATH,
    backup_dir: Path = BACKUP_DIR,
) -> dict[str, str]:
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir.mkdir(parents=True, exist_ok=True)

    model_backup = backup_dir / f"{model_path.stem}_{timestamp}{model_path.suffix}"
    shutil.copy2(model_path, model_backup)

    metadata_backup = ""
    if metadata_path.exists():
        metadata_target = backup_dir / f"{metadata_path.stem}_{timestamp}{metadata_path.suffix}"
        shutil.copy2(metadata_path, metadata_target)
        metadata_backup = str(metadata_target)

    return {
        "model_backup": str(model_backup),
        "metadata_backup": metadata_backup,
    }


def list_model_backups(backup_dir: Path = BACKUP_DIR) -> list[Path]:
    if not backup_dir.exists():
        return []

    return sorted(
        backup_dir.glob(f"{MODEL_PATH.stem}_*{MODEL_PATH.suffix}"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def rollback_latest_model(
    model_path: Path = MODEL_PATH,
    metadata_path: Path = METADATA_PATH,
    backup_dir: Path = BACKUP_DIR,
) -> dict[str, str]:
    backups = list_model_backups(backup_dir)
    if not backups:
        raise FileNotFoundError(f"No model backups found in {backup_dir}")

    latest_model_backup = backups[0]
    shutil.copy2(latest_model_backup, model_path)

    timestamp = latest_model_backup.stem.replace(f"{model_path.stem}_", "", 1)
    metadata_backup = backup_dir / f"{metadata_path.stem}_{timestamp}{metadata_path.suffix}"
    restored_metadata = ""

    if metadata_backup.exists():
        shutil.copy2(metadata_backup, metadata_path)
        restored_metadata = str(metadata_backup)

    return {
        "restored_model": str(latest_model_backup),
        "restored_metadata": restored_metadata,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage production model backups.")
    parser.add_argument("action", choices=["backup", "list", "rollback"])
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.action == "backup":
        print(backup_current_model())
    elif args.action == "list":
        print([str(path) for path in list_model_backups()])
    elif args.action == "rollback":
        print(rollback_latest_model())


if __name__ == "__main__":
    main()
