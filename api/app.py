from fastapi import FastAPI,HTTPException
from contextlib import asynccontextmanager
from core.models.laptime_model import load_model
from core.models.degradation import degradation_curve,stint_total_time
from core.optimizer import optimize_strategy
from api.schemas import(
    SimulateRequest,SimulateResponse,CompareRequest,CompareResponse,StintResult,
    OptimizeRequest,OptimizeResponse
)

ml_model={}

@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_model["pipeline"]= load_model()
    print("Model Loaded Successfully")
    yield

app = FastAPI(title="RaceEngineerAI",lifespan=lifespan)

@app.get("/health")
def health():
    return{"status":"ok","model_loaded":"pipeline" in ml_model}

@app.post("/simulate",response_model=SimulateResponse)
def simulate(req: SimulateRequest):
    try:
        pipeline = ml_model["pipeline"]
        curve = degradation_curve(
            pipeline,
            track=req.track,
            driver=req.driver,
            compound=req.compound,
            start_lap=req.start_lap,
            stint_length=req.stint_length
        )
        laps = curve["PredictedLapTime"].tolist()
        total_time = round(sum(laps),3)
        return SimulateResponse(laps=laps,total_time=total_time)
    except Exception as e :
        raise HTTPException (status_code=500,detail=str(e))

@app.post("/compare",response_model=CompareResponse)
def compare(req:CompareRequest):
    try:
        pipeline = ml_model["pipeline"]

        curve_a = degradation_curve(pipeline,req.track,req.driver,req.compound_a,1,req.stint_length)
        curve_b = degradation_curve(pipeline,req.track,req.driver,req.compound_b,1,req.stint_length)  

        laps_a = curve_a["PredictedLapTime"].tolist()
        laps_b = curve_b["PredictedLapTime"].tolist()

        total_a = round(sum(laps_a),3)
        total_b = round(sum(laps_b),3)

        winner = req.compound_a if total_a< total_b else req.compound_b

        return CompareResponse(
            compound_a=StintResult(laps=laps_a,total_time=total_a),
            compound_b=StintResult(laps=laps_b,total_time=total_b),
            winner = winner
        )
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.post("/optimize",response_model=OptimizeResponse)
def optimize(req:OptimizeRequest):
    try:
        pipeline =ml_model["pipeline"]
        strategies= optimize_strategy(
            pipeline,
            track=req.track,
            driver =req.driver,
            race_laps=req.race_laps,
            pit_stop_penalty=req.pit_stop_penalty
        )
        return OptimizeResponse(strategies=strategies)
    except Exception as e :
        raise HTTPException(status_code=500,detail=str(e))
    