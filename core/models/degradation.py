import pandas as pd
from core.models.laptime_model import predict_lap_time

def degradation_curve(pipeline,track,driver,compound,start_lap,stint_length):
    rows=[]
    for i in range(stint_length):
        lap_number = start_lap+i
        tyre_life =i+1 
        lap_time = predict_lap_time(
            pipeline,track=track,driver=driver,compound=compound,
            lap_number=lap_number,tyre_life=tyre_life,stint=1
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


