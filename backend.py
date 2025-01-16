import pyttsx3
import speech_recognition as sr
import datetime
import os
import requests
import wikipedia
import webbrowser
import pywhatkit as kit
import pygetwindow as gw
import aiprocess as ap
import AppOpener
import gemini_ai
import time
import dotenv
import main 
import io
import sys
import psutil
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER


commands = ["open", "shutdown", "ip address of my device", "minimise window","close window","maximise window","go to","search on google","search on wikipedia",
            "current temperature","send message","ai mode","sleep","current date","restart","play video on youtube","help","close","send message","battery","current time","Incomplete","mute","unmute"]


def wiki(query):
    
    try: 
        result=wikipedia.summary(query,sentences=2)
        print(f"According to wikipedia {result} for more information go to wikipedia.com")
        return f"According to wikipedia {result} for more information go to wikipedia.com"
        
    except Exception as e:
        return f"Something went wrong {e}"
    

def google_search(query):
    try:
        kit.search(query)
        return f"{query} Searching from google"
    except Exception as e:
        return f"Something went wrong {e}"


def ytvideo(video_name):
    try:
        kit.playonyt(video_name)
        return f"{video_name} is going to play on YouTube"
    except Exception as e:
        return f"Something went wrong {e}"


dotenv.load_dotenv()
def temperature(city):
    
    api_key = os.getenv("WEATHER_API_KEY")  # replace with your actual WeatherAPI key
    base_url = "http://api.weatherapi.com/v1/current.json"
    
    complete_url = f"{base_url}?key={api_key}&q={city}"
    response = requests.get(complete_url)
    weather_data = response.json()
    
    if "error" not in weather_data:
        # Extract temperature
        temp_celsius = weather_data['current']['temp_c']
        condition = weather_data['current']['condition']['text']
        
        return f"The temperature in {city} is {temp_celsius}°C with {condition}."
    else:
        return "Please Enter valid city name"


def send_message(message):
    return "whatsapp",message
#     number = CustomInputBox.show_input_dialog("Please provide the phone number to which I should send messages")
#     while (len(number)<=9):
#         number = CustomInputBox.show_input_dialog(f"The provided phone number have only {len(number)} digits Please Enter again")
    
#     # speak("This process may take a few seconds and during this process i can't do any other work")
#     now = datetime.datetime.now()
#     future_time = now + datetime.timedelta(minutes=2)
#     time_hour = future_time.hour
#     time_minute = future_time.minute

#     country_code="+91"
#     number=f"{country_code}{number}"
#     kit.sendwhatmsg(number, message, time_hour, time_minute)

def incomplete_command(complete_command):
    return f"The command you provide is incomplete command, the complete {complete_command}"

def open_apps(app_name):
    
    try:
        AppOpener.open(app_name,match_closest=True)
        return f"{app_name} is Opened"
    except Exception as e:
        return f"Something went wrong {e}"
        
        
        
def mute():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)
        return "System muted!"
    except Exception as e:
        return f"Something went wrong {e}"


def unmute():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Unmute the system
        volume.SetMute(0, None)
        return "System unmuted!"
    except Exception as e:
        return f"Something went wrong {e}"

def process_airesponse(response):
    for command in commands:
        if response.startswith(command): 
            param = response[len(command):].strip()  
            return command,param
    return None,None

def restart():
    try:
        os.system("shutdown /r /t 0")
        return "Restart canceled"
    except Exception as e:
        return f"Something Went wrong {e}"
    
def battery():
    try:
        battery = psutil.sensors_battery()
        if battery is not None:
            percentage = battery.percent
            plugged = battery.power_plugged
            if plugged:
                status="is"
            else:
                status="is Not"
            return f"Your current battery percentage is {percentage}% and currently charger {status} Plugged In"
        else:
            return "Battery not found" 
    except Exception as e:
        return f"Something went wrong {e}"
    

