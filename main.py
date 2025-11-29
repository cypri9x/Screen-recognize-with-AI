import google.generativeai as genai
import pyautogui
from PIL import Image, ImageDraw
import time
import keyboard
import pyttsx3
import threading

API_KEY = "API KEY"

genai.configure(api_key=API_KEY)

running = True 

def capture_screen():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    return screenshot

def process_image():
    prompt = "aPENAS responda as perguntas do discord a alternativa rapido "
    try:
        img = Image.open("screenshot.png")

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([prompt, img], stream=True)

        result = []
        for chunk in response:
            for part in chunk.parts:
                result.append(part.text)
        
        response_text = " ".join(result)
        speak_text(response_text)

    except Exception as e:
        print(f"Error processing image: {e}")

def speak_text(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')  
    engine.setProperty('rate', rate + 50)  

    voices = engine.getProperty('voices')
    voice_found = False
    for voice in voices:
        if "brazil" in voice.id.lower():
            engine.setProperty('voice', voice.id)
            voice_found = True
            break
   
    if not voice_found:
        for voice in voices:
            if "male" in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
        else:
            engine.setProperty('voice', voices[0].id) 

    engine.say(text)
    engine.runAndWait()

def start_program():
    while running:
        if keyboard.is_pressed('p'):
            capture_screen()
            process_image()
            time.sleep(1)  

start_program()

