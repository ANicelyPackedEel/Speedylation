import os
import sys
import tkinter
from tkinter import *
import clipboard
import pyautogui
import requests
from bs4 import BeautifulSoup
from pynput import keyboard as keyboard
from pynput.mouse import Button, Controller
from gtts import gTTS
from playsound import playsound
# import vlc

# key table to write .keysym in file https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html
program_key = "Pause"
if not os.path.exists('C:\\Speedylation'):
    os.makedirs('C:\\Speedylation')
if not os.path.exists("C:\\Speedylation\\ProgramKey.txt"):
    file = open("C:\\Speedylation\\ProgramKey.txt", 'w')
    file.write("Pause")
    file.close()
    sys.exit()
else:
    with open("C:\\Speedylation\\ProgramKey.txt", "r+") as f:
        f.seek(0)
        if f.read() == "":
            f.seek(0)
            f.write("Pause")
        f.seek(0)
        program_key = f.read()

"""
def detect_darkmode_in_windows():
    try:
        import winreg
    except ImportError:
        # window.
        return False
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        reg_key = winreg.OpenKey(registry, reg_keypath)
    except FileNotFoundError:
        return False

    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            if value_name == 'AppsUseLightTheme':
                return value == 0
        except OSError:
            break
    return False
"""


def on_press(key):
    key_string = f"{key}"[4:]
    if key_string.upper() != program_key.upper():
        return

    clipboard_text = clipboard.paste()
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    text = clipboard.paste()
    clipboard.copy(clipboard_text)

    if text == '':
        return

    data = requests.get("https://www.morfix.co.il/" + text)
    soup = BeautifulSoup(data.text, "lxml")

    translations = ''
    for t in soup.find_all('div', {'class': 'normal_translation_div'}):
        translations += t.text
    if translations == '':
        translations = "No translation found :("
    else:
        translations = translations.replace(';', ',').strip('\n').rstrip() + "\n"

    data = requests.get("https://www.urbandictionary.com/define.php?term={}".format(text))
    soup = BeautifulSoup(data.content, "lxml")

    word_meaning = soup.find("div", attrs={"class": "meaning"})

    def close():
        window.destroy()

    mouse_pos = pyautogui.position()

    window = Tk()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    window.geometry(f"+{mouse_x}+{mouse_y}")  # x, y
    window.title("What's \"" + text + "\"?")
    window.lift()
    window.attributes('-topmost', True)
    window.bind(f"<{program_key}>", lambda event: close())
    window.resizable(True, True)

    translated = Label(text="\"" + text + "\" in Hebrew is:")
    translation = Label(text=translations.lstrip().rstrip())
    translated.pack()
    translation.pack()
    meaning = Label(text="The meaning of " + "\"" + text + "\" by Urban Dictionary:")
    meaning.pack()
    if word_meaning is not None:
        word_meaning = word_meaning.text
        means = Label(text=word_meaning)
        means.pack()
    else:
        word_meaning = "No definition found :("
        means = Label(text=word_meaning)
        means.pack()

    mouse = Controller()
    window_pos = (mouse_x + window.winfo_width() / 2, mouse_y + window.winfo_height() / 2)
    pos = mouse.position
    mouse.position = window_pos
    window.update()
    mouse.press(Button.left)
    mouse.release(Button.left)
    mouse.position = pos
    window.after_idle(window.attributes, '-topmost', False)

    def tts_pressed():
        if os.path.exists('C:\\Speedylation\\temp.mp3'):
            os.remove('C:\\Speedylation\\temp.mp3')

        tts = gTTS(text=text, lang='en', tld="com")
        tts.save("C:\\Speedylation\\temp.mp3")

        playsound("C:\\Speedylation\\temp.mp3")
        # p = vlc.MediaPlayer("temp.mp3")
        # p.play()

    tts_button = tkinter.Button(window, text="Hear pronunciation", command=tts_pressed)
    tts_button.pack()

    window.minsize(window.winfo_width(), window.winfo_height())

    window.mainloop()


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Use the following command to build the .exe file:
# pyinstaller --onefile --exclude-module _bootlocale --noconsole -n Speedylation.exe main.py
