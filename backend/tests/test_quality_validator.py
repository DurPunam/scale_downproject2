import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parent.parent
    / "services"
    / "quality-validator"
    / "app"
    / "validator.py"
)
spec = importlib.util.spec_from_file_location("validator", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
validate = module.validate


def test_validation_accepts_good_similarity() -> None:
    result = validate(0.92, 0.8)
    assert result.action == "accept"


def test_validation_reprocesses_low_similarity() -> None:
    result = validate(0.84, 0.8)
    assert result.action == "reprocess"
