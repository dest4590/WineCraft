import customtkinter as cs
from tkinter import ttk
from functions import *
from cheats import cheats
from threading import Thread
from config import init, read_config, write_config, get_value
import random

default_cheat = cheats[0]['name']

init(default_cheat)

cheat = read_config()['cheat']

if cheat not in [v['name'] for v in cheats]:
    cheat = 'NoRender'

class App(cs.CTk):
    def __init__(self):
        super().__init__()

        app = self

        self.title('WineCraft - New era of WineLauncher')
        self.geometry('800x430')
        app.grid_columnconfigure(4, weight=1)
        app.grid_rowconfigure(5, weight=1)


        # Banner
        self.banner_var = StringVar()
        self.banner_var.set('')
        self.banner = cs.CTkLabel(app, font=cs.CTkFont('Bahnschrift', 25), textvariable=self.banner_var)
        self.banner.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
        
        # Banner animation
        Thread(target=label_animation, args=(self.banner_var, 'WineCraft')).start()

        # Cheats combobox
        self.cheats_box = cs.CTkComboBox(app, values=[v['name'] for v in cheats], state='readonly', font=cs.CTkFont('Bahnschrift', 16), command=lambda choice:on_cheat_select(self.cheats_box, choice, self.cheat_var), dropdown_font=cs.CTkFont('Bashscrift', 16))
        self.cheats_box.set(cheat)
        self.cheats_box.grid(row=1, column=0, padx=10, sticky='nw')


        self.cheat_var = StringVar()
        self.cheat_var.set('')
        self.cheat_name = cs.CTkLabel(app, font=cs.CTkFont('Bahnschrift', 25), textvariable=self.cheat_var)
        self.cheat_name.grid(row=3, column=0, padx=10, pady=10, sticky='nw')

        # Nickname input
        config_nickname = get_value('nickname')
        if not config_nickname: # если ника нету
            config_nickname = 'WineCraft_User' + str(random.randint(1000, 9999))

        self.nickname = cs.CTkEntry(app, 620, 40, font=cs.CTkFont('Bahnschrift', 16))
        self.nickname.insert(0, config_nickname)
        self.nickname.grid(row=999, column=0, sticky='w', padx=10, pady=10)

        # Start button
        self.start_button = cs.CTkButton(app, text='Start', command=lambda:start_cheat(app, self.start_button, self.nickname), font=cs.CTkFont('Arial', 20), cursor='hand1')
        self.start_button.grid(row=999, column=999, padx=10, pady=10, sticky='e')



app = App()
app.mainloop()