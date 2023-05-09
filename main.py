import pyttsx3 as ttx
import time
import random
import speech_recognition as sr
import openai

############################### Configuration de la clé d'API ############
openai.api_key = "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"  ##
##########################################################################

bonjour = ["bonjour docteur.", "bonjour monssieur.", "bienvenue docteur vous êtes matinal.",
           "ravi de vous revoir en ce matin docteur."]
bonsoir = ["bonsoir docteur.", "bonsoir monssieur.", "bienvenue docteur.", "ravi de vous revoir en ce soir docteur."]
bon_apres_midi = ["bon après midi docteur.", "bon aprés midi monssieur.", "comment allez-vous docteur. ?",
                  "ravi de vous revoir en cet après midi docteur."]
machine = ttx.init()

#####################################################################

jour = time.strftime("%d")
mois = time.strftime(" %m")
annee = time.strftime(" %Y")
l_heure = time.strftime("%H")
minute = time.strftime(" %I ")
sec = time.strftime("%S")


#####################################################################


# faire parler l'ordinateur
def talk(objet):
    machine.say(objet)
    machine.runAndWait()


def heure():
    temps = f"nous somme au {jour}{mois} ième mois {annee} et il est {l_heure} heure {minute} minutes et {sec} secondes"
    talk(temps)


def salutation():
    if int(l_heure) < 12:
        talk(random.choices(bonjour))
    elif int(l_heure) > 18:
        talk(random.choices(bonsoir))
    else:
        talk(random.choices(bon_apres_midi))


def saisi_texte(command):
    # nom_fichier = command.replace('le non du fichier est', '')
    with open('hubert.txt', 'a+') as file:
        for texte in command:
            file.write(texte)
    file.close()
    '''
    with open("saisie_assistant.docx", "r+") as file:
        texte = file.readlines()
        file.close()
'''


listener = sr.Recognizer()


def ecouter():
    try:
        with sr.Microphone() as source:
            listener.pause_threshold = 5
            voix = listener.listen(source)
            command = listener.recognize_google(voix, language='fr-FR')
            command = command.lower()
    except UnboundLocalError:
        talk("je n'ai pas compris veillez réessayer.")
    else:
        print('...')
    return command


def iareponse(inputext):
    input_text = f"{inputext}"

    # Appel à l'API de ChatGPT-3 pour générer une réponse
    response = openai.Completion.create(
        engine="davinci",
        prompt=input_text,
        max_tokens=1024,
        n=5,
        stop=None,
        temperature=0.5,
    )

    # Affichage de la réponse générée
    return response.choices[0].text


def lanceur():
    print('...')
    commande = ecouter()
    print(commande)
    reponse = iareponse(commande)

    print(reponse)
    talk(reponse)


talk('bonjour, en quoi puis-je vous aidez ?')

while True:
    lanceur()
