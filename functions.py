from time import sleep as wait
from customtkinter import CTk, CTkButton, CTkLabel, StringVar, CTkComboBox, CTkEntry, CTkProgressBar
from random import choice
from config import update_config
from cheats import find_cheat, run_cheat
from threading import Thread

def start_cheat(app: CTk, start_button: CTkButton, nickname: CTkEntry, combobox: CTkComboBox, progress_bar: CTkProgressBar):
    print('start cheat')

    update_config('nickname', nickname.get())

    # start cheat in new thread
    cheat_thread = Thread(target=run_cheat, args=(combobox.get(), nickname.get(), progress_bar))
    cheat_thread.start()

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
    cheat_name = choice if cheat_info['type'] == 'free' else choice + ' By ' + cheat_info['crack_by']
    update_config('cheat', choice)
    # Cheat name animation
    Thread(target=label_animation, args=(cheat_var, cheat_name)).start()