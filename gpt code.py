import sys
import webbrowser
import datetime

import detectlanguage
import pyjokes
import pywhatkit
import wikipedia
import pyttsx3
import speech_recognition as sr
import os
import math
import random

from deep_translator import GoogleTranslator

detectlanguage.configuration.api_key = "d6e1c0b240102581d15e114628a303e6"

PHRASES = {
    'salutation': [
        "bonjour docteur.", "bonjour monssieur.", "bienvenue docteur vous êtes matinal.",
        "ravi de vous revoir en ce matin docteur.",
        "bonsoir docteur.", "bonsoir monssieur.", "bienvenue docteur.",
        "ravi de vous revoir en ce soir docteur.",
        "bon après midi docteur.", "bon aprés midi monssieur.", "comment allez-vous docteur. ?",
        "ravi de vous revoir en cet après midi docteur."
    ],
    'etat': [
        "je vais bien quand je vous parle", "je vais bien et vous", "la vie est belle", "je vais à merveille",
        "je suis au také", "bien pour le service", "bien", "ça va", "toujours prêt pour une aventure excitante",
        "j'ai juste hate de travailler", "je suis juste trop amouré et vous?"
    ],
    'merci': ["c'est un plaisir", "je vous en prie", "de rien", "c'est rien"]
}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language="fr-FR")
            print(said)
        except Exception as e:
            print("Exception:", str(e))

    return said.lower()


# fonction pour envoyer un message WhatsApp
def send_whatsapp_message(phone_number, message, hours, minutes):
    pywhatkit.sendwhatmsg(f"+{phone_number}", message, hours, minutes)


# fonction pour récupérer des informations sur Wikipédia
def wikipedia_search(query):
    wikipedia.set_lang("fr")
    try:
        results = wikipedia.summary(query, sentences=3)
        return results
    except:
        return "Désolé, je n'ai pas pu trouver d'informations à ce sujet sur Wikipédia."


# fonction pour ouvrir un site web à partir de l'URL
def open_website(url):
    webbrowser.open(url)


# fonction pour récupérer la date et l'heure actuelle
def get_date_time():
    now = datetime.datetime.now()
    date_time = now.strftime("Il est %H heures %M minutes, le %d/%m/%Y.")
    return date_time


# fonction pour résoudre une équation de second degré
def solve_quadratic_equation(a, b, c):
    delta = b ** 2 - 4 * a * c

    if delta > 0:
        x1 = (-b + math.sqrt(delta)) / (2 * a)
        x2 = (-b - math.sqrt(delta)) / (2 * a)
        print(f"Les solutions de l'équation sont : {x1} et {x2}")
        speak(f"Les solutions de l'équation sont : {x1} et {x2}")
    elif delta == 0:
        x = -b / (2 * a)
        print(f"L'unique solution de l'équation est : {x}")
        speak(f"L'unique solution de l'équation est : {x}")
    else:
        print("L'équation n'a pas de solution réelle.")
        speak("L'équation n'a pas de solution réelle.")


# fonction pour écrire un texte dans un fichier texte
def write_to_file(text, filename):
    with open(filename, "w") as file:
        file.write(text)
    return "Le texte a été écrit dans le fichier avec succès."


# fonction pour lire un fichier texte
def read_file(filename):
    try:
        with open(filename, "r") as file:
            text = file.read()
        return text
    except:
        return "Le fichier n'a pas pu être ouvert."


# fonction pour récupérer une blague en anglais
def get_joke():
    ma_blague = pyjokes.get_joke('en', 'all')
    return ma_blague


# fonction pour saluer l'utilisateur selon l'heure de la journée
def greet():
    now = datetime.datetime.now()
    if now.hour < 12:
        speak("Bonjour!")
    elif now.hour < 18:
        speak("Bon après-midi!")
    else:
        speak("Bonsoir!")


def wish_me():
    heure = datetime.datetime.now().hour
    if 0 <= heure < 12:
        speak("Bonjour !")
    elif 12 <= heure < 18:
        speak("Bon après-midi !")
    else:
        speak("Bonsoir !")
    speak("Comment puis-je vous aider ?")


def take_query():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("En écoute...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Reconnaissance...")
        query = r.recognize_google(audio, language='fr-FR')
        print(f"Utilisateur : {query}\n")

    except Exception as e:
        print("Répétez s'il vous plaît...")
        return "None"
    return query


