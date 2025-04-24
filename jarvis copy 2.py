import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime

# Initialize engine
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[132].id)  # Set female voice (change index if necessary)

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
            # Don't speak here; just return empty to keep things quiet
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""


# Jarvis Logic
def run_jarvis():
    speak("Hello, I am Jarvis. How can I assist you today?")
    while True:
        command = take_command()

        if command.strip() == "":
            continue  # Don't say "Listening..." again; just wait for actual speech

        if 'open youtube' in command:
            speak("Opening YouTube...")
            webbrowser.open('https://youtube.com')
            
            
        elif 'how are you' in command:
            speak("I'm good! How are you feeling today?")
            response = take_command()
            if 'good' in response or 'fine' in response:
                speak("I'm glad to hear that! 😊")
            elif 'not good' in response or 'sad' in response:
                speak("Oh no, I hope your day gets better soon.")
 
       
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The time is {time}")

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye sir. Take care.")
            break

        else:
            speak("Sorry, I don't know that yet.")

run_jarvis()
