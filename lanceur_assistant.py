import sys
import pyttsx3 as ttx
import time
import datetime
import random
import speech_recognition as sr
import pywhatkit
import wikipedia
import os
import math
import webbrowser
import pyjokes
from deep_translator import GoogleTranslator
import detectlanguage
###########################################################################
bonjour = ["bonjour docteur.", "bonjour monssieur.", "bienvenue docteur vous êtes matinal.",
           "ravi de vous revoir en ce matin docteur."]

bonsoir = ["bonsoir docteur.", "bonsoir monssieur.", "bienvenue docteur.",
           "ravi de vous revoir en ce soir docteur."]

bon_apres_midi = ["bon après midi docteur.", "bon aprés midi monssieur.", "comment allez-vous docteur. ?",
                  "ravi de vous revoir en cet après midi docteur."]

etat = ["je vais bien quand je vous parle", "je vais bien et vous", "la vie est belle", "je vais à merveille",
        "je suis au také", "bien pour le service", "bien", "ça va", "toujours prêt pour une aventure excitante",
        "j'ai juste hate de travailler", "je suis juste trop amouré et vous?"]

merci = ["c'est un plaisir", "je vous en prie", "de rien", "c'est rien"]




#################################
nom_assistant = "Pela"
##############################


machine = ttx.init()
jour = time.strftime("%d")
mois = time.strftime(" %m")
annee = time.strftime(" %Y")
l_heure = time.strftime("%H")
minute = time.strftime(" %I ")
sec = time.strftime("%S")
#####################################################################

listener = sr.Recognizer()
voice = machine.getProperty('voices')
machine.setProperty('voice', 'french')
machine.setProperty('rate', 170)


detectlanguage.configuration.api_key = "d6e1c0b240102581d15e114628a303e6"
# Enable secure mode (SSL) if you are passing sensitive data
# detectlanguage.configuration.secure = True


def parler(text):
    machine.say(text)
    machine.runAndWait()


def dateheure():
    temps = f"nous somme au {jour}{mois} ième mois {annee} et il est {l_heure} heure {minute} minutes et {sec} secondes"
    parler(temps)


def equation_2(a, b, c):
    print("------------------RESOLUTION D'EQUATION DE TYPE ax^2 + bx + c = 0 -------------------------- ")
    try:
        discriminant = math.exp(b) - 4 * a * c
        print(f"le discriminant est:{discriminant}")
        parler(f"le discriminant est:{discriminant}")

        if discriminant < 0:
            print("pas de solution")
            parler("pas de solution")
        elif discriminant == 0:
            x1 = -b / 2 * a
            print(f"la solution est : {x1}")
            parler(f"la solution est : {x1}")
        elif discriminant > 0:
            x1 = (b - math.sqrt(discriminant)) / 2 * a
            x2 = (-b - math.sqrt(discriminant)) / 2 * a
            print(f"les solutions sont : x1 = {x1} et x2 ={x2}")
            parler(f"les solutions sont : x1 = {x1} et x2 ={x2}")

    except ZeroDivisionError:
        print("veiller saisir une equation de second dégré le 'a' ne peut pas être 0")
        parler("veiller saisir une equation de second dégré le 'a' ne peut pas être 0")
    except ValueError:
        print("veiller saisir des nombre réels svp")
        parler("veiller saisir des nombre réels svp")


def whatsapp_message(numero, message):
    pywhatkit.sendwhatmsg_instantly(numero, message)


def saisi_texte(command):
    # nom_fichier = command.replace('le non du fichier est', '')
    with open('saisie_assistant.txt', 'a+') as file:
        for texte in command:
            file.write(texte + "\n")
        file.close()
        parler('Si vous voulez affichier votre texte dites: afficher mon texte')
    if 'afficher mon texte' in command:
        with open("saisie_assistant.txt", "r+") as file:
            texte = file.readlines()
            print(texte)
            file.close()


def blague():
    ma_blague = pyjokes.get_joke('en', 'all')
    return ma_blague


def salutation():
    if int(l_heure) < 12:
        parler(random.choices(bonjour))
    elif int(l_heure) > 18:
        parler(random.choices(bonsoir))
    else:
        parler(random.choices(bon_apres_midi))


def ecouter():
    try:

        with sr.Microphone() as source:
            print("...")
            listener.pause_threshold = 5
            voix = listener.listen(source)
            commande = listener.recognize_google(voix, language='fr-FR')
            commande = commande.lower()
            source = detectlanguage.simple_detect(commande)
            if source[0] != 'fr':
                commande = GoogleTranslator(source='auto', target='fr').translate(text=commande)
            if nom_assistant in commande:
                commande = commande.replace(f"{nom_assistant}", '')
    except TimeoutError:
        parler("revoyer votre connexion puis réessayer")

    except sr.RequestError:
        parler("votre connection internet étant désactivée, je ne peux pas vous aider pour le moment!")
    except sr.UnknownValueError:
        parler("je ne parle pas cette langue. voulez-vous changer de langue?")
        time.sleep(5)
        if UnboundLocalError:
            parler("je ne comprend pas")
            breakpoint()
    return commande


