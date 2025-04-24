import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import pywhatkit  # 👈 Added
from chatbot_response import chatbot_reply
import re  # add this at the top if not added already

# Initialize engine
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[132].id)   
engine.setProperty('rate', 180)  # Slower for smoothness
engine.setProperty('pitch', 150)
for index, voice in enumerate(voices):
    print(f"{index}: {voice.name} - {voice.languages}")
# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen function
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"✅ You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""

# Play song logic
def play_song(command):
    if "play a song" in command or "play music" in command:
        song = "Shape of You"  # Default fallback song
        speak(f"Playing {song} on YouTube...")
        pywhatkit.playonyt(song)
        return True
    elif "play" in command:
        song = command.replace("play", "").strip()
        if song:
            speak(f"Playing {song} on YouTube...")
            pywhatkit.playonyt(song)
        else:
            speak("Please tell me the name of the song you want to play.")
        return True
    return False

# Jarvis logic
def run_jarvis():
    speak("Hello, I am Miku. How can I assist you today?")
    while True:
        command = take_command()

        if command.strip() == "":
            continue

        if play_song(command):  # 👈 Handles music requests
            continue
        if "open" in command:
                    url_match = re.search(r"(https?://)?(www\.[a-zA-Z0-9\-]+\.[a-z]{2,})", command)
                    if url_match:
                        url = url_match.group()
                        if not url.startswith("http"):
                            url = "https://" + url
                        speak(f"Opening {url}")
                        webbrowser.open(url)
                        continue
        if 'open youtube' in command:
            speak("Opening YouTube...")
            webbrowser.open('https://youtube.com')

        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The time is {time}")

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye sir. Take care.")
            break

        else:
            ai_response = chatbot_reply(command)
            speak(ai_response)

run_jarvis()
