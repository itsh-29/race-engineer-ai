from fastapi import FastAPI,HTTPException,BackgroundTasks
from contextlib import asynccontextmanager
import uuid
from concurrent.futures import ThreadPoolExecutor
from core.models.laptime_model import load_model
from core.models.degradation import degradation_curve,stint_total_time
from core.optimizer import optimize_strategy
from api.ai import explain_strategy, chat_with_engineer
from api.schemas import(
    SimulateRequest,SimulateResponse,CompareRequest,CompareResponse,StintResult,
    OptimizeRequest,OptimizeResponse,ExplainRequest,ChatRequest
)
from fastapi.middleware.cors import CORSMiddleware

ml_model={}
jobs ={}
executor = ThreadPoolExecutor(max_workers=2)

@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_model["pipeline"]= load_model()
    print("Model Loaded Successfully")
    yield

app = FastAPI(title="RaceEngineerAI",lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://race-engineer-ai.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
@app.post("/optimize")
def optimize(req:OptimizeRequest,background_tasks:BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id]={"status":"running","result":None}
    background_tasks.add_task(run_optimize,job_id,req)
    return {"job_id":job_id}

def run_optimize(job_id:str,req:OptimizeRequest):
    try:
        pipeline= ml_model["pipeline"]
        strategies = optimize_strategy(
            pipeline,
            track=req.track,
            driver=req.driver,
            race_laps=req.race_laps,
            pit_stop_penalty=req.pit_stop_penalty
        )
        jobs[job_id] = {"status":"done","result":strategies}
    except Exception as e :
        jobs[job_id] ={"status":"error","result":str(e)}

@app.get("/status/{job_id}")
def get_status(job_id:str):
    if job_id not in jobs:
        raise HTTPException(status_code=404,detail="Job Not Found")
    return {"status":jobs[job_id]["status"]}

@app.get("/results/{job_id}")
def get_results(job_id:str):
    if job_id not in jobs:
        raise HTTPException(status_code=404,detail="Job Not Found")
    if jobs[job_id]["status"] != "done":
        raise HTTPException(status_code=400,detail="Job Not Ready")
    return OptimizeResponse(strategies=jobs[job_id]["result"])

@app.post("/explain")
def explain(req:ExplainRequest):
    try:
        strategies =[s.model_dump() for s in req.strategies]
        explanation = explain_strategy(req.track,req.driver,strategies)
        return {"explanation":explanation}
    except Exception as e :
        print(f"EXPLAIN ERROR: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    
@app.post("/chat")
def chat(req:ChatRequest):
    try:
        strategies =[s.model_dump() for s in req.strategies]
        response =chat_with_engineer(req.track,req.driver,strategies,req.message)
        return {"response":response}
    except Exception as e :
        raise HTTPException(status_code=500,detail=str(e))