def lancer_assistant():
    command = ecouter()

    print(command)
    if 'heure' in command:
        heure = datetime.datetime.now().strftime('%H heure :%M minute')
        parler('il est' + heure)
        print(heure)

    elif 'date' in command:
        dateheure()
    elif "musique de" in command:
        musique = command.replace("musique de", "")
        print("musique en cours ...")
        pywhatkit.playonyt(musique)
        time.sleep(40)

    elif "équation" and "second degré" in command:
        a = float(input(parler("veillez entrer le a ")))
        b = float(input(parler("veillez entrer le b ")))
        c = float(input(parler("veillez entrer le c ")))
        equation_2(a, b, c)

    elif 'merci' in command:
        parler(random.choices(merci))

    elif "message" and "whatsapp" in command:
        numero = input(parler("entrez le numero du destinateur s'il vous plait"))
        parler("quel est votre message ?")
        message = ecouter()
        whatsapp_message(numero, message)

    elif 'bonjour' or 'bonsoir' or 'bon après midi' in command:
        parler('ravi de vous revoir')
        parler('que puis-je faire pour vous?')

    elif "comment t'appelles-tu" or "ton nom" or "comment tu t'appelles" in command:
        parler("Je m'appelle Pélagie et je suis là pour servir")

    elif "ouvre le répertoire" in command:
        rep = command.replace("ouvre le répertoire", '')
        parler(f'Ouverture du répertoire {rep} en cours.')
        os.system(rep)
        print(os.listdir(rep))

    elif 'répertoire parents' in command:
        print(os.listdir(os.getcwd()))

    elif 'saisir ' and 'texte' in command:
        saisi_texte(command)

    elif 'qui est' in command:
        person = command.replace('qui est', '')
        wikipedia.set_lang('fr')
        info = wikipedia.summary(person, 1)
        parler(info)

    elif 'sortir avec' in command:
        parler("Désolé je suis suis pas de bonne hummeur. Peut-être que si vous bosser un peu je serai d'hummeur")

    elif 'es-tu es couple ' in command:
        parler('Non pas encore, mon coeur est à conquérir.')

    elif 'désactive toi' in command:
        parler('Ce fut un plaisir.')
        sys.exit()

    elif 'comment' and 'vas' or 'bien et toi' in command:
        parler(random.choices(etat))

    elif "ouvre google" in command:
        webbrowser.open('https://www.google.com')
        parler("C'est fais, voici google Monsieur")

    elif "lance google" in command:
        webbrowser.open('https://www.google.fr')
        parler("Google à été lancer, Monsieur")

    elif "lance facebook" in command:
        webbrowser.open('https://www.facebook.com')
        parler("Voici Facebook, Monsieur")

    elif "lance youtube" in command:
        webbrowser.open('https://www.youtube.com')
        parler("Youtube à été bien lancer, Monsieur")

    elif "lance stack overflow" in command:
        webbrowser.open('https://stackoverflow.com')
        parler("Bienvenue sur Stack Overflow, Monsieur")

    elif "lance le forum des développeurs" in command:
        webbrowser.open('https://stackoverflow.com')
        parler("Bienvenue sur Stack Overflow, Monsieur")

    elif "lance le site de genius academy" in command:
        webbrowser.open('https://genius-academy.ci')
        parler("Bienvenue sur Genius Academy, Monsieur")

    elif "ouvre bloc-note" in command:
        os.system("C:\\Windows\\notepad.exe")
        parler("J'ai ouvert Bloc Notes pour vous")

    elif "lance bloc-note" in command:
        parler("deux sécondes monsieur J'ouvre Bloc Notes pour vous")
        os.system("C:\\Windows\\notepad.exe")

    elif "android studio" in command:
        parler("Ouverture en cours")
        os.system("C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe")

    elif "oui je suis là" in command:
        parler("Avez vous besoin de moi ?")

    elif "oui" in command:
        parler("Que puis-je faire pour vous?")

    elif "je suis là" in command:
        parler("Avez vous besoin de moi ?")

    elif "blague" in command:
        bl = blague()
        blag = GoogleTranslator(source='en', target='fr').translate(text=bl)
        parler(blag)

    elif "traduire" and "anglais" in command:
        texte = command.replace("traduire", "")
        texte = command.replace("anglais", "")
        dt = detectlanguage.simple_detect(texte)

        texte_traduit = GoogleTranslator(source='auto', target='en').translate(text=texte)
        parler(f"{texte} en anglais se dit: {texte_traduit}")

        '''pour cette partie je dois trouver un moyen d'optimiser le code de sorte a pouvoir traduire 
        dans toutes les langues '''

    else:
        parler("je ne suis pas capable de repondre à cette préoccupation pour l'instant")


salutation()

parler('Que puis-je faire pour vous?')

while True:
    lancer_assistant()
