import fastf1
import pandas as pd
from core.config import CACHE_DIR,RAW_LAPS_PATH,SESSIONS 


fastf1.Cache.enable_cache(str(CACHE_DIR))

def fetch_session_laps(year,track,session_type):
    print(f"Loading {year}{track}({session_type})...")
    session = fastf1.get_session(year,track,session_type)
    session.load()

    laps = session.laps.copy()
    laps = laps[laps["PitOutTime"].isna()]
    laps = laps[laps["PitInTime"].isna()]
    laps = laps[laps["TrackStatus"]== "1"]

    laps["Track"] = track
    laps["Year"]  = year
    laps["RaceId"] = f"{year}_{track}"

    return laps;

def fetch_all_laps(force_refresh = False):
    if RAW_LAPS_PATH.exists() and not force_refresh:
        print(f"Loading cached laps from {RAW_LAPS_PATH}")
        return  pd.read_parquet(RAW_LAPS_PATH)

    all_laps =[]
    for year,track,session_type in SESSIONS:
        try:
            laps =fetch_session_laps(year,track,session_type)
            all_laps.append(laps)
        except Exception as e:
            print(f"Skipping {year} {track}:{e}")
    if not all_laps:
        raise RuntimeError("No sessions loaded. Check your internet connection or SESSIONS list in config.py.")
    combined = pd.concat(all_laps, ignore_index=True)
    combined.to_parquet(RAW_LAPS_PATH)
    print(f"Saved{len(combined)} laps to {RAW_LAPS_PATH}")
    return combined