def help_function():
    help_text = (
        "Welcome to the Command Assistant!, My name is Nova, Here are some commands you can use:\n\n"
        "1. **Go to <website name>**\n"
        "   - Example: 'Go to amazon' or 'Go to google'\n"
        "   - Opens the website in your browser. The assistant will append '.com' to the website name if not specified.\n\n"
        
        "2. **Search on Google <query>**\n"
        "   - Example: 'Search on Google Python tutorials'\n"
        "   - Performs a Google search with the specified query.\n\n"
        
        "3. **Open <app/system tool>**\n"
        "   - Example: 'Open calculator' or 'Open notepad'\n"
        "   - Opens the specified application or system tool.\n\n"
        
        "4. **IP address of my device**\n"
        "   - Example: 'IP address of my device'\n"
        "   - Provides the IP address of your device.\n\n"
        
        "5. **Search on Wikipedia <topic>**\n"
        "   - Example: 'Search on Wikipedia Python programming'\n"
        "   - Searches Wikipedia for the specified topic and reads a summary.\n\n"
        
        "6. **Send message**\n"
        "   - Example: 'Send message'\n"
        "   - Prompts you to provide a phone number and a message to send via WhatsApp.\n\n"
        
        "7. **Current temperature <city_name>**\n"
        "   - Example: 'Current temperature in New York'\n"
        "   - Provides the current temperature for the specified city.\n\n"
        
        "8. **Play video on YouTube <video_name>**\n"
        "   - Example: 'Play video on YouTube Python tutorial'\n"
        "   - Searches for and plays the specified video on YouTube.\n\n"
        
        "9. **Current time**\n"
        "   - Example: 'Current time'\n"
        "   - Provides the current time.\n\n"
        
        "10. **AI mode <query>**\n"
        "    - Example: 'AI mode What is the weather like?'\n"
        "    - Interacts with the AI model to process your query in AI mode.\n\n"
        
        "11. **Shutdown**\n"
        "    - Example: 'Shutdown'\n"
        "    - Shuts down the computer.\n\n"
        
        "12. **Restart**\n"
        "    - Example: 'Restart'\n"
        "    - Restarts the computer.\n\n"
        
        "13. **Sleep**\n"
        "    - Example: 'Sleep'\n"
        "    - Puts the computer into sleep mode.\n\n"
        
        "14. **Minimise window**\n"
        "    - Example: 'Minimise window'\n"
        "    - Minimizes the currently active window.\n\n"
        
        "15. **Maximise window**\n"
        "    - Example: 'Maximise window'\n"
        "    - Maximizes the currently active window.\n\n"
        
        "16. **Close window**\n"
        "    - Example: 'Close window'\n"
        "    - Closes the currently active window.\n\n"
        
        # "17. **No thanks exit**\n"
        # "    - Example: 'No thanks exit'\n"
        # "    - Exits the assistant.\n\n"
        
        "If you need help with a specific command or have any questions, just ask!"
    )
    return help_text
    
          
  

def sleep():
    try:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Sleep canceled"
    except Exception as e:
        return f"Something Went wrong {e}"
        
        
def ip_address():
    
    try:
        ip=requests.get("https://api.ipify.org").text
        return f"Your IP Address is {ip}"
    except Exception as e:
        return f"Something went wrong {e}"

def minimize():
    
    try:
        window = gw.getActiveWindow()
        if window:
            window.minimize()
            return "current window is minimized"
        else:
            return "Current window can't recognize"
    except Exception as e:
        return f"Something went wrong {e}"
        
        
def maximize():
    
    try:
        window = gw.getActiveWindow()
        if window:
            window.maximize()
            return "Current Window is Maximized"
        else:
            return "Current window can't recognize"
    except Exception as e:
        return f"Something went wrong {e}"
        
              
def closewindow():
    
    try:
        window = gw.getActiveWindow()
        if window:
            window.close()
            return "Current Window is Closed"
        else:
            return "Current can't recognize"
    except Exception as e:
        return f"Something went wrong {e}"
        
def shutdown():
    try:
        os.system("shutdown /s /t 0")
        return "Shutdown Cancelled"
    except Exception as e:
        return f"Something Went wrong {e}"

def open_website(web_name):
    try:
        webbrowser.open(f"http://{web_name}")
        return f"Opening {web_name} in your browser..."
    except Exception as e:
        return f"Failed to open {web_name}"
        
        
def close_apps(app_name):
    try:
        captured_output = io.StringIO()
        sys.stdout = captured_output
        AppOpener.close(app_name)
        sys.stdout = sys.__stdout__
        result = captured_output.getvalue().strip()
        
        if "not running" in result:
            return "Sorry I can't close the app due to security concern and permission issues, If the app you want to close is your current window, then try again and say close the current window"
    except Exception as e:
        return f"Something went wrong {e}"

def ai_mode(query):
    result=gemini_ai.aispeechmode(query)
    return result

def current_time():
    time = datetime.datetime.now().strftime("%I:%M %p") 
    return f"The current time is {time}"

   
def current_date():
    date=date=datetime.datetime.now().strftime("%B %d, %Y")
    return f"Today's date is {date}"

def default_fucntion(query):
    return query

command_actions={
    "open":open_apps,
    "search on wikipedia":wiki,
    "sleep":sleep,
    "minimise window":minimize,
    "maximise window":maximize,
    "close window":closewindow,
    "go to":open_website,
    "search on google":google_search,
    "ip address of my device":ip_address,
    "play video on youtube":ytvideo,
    "restart":restart,
    "shutdown":shutdown,
    "mute":mute,
    "unmute":unmute,
    "current date":current_date,
    "send message":send_message,
    "current temperature":temperature,
    "current time":current_time,
    "ai mode":ai_mode,
    "battery":battery,
    "help":help_function,
    "close":close_apps,
    "Incomplete":incomplete_command,
    # "exit":exit_fucntion
}
   

    
    
    
    
        
    
 
    
    
    
    
        
        