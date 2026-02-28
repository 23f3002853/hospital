# app.py
# Integration Layer for IVR (VXML ↔ ACS/BAP Simulation)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI(title="IVR Integration Layer")

# Enable CORS (Frontend / VXML simulator compatibility)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Data Models
# -----------------------------

class StartCallRequest(BaseModel):
    caller_id: str = "SIMULATOR"

class InputRequest(BaseModel):
    session_id: str
    digit: str

# -----------------------------
# In-Memory Session Store
# -----------------------------

sessions = {}
call_logs = []

# -----------------------------
# IVR Menu Definitions
# -----------------------------

MENUS = {
    "home": {
        "prompt": "Welcome to the IVR system. Press 1 to continue.",
        "options": {
            "1": {"action": "goto", "target": "main"}
        }
    },
    "main": {
        "prompt": "Main Menu. Press 1 for Booking, 2 for Status, 9 to repeat, 0 to go back.",
        "options": {
            "1": {"action": "goto", "target": "booking"},
            "2": {"action": "goto", "target": "status"},
            "9": {"action": "repeat"},
            "0": {"action": "back"}
        }
    },
    "booking": {
        "prompt": "Booking Menu. Press 1 for Domestic, 2 for International, 0 to go back.",
        "options": {
            "1": {"action": "end", "message": "Domestic booking registered."},
            "2": {"action": "end", "message": "International booking registered."},
            "0": {"action": "back"}
        }
    },
    "status": {
        "prompt": "Flight Status Menu. Press 1 to check status, 0 to go back.",
        "options": {
            "1": {"action": "end", "message": "Flight is on time."},
            "0": {"action": "back"}
        }
    }
}

# -----------------------------
# Utility Functions
# -----------------------------

def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def create_session(caller_id):
    session_id = f"CALL_{random.randint(100000, 999999)}"
    sessions[session_id] = {
        "caller_id": caller_id,
        "current_menu": "home",
        "previous_menu": None,
        "history": [],
        "invalid_count": 0,
        "start_time": datetime.now()
    }
    return session_id

def end_session(session_id, reason):
    session = sessions.get(session_id)
    if session:
        call_logs.append({
            "session_id": session_id,
            "caller_id": session["caller_id"],
            "history": session["history"],
            "end_reason": reason,
            "duration_seconds": (datetime.now() - session["start_time"]).seconds
        })
        del sessions[session_id]

# -----------------------------
# API Endpoints (Connectors)
# -----------------------------

@app.post("/ivr/start")
def start_call(request: StartCallRequest):
    session_id = create_session(request.caller_id)
    greeting = get_greeting()

    return {
        "session_id": session_id,
        "menu": "home",
        "prompt": f"{greeting}. {MENUS['home']['prompt']}"
    }

@app.post("/ivr/input")
def process_input(request: InputRequest):
    session = sessions.get(request.session_id)
    if not session:
        return {"error": "Invalid session"}

    current_menu = session["current_menu"]
    menu_def = MENUS.get(current_menu)

    digit = request.digit
    session["history"].append(digit)

    # Invalid input handling
    if digit not in menu_def["options"]:
        session["invalid_count"] += 1

        if session["invalid_count"] >= 3:
            end_session(request.session_id, "Too many invalid inputs")
            return {
                "action": "hangup",
                "message": "Too many invalid attempts. Call ended."
            }

        return {
            "status": "invalid",
            "prompt": f"Invalid input. {menu_def['prompt']}"
        }

    # Reset invalid counter on valid input
    session["invalid_count"] = 0
    option = menu_def["options"][digit]
    action = option["action"]

    # Action handlers
    if action == "goto":
        session["previous_menu"] = current_menu
        session["current_menu"] = option["target"]
        return {
            "menu": option["target"],
            "prompt": MENUS[option["target"]]["prompt"]
        }

    if action == "repeat":
        return {
            "menu": current_menu,
            "prompt": menu_def["prompt"]
        }

    if action == "back":
        prev = session["previous_menu"] or "home"
        session["current_menu"] = prev
        return {
            "menu": prev,
            "prompt": MENUS[prev]["prompt"]
        }

    if action == "end":
        end_session(request.session_id, "Completed normally")
        return {
            "action": "hangup",
            "message": option["message"] + " Thank you for calling."
        }

@app.get("/ivr/logs")
def get_logs():
    return call_logs

@app.get("/")
def health_check():
    return {"status": "IVR Integration Layer Running"}

