import shutil
from pathlib import Path

ROOT = Path.cwd()
DRY_RUN = False  # Set to True to see what would be moved without actually moving files

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

# =========================
# ORGANIZE WITHOUT DELETE
# =========================
def organize():
    exp = ROOT / "experiments" / "exp_001"

    # move main folders
    move(exp / "data", ROOT / "data")
    move(exp / "checkpoints", ROOT / "checkpoints")

    outputs = exp / "outputs"

    for folder in ["logs", "metrics", "plots", "predictions", "reports"]:
        move(outputs / folder, ROOT / folder)

    # keep experiments as backup
    move(ROOT / "experiments", ROOT / "experiments_backup")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    organize()