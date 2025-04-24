import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import pywhatkit  # Added for playing songs on YouTube
from chatbot_response import chatbot_reply
import re  # Regular expression for URL matching
import psutil  # To check system health

# Initialize the speech engine
engine = pyttsx3.init()

# Get available voices and set preferences
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[132].id)  # You can change this to different indices for different voices
engine.setProperty('rate', 180)  # Adjust speech rate for smoothness
engine.setProperty('pitch', 150)  # Adjust pitch for a nicer tone

# Print available voices for reference
for index, voice in enumerate(voices):
    print(f"{index}: {voice.name} - {voice.languages}")

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()




# Function to listen to the user's command
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

# Function to handle playing a song
def play_song(command):
    if "play a song" in command or "play music" in command:
        song = "Shape of You"  # Default song if nothing specified
        speak(f"Playing {song} on YouTube...")
        pywhatkit.playonyt(song)  # Playing the default song
        return True
    elif "play" in command:
        song = command.replace("play", "").strip()  # Extract song name after "play"
        if song:
            speak(f"Playing {song} on YouTube...")
            pywhatkit.playonyt(song)  # Playing the song specified
        else:
            speak("Please tell me the name of the song you want to play.")  # If no song name is given
        return True
    return False

# Function to check system health (CPU, memory, disk)
def check_system_health():
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage
    memory_info = psutil.virtual_memory()  # Memory usage
    disk_info = psutil.disk_usage('/')  # Disk space usage

    # Prepare a health report
    health_report = f"CPU usage is at {cpu_usage}%, Memory usage is at {memory_info.percent}%, Disk usage is at {disk_info.percent}%."
    
    # Speak the health report
    speak(f"System health check: {health_report}")

# Main function to run the assistant
def run_jarvis():
    speak("Hello, I am Miku. How can I assist you today?")  # Introduce the assistant
    while True:
        command = take_command()

        # Skip empty commands
        if command.strip() == "":
            continue

        # Check if the user wants to play a song
        if play_song(command):  # If music is requested
            continue

        # Check for URL opening requests
        if "open" in command:
            url_match = re.search(r"(https?://)?(www\.[a-zA-Z0-9\-]+\.[a-z]{2,})", command)
            if url_match:
                url = url_match.group()
                if not url.startswith("http"):  # Ensure the URL starts with "https://"
                    url = "https://" + url
                speak(f"Opening {url}")
                webbrowser.open(url)  # Open the URL in the web browser
                continue

        # Specific command to open YouTube
        if 'open youtube' in command:
            speak("Opening YouTube...")
            webbrowser.open('https://youtube.com')

        # Check for the time
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')  # Get the current time
            speak(f"The time is {time}")

        # Check system health command
        elif 'check system health' in command or 'system health' in command:
            check_system_health()  # Call the system health check function

        # Exit the assistant
        elif 'exit' in command or 'stop' in command:
            speak("Goodbye sir. Take care.")
            break

        # Chatbot response for any other command
        else:
            ai_response = chatbot_reply(command)  # Assuming you have the chatbot's response function
            speak(ai_response)

# Run the assistant
run_jarvis()
