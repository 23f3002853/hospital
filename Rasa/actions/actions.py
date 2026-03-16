from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sqlite3

# Initialize Database once
def init_db():
    conn = sqlite3.connect("hospital_system.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS appointments (dept TEXT, doc TEXT, time TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS call_logs (input TEXT, intent TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

init_db()

class ActionConfirmAppointment(Action):
    
    def name(self) -> Text:
        return "action_confirm_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # 1. Tracking the State: Check what we already know from the NLU
        dept = tracker.get_slot("department")
        doc = tracker.get_slot("doctor")
        time = tracker.get_slot("time")

        # 2. Context-Aware Follow-up (Interactive Content)
        # If slots are missing, ask specifically for them
        if not dept:
            dispatcher.utter_message(text="Which department would you like to visit?")
            return []
        
        if not doc:
            dispatcher.utter_message(text=f"Do you have a preferred doctor in the {dept} department?")
            return []
            
        if not time:
            dispatcher.utter_message(text=f"When would you like to schedule your appointment with {doc}?")
            return []

        # 3. Bridge to Backend (Database Insertion)
        try:
            conn = sqlite3.connect("hospital_system.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO appointments (dept, doc, time) VALUES (?,?,?)", (dept, doc, time))
            
            # Log the successful transaction in call_logs
            user_input = tracker.latest_message.get("text")
            cursor.execute("INSERT INTO call_logs (input, intent) VALUES (?,?)", (user_input, "book_appointment"))
            
            conn.commit()
            conn.close()
            
            dispatcher.utter_message(text=f"Confirmed! Your appointment with {doc} in {dept} is scheduled for {time}.")
            
            # Reset slots so the user can book another appointment if needed
            return [SlotSet("department", None), SlotSet("doctor", None), SlotSet("time", None)]
            
        except Exception as e:
            print(f"Database Error: {e}")
            dispatcher.utter_message(text="I'm sorry, I'm having trouble saving your appointment right now.")
            return []