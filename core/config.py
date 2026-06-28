import fastf1
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent



def get_all_sessions(years=[2023,2024]):
    sessions =[]
    for year in years:
        schedule = fastf1.get_event_schedule(year,include_testing=False)
        for _,event in schedule.iterrows():
            sessions.append((year,event["EventName"],"R"))
        return sessions

SESSIONS =get_all_sessions()

TRACK_BASE_LAPTIMES = {
    "Monaco": 75.0,
    "Silverstone": 90.0,
    "Monza": 82.0,
    "Bahrain": 93.0,
    "Saudi Arabia": 90.0,
    "Australia": 85.0,
    "Japan": 92.0,
    "China": 95.0,
    "Miami": 90.0,
    "Canada": 75.0,
    "Spain": 82.0,
    "Austria": 67.0,
    "Hungary": 80.0,
    "Belgium": 105.0,
    "Netherlands": 73.0,
    "Azerbaijan": 105.0,
    "Singapore": 100.0,
    "United States": 98.0,
    "Mexico City": 79.0,
    "São Paulo": 71.0,
    "Las Vegas": 96.0,
    "Qatar": 84.0,
    "Abu Dhabi": 87.0,
}


CACHE_DIR = ROOT_DIR / "cache"
DATA_DIR = ROOT_DIR / "data"
MODEL_DIR = ROOT_DIR / "models_store"

RAW_LAPS_PATH = DATA_DIR / "raw_laps.parquet"
FEATURES_PATH = DATA_DIR / "features.parquet"
MODEL_PATH = MODEL_DIR / "laptime_model.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"

for d in (CACHE_DIR, DATA_DIR, MODEL_DIR):
    d.mkdir(parents=True, exist_ok=True)

NUMERIC_FEATURES = ["LapNumber", "TyreLife", "Stint", "TrackBaseLapTime"]
CATEGORICAL_FEATURES = ["Track", "Driver", "Compound"]
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "LapTimeSeconds"
VALID_COMPOUNDS = ["SOFT", "MEDIUM", "HARD"]