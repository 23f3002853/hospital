import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    # Higher threshold = less sensitive to background static
    recognizer.energy_threshold = 400 
    
    with sr.Microphone() as source:
        print("Adjusting for noise... please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        print("Speak now...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            # Use 'en-IN' to better capture Indian accents/Hindi mix
            text = recognizer.recognize_google(audio, language="en-IN")
            return text
        except Exception:
            return ""