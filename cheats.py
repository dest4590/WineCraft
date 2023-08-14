from time import sleep as wait
from download import download
import os

cheats = []

def createFolder(folder: str):            
    if not os.path.isdir(folder):
        os.mkdir(folder)

libraries_link = 'https://cdn.discordapp.com/attachments/1042843016316076135/1122174397621469304/libraries.zip'
assets_1_12 = 'https://cdn.discordapp.com/attachments/698068083360792576/1121762450086297620/assets.zip'

natives_link_windows = 'https://cdn.discordapp.com/attachments/1042843016316076135/1140629553006510100/natives.zip'

jre_windows = 'https://cdn.discordapp.com/attachments/1042843016316076135/1122498814981439548/jre_windows.zip'

def find_cheat(name: str):
    for cheat in cheats:
        if cheat['name'] == name:
            return cheat['class']

def run_cheat(name: str, nickname: str, progress_bar):
    class_ = find_cheat(name)
    class_.run(nickname, progress_bar)

def animation(num: float, progress_bar):
    list = []
    for i in range(int((num - progress_bar.get()) / 0.1) + 1):
        value = progress_bar.get() + i * 0.1
        list.append(value)
    list.append(num)

    for _ in list:
        progress_bar.set(_)
    wait(0.1)

class Cheat:
    def __init__(self, name, link, jar, type, crack_by, os, main_class = 'net.minecraft.client.main.Main'):
        self.name = name
        self.link = link
        self.jar = jar
        self.type = type
        self.crack_by = crack_by
        self.main_class = main_class
        self.os = os
        cheats.append(self.get_all())
    def get_all(self):
        # костыли
        all_members = {
            'name': self.name,
            'link': self.link,
            'jar': self.jar,
            'type': self.type,
            'crack_by': self.crack_by,
            'main_class': self.main_class,
            'os': self.os,
            'class': self
        }
        return all_members

    def download(self, progress_bar, forge): # downloads libs, natives, etc.
        if not os.path.isdir('downloads'):
            animation(0.1, progress_bar)
            os.mkdir('downloads')

        if not os.path.isdir('downloads/libraries'):
            animation(0.2, progress_bar)
            os.mkdir('downloads/libraries')
            download(libraries_link, 'downloads/', kind='zip', replace=True)
        
        if not os.path.isdir('downloads/natives'):
            animation(0.3, progress_bar)
            os.mkdir('downloads/natives')
            download(natives_link_windows, 'downloads/', kind='zip', replace=True)

        
        if not os.path.isdir('downloads/assets'):
            animation(0.4, progress_bar)
            os.mkdir('downloads/assets')
            download(assets_1_12, 'downloads/', kind='zip', replace=True)

        if not os.path.isdir('downloads/jre_windows'):
            animation(0.5, progress_bar)
            download(jre_windows, 'downloads/', kind='zip', replace=True)
        
        if not forge:
            if not os.path.isfile('downloads/' + self.jar):
                if not str(self.link).endswith('.zip'):
                    download(self.link, 'downloads/' + self.jar, replace=True)
                else:
                    download(self.link, 'downloads/', kind='zip', replace=True)

        animation(1, progress_bar)

    def run(self, nickname, progress_bar, custom_params = '', custom_params_java = '', forge = False):
        self.download(progress_bar, forge)
        
        java_bin = 'jre_windows\\bin\\java.exe'
        
        os.chdir('downloads')

        if forge:
            self.jar = 'forge_1.12.2.jar'
        
        start_command = f'''{java_bin} -noverify -Xmx2048M -Djava.library.path=natives; {custom_params_java} -cp libraries\*;{self.jar} {self.main_class} --username {nickname} --version WineCraft --gameDir .\\ --assetsDir .\\assets --assetIndex 1.12 --uuid N/A --accessToken 0 --userType legacy ''' + custom_params
        
        progress_bar.set(0)
        os.system(start_command)

        print('Minecraft STOP')
        os.chdir('.\\')

rockstar = Cheat('Rockstar', 'https://cdn.discordapp.com/attachments/1070727971515662447/1121882108554653756/RockStarFree.jar', 'RockStarFree.jar', 'free', None, 'any')
celestial = Cheat('Celestial', 'https://cdn.discordapp.com/attachments/1121892223324278916/1121914336248610837/Celestial.zip', 'Celestial.jar', 'crack', 'HCU', 'windows')

#'''
class progress_bar:
    def get():
        return 2.0
    def set(a):
        return None

#rockstar.run('Purpl3_YT', progress_bar)
#celestial.run('Purpl3_YT', progress_bar)
#'''
