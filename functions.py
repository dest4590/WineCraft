from time import sleep as wait
from customtkinter import CTk, CTkButton, StringVar, CTkComboBox, CTkEntry, CTkProgressBar, CTk
from random import choice
from config import update_config
from cheats import find_cheat, run_cheat, createFolder
from threading import Thread
from download import download
import os

minecraft_threads = []

def start_cheat(app: CTk, start_button: CTkButton, nickname: CTkEntry, combobox: CTkComboBox, progress_bar: CTkProgressBar):
    print('Start Cheat: ' + combobox.get())

    update_config('nickname', nickname.get())

    # start cheat in new thread
    cheat_thread = Thread(target=run_cheat, args=(combobox.get(), nickname.get(), progress_bar))
    cheat_thread.start()
    minecraft_threads.append(cheat_thread)

def text_animation(text):#return a list with step by step animation
    symbols = ['*','@','#','$','%','^','&']#symbols to insert to step
    temp = text
    temp+=temp[:1]#fix bug
    shif = []
    for i in range(1,len(temp)+1):#idk what this doing
        shif.append(choice(symbols))
    steps = []
    phrase = []
    for i in range(1,int(len(temp))+1):
        phrase.append(temp[i-1:i])
    x = 0
    for i in phrase:#idk how this work without errors
        shif.pop(x)
        str = ''.join(shif)
        steps.append(str)
        shif.insert(x,i)
        str = ''.join(shif)
        x+=1
    return steps

def label_animation(stringvar: StringVar, text: str):
    for i in text_animation(text):
        stringvar.set(i)
        wait(0.05)

def on_cheat_select(combobox: CTkComboBox, choice: str, cheat_var: StringVar):
    cheat_info = find_cheat(choice).get_all()
    cheat_name = choice + ' Free' if cheat_info['type'] == 'free' else choice + ' Crack By ' + cheat_info['crack_by']
    update_config('cheat', choice)
    # Cheat name animation
    Thread(target=label_animation, args=(cheat_var, cheat_name)).start()

def print_watermark(watermark: str):
    for wm in watermark.split('\n')[1:]:
        print(wm)
        wait(0.05)

def progress_bar_animation(progress_bar: CTkProgressBar):
    for width in range(0, 770+1):
        print(width)
        progress_bar.configure(width)
        wait(0.01)

def download_assets():
    createFolder('./assets')
    
    if not os.path.isfile('./assets/logo.png'):
        download('https://cdn.discordapp.com/attachments/1121892223324278916/1122125098309124126/assets.zip', './', kind='zip', replace=True, progressbar=False, verbose=False)