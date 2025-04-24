import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime

# Initialize engine
engine = pyttsx3.init()

# Set voice to female (adjust index based on your system)
voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    print(f"{index}: {voice.name} ({voice.languages})")

engine.setProperty('voice', voices[132].id)  # Set female voice (change index if necessary)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio).lower()  # Convert to lowercase for case-insensitive comparison
            print(f"✅ You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
            return ""

def respond_to_command(command):
    if 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {time}")

    elif 'i love u' in command:
        speak("I love you too!")
      
    elif 'stop' in command or 'exit' in command:
        speak("Goodbye")
        exit()

    else:
        speak("Sorry, I don't understand that yet.")

def run_jarvis():
    speak("Miku is listening... say 'miku' to wake me up.")
    while True:
        text = listen()
        if "miku" in text:
            speak("Yes, I'm here. How can I help?")
            command = listen()
            respond_to_command(command)
        else:
            print("🔕 Wake word not detected. Sleeping...")

run_jarvis()
