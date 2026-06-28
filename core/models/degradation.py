import pandas as pd
from core.models.laptime_model import predict_lap_time
from core.config import TRACK_BASE_LAPTIMES

def degradation_curve(pipeline,track,driver,compound,start_lap,stint_length):
    
    
    base_time = TRACK_BASE_LAPTIMES.get(track, 90.0)
    #building all the laps at once instead of one by one
    rows = pd.DataFrame([{
        "Track":track,
        "Driver":driver,
        "Compound":compound,
        "LapNumber":start_lap+1,
        "Tyre_life":i+1,
        "Stint":1,
        "TrackBaseLapTime":base_time
    }] for i in range(stint_length)) 
    predictions = pipeline.predict(rows)
   
    return pd.DataFrame({
            "LapNumber":rows["LapNumber"],
            "TyreLife": rows["TyreLife"],
            "PredictedLapTime":predictions
        })

def stint_total_time(pipeline,track,driver,compound,start_lap,stint_length):
    curve = degradation_curve(pipeline,track,driver,compound,start_lap,stint_length)
    return curve["PredictedLapTime"].sum()


