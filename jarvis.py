import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import pywhatkit  # For playing songs on YouTube
from chatbot_response import chatbot_reply
import re  # For URL matching
import psutil  # For system health check
import time
import threading
import sys
import os
import subprocess
import pywhatkit as kit
import pyautogui
 
from datetime import datetime, timedelta

# Initialize the speech engine
engine = pyttsx3.init()

# Get available voices and set preferences
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[132].id)  # You can change this index
engine.setProperty('rate', 180)
engine.setProperty('pitch', 150)

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Spinner-style loader animation
def show_spinner(stop_event):
    spinner = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r🎤 Listening... {spinner[idx % len(spinner)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1

# Function to listen to the user's command
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=show_spinner, args=(stop_event,))
        spinner_thread.start()

        try:
            audio = r.listen(source)
            stop_event.set()
            spinner_thread.join()
            print("\n✅ Processing your voice...")

            command = r.recognize_google(audio)
            print(f"✅ You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            stop_event.set()
            spinner_thread.join()
            print("\n❌ Sorry, I couldn't understand.")
            return ""
        except sr.RequestError:
            stop_event.set()
            spinner_thread.join()
            speak("Sorry, my speech service is down.")
            return ""

# Function to handle playing a song
def play_song(command):
    if "play a song" in command or "play music" in command:
        song = "Shape of You"
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

# Function to check system health
def check_system_health():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    health_report = f"CPU usage is at {cpu_usage}%, Memory usage is at {memory_info.percent}%, Disk usage is at {disk_info.percent}%."
    speak(f"System health check: {health_report}")


def open_whatsapp():
    try:
          webbrowser.open('https://web.whatsapp.com')  # Opens WhatsApp Web
    except Exception as e:
        print("Error opening WhatsApp:", e)

def ask_for_message():
    speak("What message would you like to send?")
    message = take_command()  # Capture the user's message
    return message

def send_whatsapp_message(command):
    # Extract the name from the command
    match = re.search(r"send message to (\w+)", command)
    
    if match:
        name = match.group(1)
        
        # Define phone numbers for contacts
        contacts = {
            "nima": "+918328708365",  # Remove spaces from phone number
            "neema": "+918328708365", 
            "priya": "+919830794080",
            "Hehe": "Hehe 😁"
            # Add more contacts here
        }
        
        # Convert name to lowercase for case-insensitive comparison
        if name.lower() in contacts:
            phone_number = contacts[name.lower()]
            
            # Ask for the message
            speak(f"What message would you like to send to {name}?")
            message = take_command()
            
            if message:
                try:
                    # Open WhatsApp Web with the contact directly (no need to search)
                    # Format: remove all spaces and special characters from phone number
                    formatted_number = re.sub(r'[^0-9]', '', phone_number)
                    whatsapp_url = f"https://web.whatsapp.com/send?phone={formatted_number}&text={message}"
                    
                    speak(f"Opening WhatsApp and preparing to send message to {name}.")
                    webbrowser.open(whatsapp_url)
                    
                    # Wait for WhatsApp Web to load - adjust this time based on your internet speed
                    # 10 seconds is usually enough with good internet
                    speak("Waiting for WhatsApp to load...")
                    time.sleep(10)  # Reduced to 10 seconds
                    
                    # Press Enter to send the message
                    pyautogui.press('enter')
                    speak(f"Message sent to {name} successfully.")
                    return True
                except Exception as e:
                    print(f"Error sending message: {str(e)}")
                    speak(f"I encountered an error when sending the message.")
                    return False
            else:
                speak("I didn't hear a message. Please try again.")
                return False
        else:
            speak(f"I don't have {name}'s contact information in my database.")
            return False
    return False


def send_whatsapp_group_message(command):
    # Extract group name from command
    match = re.search(r"send message to group (\w+)", command)
    
    if match:
        group_name = match.group(1)
        
        # Ask for the message
        speak(f"What message would you like to send to the {group_name} group?")
        message = take_command()
        
        if message:
            try:
                # Open WhatsApp Web
                speak(f"Opening WhatsApp. Please navigate to the {group_name} group manually.")
                webbrowser.open("https://web.whatsapp.com")
                
                # Wait for user to navigate to the group
                speak("I'll wait 15 seconds for you to navigate to the group chat.")
                time.sleep(15)
                
                # Type and send the message
                pyautogui.typewrite(message)
                time.sleep(1)
                pyautogui.press('enter')
                speak(f"Message sent to {group_name} group successfully.")
                return True
            except Exception as e:
                print(f"Error sending message: {str(e)}")
                speak(f"I encountered an error when sending the message.")
                return False
        else:
            speak("I didn't hear a message. Please try again.")
            return False
    return False
# Alternative approach using pyautogui for more direct control
 
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
        # Check if the user wants to open WhatsApp
            if "open whatsapp" in command:
                speak("Opening WhatsApp...")
                open_whatsapp()  # Launch WhatsApp
                continue

        # Check if the user wants to send a message
        if "send message" in command:
            if send_whatsapp_message(command):
                continue
       
        # Specific command to open YouTube
        if 'open youtube' in command:
            speak("Opening YouTube...")
            webbrowser.open('https://youtube.com')

        # Check for the time
        elif 'time' in command:
            time = datetime.now().strftime('%I:%M %p')  # Get the current time
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
