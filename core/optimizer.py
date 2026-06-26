from itertools import permutations
from core.config import VALID_COMPOUNDS
from core.models.degradation import stint_total_time

def generate_strategies(race_laps,min_pit_lap=5):
    strategies=[]

    #1-Stop Strategies
    for c1,c2 in permutations(VALID_COMPOUNDS,2):
        for pit_lap in range(min_pit_lap,race_laps-min_pit_lap):
            strategies.append([
                {"compound":c1,"start_lap":1,"laps":pit_lap},
                {"compound":c2,"start_lap":pit_lap+1,"laps":race_laps-pit_lap}
            ])
    #2-Stop Strategies
    for c1,c2,c3 in permutations(VALID_COMPOUNDS,3):
        for pit1 in range(min_pit_lap,race_laps-min_pit_lap*2):
            for pit2 in range(pit1+min_pit_lap,race_laps-min_pit_lap):
                strategies.append([
                {"compound":c1,"start_lap":1,"laps":pit1},
                {"compound":c2,"start_lap":pit1+1,"laps":pit2-pit1},
                {"compound":c3,"start_lap":pit2+1,"laps":race_laps-pit2}
            ])
    return strategies

def simulate_strategy(pipeline,track,driver,strategy,pit_stop_penalty=25.0):
    total_time =0.0
    for i,stint in enumerate(strategy):
        stint_time = stint_total_time(
            pipeline,
            track=track,
            driver=driver,
            compound=stint["compound"],
            start_lap=stint["start_lap"],
            stint_length=stint["laps"]
        ) 
        total_time += stint_time
        if i < len(strategy)-1:
            total_time += pit_stop_penalty

    return  total_time

def optimize_strategy(pipeline,track,driver,race_laps,pit_stop_penalty=25.0,top_n=5):
    strategies =generate_strategies(race_laps)
    results = []
    for strategy in strategies:
        total_time = simulate_strategy(pipeline,track,driver,strategy,pit_stop_penalty)
        pit_laps = [s["start_lap"]-1 for s in strategy[1:]]
        results.append({
            "stints":[{"compound":s["compound"],"laps":s["laps"]} for s in strategy],
            "pit_laps":pit_laps,
            "total_time":round(total_time,3)
        })
    results.sort(key=lambda x:x["total_time"])
    
    for i,r in enumerate(results[:top_n]):
        r["rank"] = i+1
    
    return results[:top_n]
