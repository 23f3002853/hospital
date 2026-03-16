from fastapi import FastAPI
from pydantic import BaseModel
import requests
import sqlite3
from datetime import datetime

app = FastAPI()

# Data model for the Voice Bot request
class IVRInput(BaseModel):
    session_id: str
    input_value: str

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

# --- NEW: Backend Mapping Function ---
def log_to_db(session_id, user_input, bot_response):
    try:
        conn = sqlite3.connect("hospital_system.db")
        cursor = conn.cursor()
        # Logging every interaction for Context/Audit trail
        cursor.execute(
            "INSERT INTO call_logs (input, intent, timestamp) VALUES (?, ?, ?)",
            (user_input, bot_response, datetime.now())
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Logging Error: {e}")

@app.post("/ivr/input")
async def handle_ivr_logic(data: IVRInput):
    payload = {
        "sender": data.session_id,
        "message": data.input_value
    }

    try:
        # 1. Bridge NLU
        response = requests.post(RASA_URL, json=payload)
        rasa_responses = response.json()

        # 2. Extract Response
        if rasa_responses:
            reply = " ".join([msg.get("text", "") for msg in rasa_responses])
        else:
            reply = "I'm sorry, I didn't catch that. Could you repeat it?"

        # 3. Map to Backend (Tracking State)
        log_to_db(data.session_id, data.input_value, reply)

        return {"prompt": reply, "status": "success"}

    except Exception as e:
        print(f"Error bridging to Rasa: {e}")
        return {"prompt": "The hospital system is currently offline.", "status": "error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)