import os
import eel
import subprocess
import platform
from engine.features import *
from engine.command import *
from engine.auth import recoganize

# Detectar el sistema operativo
current_os = platform.system()

# Archivo a ejecutar según el sistema operativo
if current_os == "Windows":
    script = "device.bat"
    shell = True  # Usar shell en Windows
    open_browser_cmd = 'start msedge.exe --app="http://localhost:8000/index.html"'
else:  # Linux o cualquier otro Unix-like
    script = "device.sh"
    shell = False  # No usar shell directamente en Linux/Unix
    open_browser_cmd = 'xdg-open "http://localhost:8000/index.html"'  # Abre en el navegador predeterminado

def start():
    eel.init("www")

    playAssistantSound()

    @eel.expose
    def init():
        print("init 1")
        # Ejecutar el archivo adecuado (device.bat o device.sh)
        subprocess.run(
            [script] if shell else ["bash", script],
            check=True,
            text=True,
            capture_output=True,
            shell=shell  # Solo usar shell=True en Windows
        )
        eel.hideLoader()
        print("init 2")
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir, How can i Help You")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Fail")

    print("init 3")
    
    # Abrir el navegador según el sistema operativo
    subprocess.run(open_browser_cmd, shell=True, check=True)

    # Iniciar eel para servir la página web
    eel.start('index.html', mode=None, host='localhost', block=True)