if __name__ == "__main__":
    wish_me()
    while True:
        query = take_query().lower()

        if 'wikipédia' in query:
            speak('Recherche sur Wikipédia...')
            query = query.replace("wikipédia", "")
            results = wikipedia.summary(query, sentences=2, auto_suggest=False, redirect=False)
            speak("D'après Wikipédia")
            speak(results)

        elif 'ouvrir youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'ouvrir google' in query:
            webbrowser.open("https://www.google.com")

        elif 'ouvrir stack overflow' in query:
            webbrowser.open("https://stackoverflow.com")

        elif 'jouer de la musique' in query:
            music_dir = 'C:\\Users\\Romaric\\Music\\Playlists\\'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'l\'heure' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Il est {strTime}")

        elif 'ouvrir code' in query:
            code_path = "C:\\Users\\Romaric\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(code_path)

        elif 'envoyer un message' in query:
            speak("Veuillez indiquer le numéro de téléphone")
            phone_no = input("Entrez le numéro de téléphone : ")
            speak("Que devrais-je dire ?")
            msg = input("Entrez le message : ")
            webbrowser.open('https://web.whatsapp.com/send?phone=' + phone_no + '&text=' + msg)

        elif 'résoudre' in query:
            speak("Veuillez indiquer les coefficients de l'équation dans l'ordre a, b, c")
            a = int(input("Entrez le coefficient de x^2 : "))
            b = int(input("Entrez le coefficient de x : "))
            c = int(input("Entrez la constante : "))
            solve_quadratic_equation(a, b, c)
        elif 'heure' in query:
            heure = datetime.datetime.now().strftime('%H heure :%M minute')
            speak('il est' + heure)
            print(heure)

        elif 'date' in query:
            get_date_time()
        elif "musique de" in query:
            musique = query.replace("musique de", "")
            print("musique en cours ...")
            pywhatkit.playonyt(musique)

        elif "équation" and "second degré" in query:
            a = float(input(speak("veillez entrer le a ")))
            b = float(input(speak("veillez entrer le b ")))
            c = float(input(speak("veillez entrer le c ")))
            solve_quadratic_equation(a, b, c)

        elif 'merci' in query:
            speak(random.choices(PHRASES['merci']))

        elif 'comment t\'appelles-tu' or 'ton nom' or 'comment tu t\'appelles' in query:
            speak("Je m'appelle ARIS et je suis là pour servir")

        elif "ouvre le répertoire" in query:
            rep = query.replace("ouvre le répertoire", '')
            speak(f'Ouverture du répertoire {rep} en cours.')
            os.system(rep)
            print(os.listdir(rep))

        elif 'répertoire parents' in query:
            print(os.listdir(os.getcwd()))

        elif 'saisir ' and 'texte' in query:
            write_to_file(query)

        elif 'qui est' in query:
            person = query.replace('qui est', '')
            wikipedia.set_lang('fr')
            info = wikipedia.summary(person, 1)
            speak(info)

        elif 'sortir avec' in query:
            speak("Désolé je suis suis pas de bonne hummeur. Peut-être que si vous bosser un peu je serai d'hummeur")

        elif 'es-tu es couple ' in query:
            speak('Non pas encore, mon coeur est à conquérir.')

        elif 'désactive toi' in query:
            speak('Ce fut un plaisir.')
            sys.exit()

        elif 'comment' and 'vas' or 'bien et toi' in query:
            speak(random.choices(PHRASES['etat']))

        elif "ouvre google" in query:
            webbrowser.open('https://www.google.com')
            speak("C'est fais, voici google Monsieur")

        elif "lance google" in query:
            webbrowser.open('https://www.google.fr')
            speak("Google à été lancer, Monsieur")

        elif "lance facebook" in query:
            webbrowser.open('https://www.facebook.com')
            speak("Voici Facebook, Monsieur")

        elif "lance youtube" in query:
            webbrowser.open('https://www.youtube.com')
            speak("Youtube à été bien lancer, Monsieur")

        elif "lance stack overflow" in query:
            webbrowser.open('https://stackoverflow.com')
            speak("Bienvenue sur Stack Overflow, Monsieur")

        elif "lance le forum des développeurs" in query:
            webbrowser.open('https://stackoverflow.com')
            speak("Bienvenue sur Stack Overflow, Monsieur")

        elif "lance le site de genius " in query:
            webbrowser.open('https://genius-academy.ci')
            speak("Bienvenue sur Genius Academy, Monsieur")

        elif "oui je suis là" in query:
            speak("Avez vous besoin de moi ?")

        elif "oui" in query:
            speak("Que puis-je faire pour vous?")

        elif "je suis là" in query:
            speak("Avez vous besoin de moi ?")

        elif "blague" in query:
            bl = get_joke()
            blag = GoogleTranslator(source='en', target='fr').translate(text=bl)
            speak(blag)

        elif 'bonjour' or 'bonsoir' or 'bon après midi' in query:
            speak(random.choices(PHRASES['salutation']))

        elif "traduire" and "anglais" in query:
            texte = query.replace("traduire", "")
            texte = query.replace("anglais", "")
            dt = detectlanguage.simple_detect(texte)

            texte_traduit = GoogleTranslator(source='auto', target='en').translate(text=texte)
            speak(f"{texte} en anglais se dit: {texte_traduit}")

            '''pour cette partie je dois trouver un moyen d'optimiser le code de sorte a pouvoir traduire 
            dans toutes les langues '''
