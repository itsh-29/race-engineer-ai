from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ml_models.strategy_simulator import optimize_strategy

app = FastAPI()

templates = Jinja2Templates(directory="api/templates")

class StrategyRequest(BaseModel):
    track: str
    driver: str
    laps: int

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/optimize")
def optimize(req: StrategyRequest):

    best_strategy, best_time, _ = optimize_strategy(
        req.track,
        req.driver,
        req.laps
    )

    return {
        "start_tire": best_strategy[0],
        "pit_lap": best_strategy[2],
        "next_tire": best_strategy[1],
        "estimated_time": round(best_time, 2)
    }

