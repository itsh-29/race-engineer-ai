import pandas as pd
from core.models.laptime_model import predict_lap_time
from core.config import TRACK_BASE_LAPTIMES

def degradation_curve(pipeline,track,driver,compound,start_lap,stint_length):
    rows=[]
    base_time = TRACK_BASE_LAPTIMES.get(track, 90.0)
    for i in range(stint_length):
        lap_number = start_lap+i
        tyre_life =i+1 
        lap_time = predict_lap_time(
            pipeline,track=track,driver=driver,compound=compound,
            lap_number=lap_number,tyre_life=tyre_life,stint=1,track_base_lap_time=base_time
        )
        rows.append({
            "LapNumber":lap_number,
            "TyreLife":tyre_life,
            "PredictedLapTime":lap_time
        })
    return pd.DataFrame(rows)

def stint_total_time(pipeline,track,driver,compound,start_lap,stint_length):
    curve = degradation_curve(pipeline,track,driver,compound,start_lap,stint_length)
    return curve["PredictedLapTime"].sum()


