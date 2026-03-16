from speech_to_text import listen
from text_to_speech import speak_advanced
from deep_translator import GoogleTranslator
from langdetect import detect
import requests

GATEWAY_URL = "http://localhost:8000/ivr/input"

def run_multilingual_bot():
    while True:
        # 1. Listen (Speech to Text)
        user_input = listen() 
        if not user_input or user_input.strip() == "":
            continue

        # 2. Language Detection with Filter
        try:
            user_lang = detect(user_input)
            # If it detects a language we don't support, default to English
            if user_lang not in ['en', 'hi', 'te', 'ta', 'kn', 'ml']:
                user_lang = 'en'
            print(f"Detected Language: {user_lang}")
        except:
            user_lang = 'en'
            
        # 3. Translate to English for Rasa
        if user_lang != 'en':
            translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)
        else:
            translated_input = user_input

        # 4. Send Translated Input
        payload = {"session_id": "user_123", "input_value": translated_input}
        try:
            response = requests.post(GATEWAY_URL, json=payload)
            english_bot_response = response.json().get("prompt", "")
        except Exception as e:
            print(f"Connection Error: {e}")
            english_bot_response = "I am having trouble connecting to the server."

        # --- GUARD CLAUSE: Check if Rasa returned an empty string ---
        if not english_bot_response or english_bot_response.strip() == "":
            english_bot_response = "I'm sorry, I didn't catch that. Could you repeat it?"

        # 5. Translate Bot Response back
        if user_lang != 'en':
            final_response = GoogleTranslator(source='en', target=user_lang).translate(english_bot_response)
        else:
            final_response = english_bot_response

        # 6. Advanced TTS (Output in native language)
        # Final check before sending to gTTS
        if final_response and final_response.strip() != "":
            print(f"Bot ({user_lang}): {final_response}")
            speak_advanced(final_response, lang=user_lang)
        else:
            print("Warning: final_response was empty. Skipping TTS.")

if __name__ == "__main__":
    run_multilingual_bot()