from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

SESSIONS = [
    (2023, "Monaco", "R"),
    (2023, "Silverstone", "R"),
    (2023, "Monza", "R"),
    (2024, "Monaco", "R"),
    (2024, "Silverstone", "R"),
    (2024, "Monza", "R"),
]

CACHE_DIR = ROOT_DIR / "cache"
DATA_DIR = ROOT_DIR / "data"
MODEL_DIR = ROOT_DIR / "models_store"

RAW_LAPS_PATH = DATA_DIR / "raw_laps.parquet"
FEATURES_PATH = DATA_DIR / "features.parquet"
MODEL_PATH = MODEL_DIR / "laptime_model.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"

for d in (CACHE_DIR, DATA_DIR, MODEL_DIR):
    d.mkdir(parents=True, exist_ok=True)

NUMERIC_FEATURES = ["LapNumber", "TyreLife", "Stint"]
CATEGORICAL_FEATURES = ["Track", "Driver", "Compound"]
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "LapTimeSeconds"
VALID_COMPOUNDS = ["SOFT", "MEDIUM", "HARD"]