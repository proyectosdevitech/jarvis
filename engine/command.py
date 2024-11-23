import pyttsx3
import speech_recognition as sr
import eel
import time
import sys

# Motor de voz global
engine = None

# Inicializar el motor de voz
def init_engine():
    global engine
    if engine is None:  # Solo inicializar si no está ya creado
        if sys.platform == 'win32':  # Si es Windows
            engine = pyttsx3.init('sapi5')
        else:  # Si es Linux
            engine = pyttsx3.init('espeak')

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Establecer la voz
        engine.setProperty('rate', 174)  # Establecer la velocidad de la voz
    return engine

# Función para hablar el texto
def speak(text):
    text = str(text)
    eel.DisplayMessage(text)  # Mostrar el mensaje en la interfaz de usuario
    engine = init_engine()
    engine.say(text)  # Reproducir el texto en voz alta
    eel.receiverText(text)  # Enviar el texto a la interfaz de usuario
    try:
        engine.runAndWait()  # Esperar a que termine de hablar
    except Exception as e:
        print(f"Error en pyttsx3: {e}")

# Función para capturar el comando de voz
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        eel.DisplayMessage('Listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
            print('Recognizing....')
            eel.DisplayMessage('Recognizing....')
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            eel.DisplayMessage(query)
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            eel.DisplayMessage("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
            eel.DisplayMessage("Error with the speech recognition service.")
        except Exception as e:
            print(f"Error: {e}")
            eel.DisplayMessage("An unexpected error occurred.")
        return ""  # En caso de error, devolver una cadena vacía

# Comandos expuestos a la interfaz de usuario
@eel.expose
def allCommands(message=1):
    try:
        if message == 1:
            query = takecommand()  # Tomar el comando de voz
            if query:
                print(query)
                eel.senderText(query)  # Enviar el texto al frontend
            else:
                return
        else:
            query = message
            eel.senderText(query)  # Enviar el mensaje al frontend

        # Comandos y acciones
        command_dict = {
            "open": "openCommand",
            "on youtube": "PlayYoutube",
            "send message": "sendMessage",
            "phone call": "makeCall",
            "video call": "whatsApp"
        }

        for command, function in command_dict.items():
            if command in query:
                module = __import__('engine.features', fromlist=[function])
                func = getattr(module, function)
                func(query)
                return
        
        # Si no hay coincidencias, usar el chatbot
        from engine.features import chatBot
        chatBot(query)  # Llamar al chatbot para otros comandos

    except Exception as e:
        print(f"Error executing command: {e}")
        eel.DisplayMessage(f"Error executing command: {e}")

    eel.ShowHood()  # Mostrar la interfaz de usuario después de ejecutar el comando
