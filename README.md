# SpeedyLation
 Translate highlighted/selected words from English to Hebrew quickly.
 Highlight/Select any word/phrase in English to see its translation to Hebrew and Its meaning in English.
 
 Once pressing the selected key, the program opens a small window with the Hebrew translation as is found in https://www.morfix.co.il/ and the highest voted meaning in Urban Dictionary.
 The windows has a button you press to listen to how the word is pronounced in English (with Google's text-to-speech).
 To close the window, press the x button or the key you pressed to open the window.
 
 The program web-scrapes the aforementioned sites to fetch the information, uses the gTTS python library to create the mp3 file for the pronouciation and copies the text you highlighted to gather the information (without changing the clipboard and last copied thing).
 
 Installation (for windows):
 Download "Speedylation.exe" and put it in the Startup folder.
 You can access the Startup folder by holding the Win key and 'r', writing "shell:startup" in the search box and pressing ok.
 
 After the initial installation, open the "Speedylation.exe" file once to create the "ProgramKey.txt".
 In that file, write the .keysym of the key you want to use for translation (use a useless key like Pause/Break, Scroll lock or the Menu key).
 You can find the .keysym of every key here: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html.
 
 Now, it sounds shady, I know , but you're going to need to 'allow the threat' at Windows Defender or any other anti-virus software you might have.
 If you have still have any doubt that it's a maleware, you can look at the code and build it yourseld with pyinstaller (using "pyinstaller --onefile --exclude-module _bootlocale --noconsole main.py").
 
 Now, run the "Speedylation.exe" file again or restart the system and you're all set! Enjoy!