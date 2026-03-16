from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionBookAppointment(Action):
    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Your appointment request has been noted. Our staff will contact you shortly.")
        return []

class ActionCheckDoctor(Action):
    def name(self) -> Text:
        return "action_check_doctor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="The doctor is available today from 10 AM to 4 PM.")
        return []

class ActionEmergencyResponse(Action):
    def name(self) -> Text:
        return "action_emergency_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Emergency services are being notified. Please stay calm. Call 108 immediately.")
        return []