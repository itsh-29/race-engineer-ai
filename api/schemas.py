from pydantic import BaseModel
from typing import List

class SimulateRequest(BaseModel):
    track:str
    driver:str
    compound: str
    stint_length:int 
    start_lap: int=1

class SimulateResponse(BaseModel):
    laps:List[float]
    total_time:float

class CompareRequest(BaseModel):
    track:str
    driver: str
    compound_a:str
    compound_b :str 
    stint_length: int

class StintResult(BaseModel):
    laps:List[float]
    total_time:float

class CompareResponse(BaseModel):
    compound_a:StintResult
    compound_b:StintResult
    winner:str

class OptimizeRequest(BaseModel):
    track:str
    driver:str
    race_laps:int
    pit_stop_penalty: float = 25.0

class StintInfo(BaseModel):
    compound: str 
    laps: int

class StrategyResult(BaseModel):
    rank:int
    stints:List[StintInfo]
    pit_laps:List[int]
    total_time :float

class OptimizeResponse(BaseModel):
    strategies: List[StrategyResult]

