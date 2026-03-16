from gtts import gTTS
import pygame
import os
import time

def speak_advanced(text, lang="en"):
    # Pass the detected language code (e.g., 'hi' for Hindi, 'ta' for Tamil)
    tts = gTTS(text=text, lang=lang)
    filename = "response.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()
    # Clean up file to save space
    if os.path.exists(filename):
        os.remove(filename)


def speak(text):
    def play_audio():
        tts = gTTS(text=text, lang="en")
        tts.save("temp.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.quit()
        if os.path.exists("temp.mp3"):
            os.remove("temp.mp3")

    # Run in a separate thread so the main bot can keep "thinking" or logging
    threading.Thread(target=play_audio).start()