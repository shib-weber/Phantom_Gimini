import os
import subprocess

def perform_action(text):
    text = text.lower()
    if "open notepad" in text:
        subprocess.Popen(['notepad.exe'])
        return "Opening Notepad for you."
    elif "shutdown" in text:
        return "I cannot do that for safety reasons, but the command is mapped."
    return None