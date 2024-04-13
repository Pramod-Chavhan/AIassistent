import sys
import webbrowser
from bs4 import BeautifulSoup
from numpy import source
import psutil
import pyttsx3
import requests
import speech_recognition as sr
import eel
import time
import pyautogui
from requests import get
import os
from PIL import Image
from dotenv import load_dotenv
from engine.config import ASSISTANT_NAME
from engine.helper import remove_words

load_dotenv()

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
        
    try:
        words_to_remove = [ASSISTANT_NAME, 'open']
        query = remove_words(query, words_to_remove)

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)

        elif "search image" in query or "search a image" in query or "image search" in query:
            speak("What do you want to search mr. Pramod?")
            generate_request = takecommand()  # Listen for the drawing request

            if generate_request:  # Check if a valid input is received
                try:
                    api_key_1 = os.getenv("qLI_2ZLy2zeJj1ASYb9YCY9gFQVzJOD9j6p6PWjNyRE")
                    base_url = "https://api.unsplash.com"
                    access_key = api_key_1
                    endpoint = "/search/photos"
                    url = f"{base_url}{endpoint}?query={generate_request}&client_id={access_key}"
                    response = requests.get(url)

                    if response.status_code == 200:
                        image_url = response.json()["results"][0]["urls"]["regular"]
                        image_response = requests.get(image_url)
                        with open("generated_image.jpg", "wb") as img_file:
                            img_file.write(image_response.content)

                        speak("Image serached successfully.")
                            
                        # Ask to show the generated image
                        speak("Can I show you the what i found...?")
                        view_image = takecommand().lower()
                        if "yes" in view_image:
                            img = Image.open("generated_image.jpg")
                            img.show()
                    else:
                        speak(f"Error generating image: {response.status_code} - {response.reason}")

                except Exception as e:
                    speak(f"Error generating image: {e}")



        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak('volume increased')
                
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak('volume decreased')
           
        elif ("volume mute" in query) or ("mute the sound" in query) :
            pyautogui.press("volumemute")
            speak('volume muted')

        elif "facebook" in query:
            speak('opening your facebook')
            webbrowser.open('https://www.facebook.com/')

        elif "whatsapp" in query:
            speak('opening your whatsapp')
            webbrowser.open('https://web.whatsapp.com/')

        elif "instagram" in query:
            speak('opening your instagram')
            webbrowser.open('https://www.instagram.com/')

        elif "twitter" in query:
            speak('opening your twitter')
            webbrowser.open('https://twitter.com/Suj8_116')

        elif 'discord' in query:
            speak('opening your discord')
            webbrowser.open('https://discord.com/channels/@me')

        elif 'github' in query:
            speak('opening your github')
            webbrowser.open('https://github.com/Pramod-chavan-7775/Pramod-Chavhan')

        elif 'gitlab' in query:
            speak('opening your gitlab')
            webbrowser.open('https://github.com/Pramod-chavan-7775/Pramod-Chavhan')

        elif 'hotstar' in query:
            speak('opening your disney plus hotstar')
            webbrowser.open('https://www.hotstar.com/in')

        elif 'prime amazon' in query:
            speak('opening your amazon prime videos')
            webbrowser.open('https://www.primevideo.com/')

        elif 'netflix' in query:
            speak('opening Netflix videos')
            webbrowser.open('https://www.netflix.com/')

        elif 'portfolio' in query:
            speak('opening your porfolio sir')
            webbrowser.open('pramodchavhan.netlify.app')

        elif ('calculator'in query) :
            speak('Opening calculator')
            os.startfile('C:\\Windows\\System32\\calc.exe')

        elif ('paint'in query) :
            speak('Opening msPaint')
            os.startfile('c:\\Windows\\System32\\mspaint.exe')

        elif ('notepad'in query) :
            speak('Opening notepad')
            os.startfile('c:\\Windows\\System32\\notepad.exe')

        elif ('discord'in query) :
            speak('Opening discord')
            os.startfile('..\\..\\Discord.exe')

        elif ('editor'in query) :
            speak('Opening your Visual studio code')
            os.startfile('..\\..\\Code.exe')

        elif ('online classes'in query) :
            speak('Opening your Microsoft teams')
            webbrowser.open('https://teams.microsoft.com/')

        elif ('spotify'in query) :
            speak('Opening spotify')
            os.startfile('..\\..\\Spotify.exe')

        elif ('lt spice'in query) :
            speak('Opening lt spice')
            os.startfile("..\\..\\XVIIx64.exe")

        elif ('steam'in query) :
            speak('Opening steam')
            os.startfile("..\\..\\steam.exe")

        elif ('media player'in query) :
            speak('Opening VLC media player')
            os.startfile("C:\Program Files\VideoLAN\VLC\vlc.exe")
 
        elif ('close calculator'in query) :
            speak("okay boss, closeing caliculator")
            os.system("taskkill /f /im calc.exe")

        elif ('close paint'in query) :
            speak("okay boss, closeing mspaint")
            os.system("taskkill /f /im mspaint.exe")

        elif ('close notepad'in query) :
            speak("okay boss, closeing notepad")
            os.system("taskkill /f /im notepad.exe")

        elif ('close spotify'in query) :
            speak("okay boss, closeing spotify")
            os.system("taskkill /f /im Spotify.exe")

        elif ('close media player'in query) :
            speak("okay boss, closeing media player")
            os.system("taskkill /f /im vlc.exe")  

        elif 'flipkart' in query:
            speak('Opening flipkart online shopping website')
            webbrowser.open("https://www.flipkart.com/")

        elif 'amazon' in query:
            speak('Opening amazon online shopping website')
            webbrowser.open("https://www.amazon.in/")

        elif 'screenshot' in query:
            speak("Boss, please tell me the name for this screenshot file")
            name = query()
            speak("Please boss hold the screen for few seconds, I am taking screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("I am done boss, the screenshot is saved in main folder.")

        elif 'system condition' in query:
            speak("checking the system condition")
            usage = str(psutil.cpu_percent())
            speak("CPU is at"+usage+" percentage")
            battray = psutil.sensors_battery()
            percentage = battray.percent
            speak(f"Boss our system have {percentage} percentage Battery")
            if percentage >=75:
                speak(f"Boss we could have enough charging to continue our work")
            elif percentage >=40 and percentage <=75:
                speak(f"Boss we should connect out system to charging point to charge our battery")
            elif percentage >=15 and percentage <=30:
                speak(f"Boss we don't have enough power to work, please connect to charging")
            else:
                speak(f"Boss we have very low power, please connect to charging otherwise the system will shutdown very soon")

        elif 'my location' in query:
            speak("Wait boss, let me check")
            try:
                IP_Address = get('https://api.ipify.org').text
                print(IP_Address)
                url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
                print(url)
                geo_reqeust = get(url)
                geo_data = geo_reqeust.json()
                city = geo_data['city']
                state = geo_data['region']
                country = geo_data['country']
                tZ = geo_data['timezone']
                longitude = geo_data['longitude']
                latidute = geo_data['latitude']
                org = geo_data['organization_name']
                print(city+" "+state+" "+country+" "+tZ+" "+longitude+" "+latidute+" "+org)
                speak(f"sir, i am not sure, but i think we are in {city} city of {state} state of {country} country")
                speak(f"and boss, we are in {tZ} timezone the latitude os our location is {latidute}, and the longitude of our location is {longitude}, and we are using {org}\'s network ")
            except Exception as e:
                speak("Sorry boss, due to network issue i am not able to find where we are.")
                pass

        # elif "download" in query:
        #     speak("Boss please enter the youtube video link which you want to download")
        #     link = input("Enter the YOUTUBE video link: ")
        #     yt=YouTube(link)
        #     yt.streams.get_highest_resolution().download()
        #     speak(f"Boss downloaded {yt.title} from the link you given into the main folder")
        elif 'gmail' in query:
            speak('opening your google gmail sir...')
            webbrowser.open('https://mail.google.com/mail/')

        elif 'maps' in query:
            speak('opening google maps')
            webbrowser.open('https://www.google.co.in/maps/')

        elif 'news' in query:
            speak('opening google news')
            webbrowser.open('https://news.google.com/')

        elif 'calender' in query:
            speak('opening google calender')
            webbrowser.open('https://calendar.google.com/calendar/')

        elif 'photos' in query:
            speak('opening your google photos')
            webbrowser.open('https://photos.google.com/')

        elif 'documents' in query:
            speak('opening your google documents')
            webbrowser.open('https://docs.google.com/document/')

        elif 'spreadsheet' in query:
            speak('opening your google spreadsheet')
            webbrowser.open('https://docs.google.com/spreadsheets/')

        elif "temperature" in query:
            IP_Address = get('https://api.ipify.org').text
            url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
            geo_reqeust = get(url)
            geo_data = geo_reqeust.json()
            city = geo_data['city']
            search = f"temperature in {city}"
            url_1 = f"https://www.google.com/search?q={search}"
            r = get(url_1)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div",class_="BNeawe").text
            speak(f"current {search} is {temp}")

        elif 'college site' in query or 'college website' in query:
            speak('opening your Trinity Acadamy of engineearing ,pune site')
            webbrowser.open('https://www.kjei.edu.in/tae/')

        elif 'your name' in query:
            speak("My name is jarvis")

        elif 'my name' in query:
            speak("your name is Mr. pramod")

        elif 'university name' in query:
            speak("you are studing in Amrita Vishwa Vidyapeetam, with batcheloe in Computer Science and Artificail Intelligence") 

        elif 'what can you do' in query:
            speak("I talk with you until you want to stop, I can say time, open your social media accounts,your open source accounts, open google browser,and I can also open your college websites, I can search for some thing in google and I can tell jokes")
        
        elif 'your age' in query:
            speak("I am very young that u")

        elif 'date' in query:
            speak('Sorry not intreseted, I am having headache, we will catch up some other time')

        elif 'are you single' in query:
            speak('No, I am in a relationship with wifi')

        elif 'are you there' in query:
            speak('Yes boss I am here')

        elif 'tell me something' in query:
            speak('boss, I don\'t have much to say, you only tell me someting i will give you the company')

        elif 'thank you' in query:
            speak('boss, I am here to help you..., your welcome')

        elif 'in your free time' in query:
            speak('boss, I will be listening to all your words')

        elif 'i love you' in query:
            speak('I love you too boss')

        elif 'can you hear me' in query:
            speak('Yes Boss, I can hear you')

        elif 'do you ever get tired' in query:
            speak('It would be impossible to tire of our conversation')

        elif ('hi'in query) or('hai'in query) or ('hey'in query) or ('hello' in query) :
            speak("Hello boss what can I help for u")

        elif ('shutdown the system' in query) or ('down the system' in query):
            speak("Boss shutting down the system in 10 seconds")
            time.sleep(10)
            os.system("shutdown /s /t 5")

        elif 'restart the system' in query:
            speak("Boss restarting the system in 10 seconds")
            time.sleep(10)
            os.system("shutdown /r /t 5")

        elif 'sleep the system' in query:
            speak("Boss the system is going to sleep")
            os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")
        
        
        elif ("good bye" in query) or ("get lost" in query):
                speak("Thanks for using me boss, have a good day")
                sys.exit()
        
        elif 'ip address' in query:
                ip = get('https://api.ipify.org').text
                print(f"your IP address is {ip}")
                speak(f"your IP address is {ip}")
        
        elif "scroll down" in query:
            pyautogui.scroll(-500)  # Scroll down
        elif "scroll up" in query:
            pyautogui.scroll(500)  # Scroll up
        elif "scroll left" in query:
            pyautogui.hscroll(-500)  # Scroll left
        elif "scroll right" in query:
            pyautogui.hscroll(500)  # Scroll right




        


        else:   
            from engine.features import chatBot
            chatBot(query)
    except:
        print("error")
        
    eel.ShowHood()

