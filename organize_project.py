import shutil
from pathlib import Path
import json

ROOT = Path.cwd()
DRY_RUN = False

def log(msg):
    print(msg)

def move(src, dst):
    if not src.exists():
        return
    if DRY_RUN:
        log(f"[DRY MOVE] {src} -> {dst}")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

def remove(path):
    if not path.exists():
        return
    if DRY_RUN:
        log(f"[DRY REMOVE] {path}")
    else:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

# =========================
# CREATE STRUCTURE
# =========================
def create_structure():
    for p in [
        "models/bigru",
        "experiments/exp_001/outputs",
        "notebooks",
        "comparisons",
        "archives"
    ]:
        if not DRY_RUN:
            (ROOT / p).mkdir(parents=True, exist_ok=True)

# =========================
# FIX NESTED MODEL
# =========================
def extract_clean_model():
    base = ROOT / "final_model_BiGRU"

    # ابحث عن أعمق فولدر فيه saved_model.pb
    candidates = list(base.rglob("saved_model.pb"))

    if not candidates:
        log("No saved_model found")
        return

    best = candidates[-1].parent  # أعمق واحد
    target = ROOT / "models" / "bigru" / "saved_model"

    move(best, target)

    # move useful files
    move(base / "final_model_BiGRU.tflite",
         ROOT / "models/bigru/model.tflite")

    move(base / "model_info.json",
         ROOT / "models/bigru/model_info.json")

    move(base / "sign_to_prediction_index_map.json",
         ROOT / "models/bigru/label_map.json")

# =========================
# MOVE EXPERIMENT
# =========================
def move_experiment():
    src = ROOT / "BiGRU"
    exp = ROOT / "experiments/exp_001"

    move(src / "data", exp / "data")
    move(src / "checkpoints", exp / "checkpoints")

    for f in ["logs", "metrics", "plots", "predictions", "reports"]:
        move(src / f, exp / "outputs" / f)

# =========================
# NORMALIZE FILES
# =========================
def normalize_files(exp):
    rename_map = {
        "BiGRU_test_results.csv": "test_results.csv",
        "BiGRU_training_history.csv": "training_history.csv",
        "BiGRU_test_predictions.csv": "test_predictions.csv"
    }

    for file in exp.rglob("*"):
        if file.name in rename_map:
            move(file, file.parent / rename_map[file.name])

# =========================
# NOTEBOOKS
# =========================
def move_notebooks():
    for nb in ["02-bigru-train.ipynb", "bigru-evaluation.ipynb"]:
        move(ROOT / nb, ROOT / "notebooks" / nb)

# =========================
# ROOT FILES
# =========================
def move_root():
    move(ROOT / "model_comparison_summary.csv",
         ROOT / "comparisons/model_comparison_summary.csv")

    move(ROOT / "final_model_BiGRU.zip",
         ROOT / "archives/final_model_BiGRU.zip")

# =========================
# METADATA
# =========================
def create_metadata():
    meta = {
        "experiment": "exp_001",
        "model": "bigru",
        "status": "completed"
    }

    path = ROOT / "experiments/exp_001/metadata.json"

    if DRY_RUN:
        log(f"[DRY CREATE] {path}")
    else:
        with open(path, "w") as f:
            json.dump(meta, f, indent=4)

# =========================
# CLEAN
# =========================
def cleanup():
    remove(ROOT / "__results___files")
    remove(ROOT / "BiGRU")
    remove(ROOT / "final_model_BiGRU")

# =========================
# MAIN
# =========================
def main():
    create_structure()
    extract_clean_model()
    move_experiment()
    move_notebooks()
    move_root()
    normalize_files(ROOT / "experiments/exp_001")
    create_metadata()
    cleanup()

if __name__ == "__main__":
    main()