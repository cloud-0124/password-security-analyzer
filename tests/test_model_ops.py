from pathlib import Path

from scripts.model_ops import backup_current_model, rollback_latest_model


def test_backup_and_rollback_model_files(tmp_path: Path):
    model_path = tmp_path / "password_strength_model.joblib"
    metadata_path = tmp_path / "password_strength_model.metadata.json"
    backup_dir = tmp_path / "backups"

    model_path.write_text("version-1", encoding="utf-8")
    metadata_path.write_text('{"version": 1}', encoding="utf-8")

    backup = backup_current_model(model_path, metadata_path, backup_dir)
    assert Path(backup["model_backup"]).exists()
    assert Path(backup["metadata_backup"]).exists()

    model_path.write_text("version-2", encoding="utf-8")
    metadata_path.write_text('{"version": 2}', encoding="utf-8")

    rollback = rollback_latest_model(model_path, metadata_path, backup_dir)

    assert Path(rollback["restored_model"]).exists()
    assert model_path.read_text(encoding="utf-8") == "version-1"
    assert metadata_path.read_text(encoding="utf-8") == '{"version": 1}'
