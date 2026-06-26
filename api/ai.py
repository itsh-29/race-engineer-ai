import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def explain_strategy(track, driver, strategies):
    best = strategies[0]
    stints_text = " -> ".join(
        [f"{s['compound']} ({s['laps']} laps)" for s in best["stints"]]
    )
    pit_laps_text = ", ".join([f"Lap {p}" for p in best["pit_laps"]])

    prompt = f"""
    You are an expert Formula 1 race engineer. Explain the following optimal race strategy in 5-6 sentences, like you are briefing your driver before the race. Be specific, technical, and confident.
    Track: {track}
    Driver: {driver}
    Best Strategy: {stints_text}
    Pit Stop Laps: {pit_laps_text}
    Estimated Total Race Time: {best["total_time"]}s

    Also briefly mention why this is better than a different strategy approach.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def chat_with_engineer(track, driver, strategies, user_message):
    best = strategies[0]
    stints_text = " -> ".join(
        [f"{s['compound']} ({s['laps']} laps)" for s in best["stints"]]
    )

    prompt = f"""
    You are an expert Formula 1 race engineer AI assistant. You have just completed a strategy analysis for {driver} at {track}.
    Optimal strategy found: {stints_text}
    Pit laps: {", ".join([f"Lap {p}" for p in best["pit_laps"]])}
    Total estimated time: {best["total_time"]}s

    The driver is asking you: {user_message}

    Answer as a knowledgeable F1 race engineer. Be concise, technical and helpful. Keep your answer under 5 sentences.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text