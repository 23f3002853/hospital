from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI(
    title="Conversational IVR Integration Layer",
    description="Middleware connecting Legacy VXML IVR with Conversational AI",
    version="1.0"
)

# Enable CORS for frontend / simulator
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# DATA MODELS
# -------------------------

class StartCallRequest(BaseModel):
    caller_id: str = "WEB_SIMULATOR"

class UserInputRequest(BaseModel):
    session_id: str
    input_value: str   # DTMF digit or text
    source: str = "VXML"  # Simulates legacy system

# -------------------------
# IN-MEMORY SESSION STORE
# -------------------------

sessions = {}

# -------------------------
# IVR MENU DEFINITIONS
# (Legacy VXML logic mapped)
# -------------------------

IVR_FLOW = {
    "HOME": {
        "prompt": "Welcome to Hospital Management IVR. Press 1 for Appointments, 2 for Billing, 3 for Emergency.",
        "options": {
            "1": "APPOINTMENTS",
            "2": "BILLING",
            "3": "EMERGENCY"
        }
    },
    "APPOINTMENTS": {
        "prompt": "Press 1 to book appointment. Press 2 to check status. Press 0 to go back.",
        "options": {
            "1": "END_BOOK",
            "2": "END_STATUS",
            "0": "HOME"
        }
    },
    "BILLING": {
        "prompt": "Press 1 for outstanding bills. Press 0 to return to main menu.",
        "options": {
            "1": "END_BILL",
            "0": "HOME"
        }
    },
    "EMERGENCY": {
        "prompt": "Please hold. Connecting you to emergency services.",
        "options": {}
    }
}

# -------------------------
# START CALL (VXML ENTRY)
# -------------------------

@app.post("/ivr/start")
def start_call(request: StartCallRequest):
    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "caller": request.caller_id,
        "current_state": "HOME",
        "start_time": datetime.now(),
        "history": []
    }

    return {
        "session_id": session_id,
        "prompt": IVR_FLOW["HOME"]["prompt"],
        "state": "HOME",
        "integration_note": "Legacy VXML entry mapped to Conversational Flow"
    }

# -------------------------
# PROCESS USER INPUT
# -------------------------

@app.post("/ivr/input")
def process_input(data: UserInputRequest):

    session = sessions.get(data.session_id)

    if not session:
        return {"error": "Invalid session"}

    current_state = session["current_state"]
    session["history"].append(data.input_value)

    state_config = IVR_FLOW.get(current_state)

    # Invalid input handling
    if data.input_value not in state_config["options"]:
        return {
            "prompt": state_config["prompt"],
            "status": "INVALID_INPUT"
        }

    next_state = state_config["options"][data.input_value]

    # End states simulate call completion
    if next_state.startswith("END"):
        del sessions[data.session_id]
        return {
            "action": "HANGUP",
            "message": f"Request processed successfully ({next_state}). Thank you!"
        }

    # Continue IVR flow
    session["current_state"] = next_state

    return {
        "prompt": IVR_FLOW[next_state]["prompt"],
        "state": next_state,
        "real_time": "YES",
        "integration": "VXML → API → Conversational Engine"
    }

# -------------------------
# HEALTH CHECK
# -------------------------

@app.get("/")
def health():
    return {
        "status": "Integration Layer Running",
        "active_sessions": len(sessions)
    }
