from glob import glob
import shutil
import os

current_path = os.popen(r'echo %cd%').read().replace('\n', '')
os.chdir(current_path)

splash = '''
 __        _____ _   _ _____ ____ ____      _    _____ _____ 
 \ \      / /_ _| \ | | ____/ ___|  _ \    / \  |  ___|_   _|
  \ \ /\ / / | ||  \| |  _|| |   | |_) |  / _ \ | |_    | |  
   \ V  V /  | || |\  | |__| |___|  _ <  / ___ \|  _|   | |  
    \_/\_/  |___|_| \_|_____\____|_| \_\/_/   \_\_|     |_|  
                                                            BUILDER
'''

class Builder:
    def __init__(self, name) -> None:
        self.name = name

    def build(self):
        print(splash) # omg logo

        os.system(f'''venv\\Scripts\\pyinstaller.exe --noconfirm --onefile --console --icon "assets\\logo.ico" --upx-dir ".\\upx" --name "{self.name}"  --clean --add-data ".\\venv\\Lib\\site-packages\\customtkinter;customtkinter" --add-data ".\\venv\\Lib\\site-packages\\PIL;PIL" --add-data "C:\\Program Files\\Python311\\Lib\\tkinter;tkinter" --exclude-module "pyqt5,pyqt6,pyside2,scipy,pandas,numpy" main.py''')

        [shutil.move(file, './') for file in glob('dist/*')]

Builder('WineCraft Alpha 1.0').build()