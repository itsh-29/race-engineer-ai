import pandas as pd
from core.config import ALL_FEATURES,FEATURES_PATH,TARGET,VALID_COMPOUNDS
from core.data.fetch import fetch_all_laps

def build_features(raw_laps):
    df = raw_laps.copy()

    # Add track average lap time BEFORE converting LapTime
    track_avg = df.groupby("Track")["LapTime"].transform(
        lambda x: x.dt.total_seconds().median()
    )
    df["TrackBaseLapTime"] = track_avg

    # keep the necessary fields
    keep_cols = ALL_FEATURES + [TARGET, "LapTime", "RaceId"]
    df = df[[c for c in keep_cols if c in df.columns]]
    df = df.dropna(subset=["LapTime"] + ALL_FEATURES)
    df = df[df["Compound"].isin(VALID_COMPOUNDS)]

    # convert lap time to seconds
    df[TARGET] = df["LapTime"].dt.total_seconds()
    df = df.drop(columns=["LapTime"])

    # Drop outlier laps
    q1 = df.groupby("Track")[TARGET].transform(lambda x: x.quantile(0.25))
    q3 = df.groupby("Track")[TARGET].transform(lambda x: x.quantile(0.75))
    upper_bound = q3 + 3 * (q3 - q1)
    df = df[df[TARGET] <= upper_bound]

    df["Stint"] = df["Stint"].astype(int)
    df["TyreLife"] = df["TyreLife"].astype(int)
    df["LapNumber"] = df["LapNumber"].astype(int)
    df = df.reset_index(drop=True)

    return df

def get_features(force_refresh=False):
    if FEATURES_PATH.exists() and not force_refresh:
        print(f"Loading cached features from {FEATURES_PATH}")
        return pd.read_parquet(FEATURES_PATH)
    raw= fetch_all_laps(force_refresh=force_refresh)
    features = build_features(raw)
    features.to_parquet(FEATURES_PATH)
    print(f"Saved {len(features)} feature rows to {FEATURES_PATH}")
    return features 
