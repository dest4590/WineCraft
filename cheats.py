from time import sleep as wait
from download import download
import inspect
import os

cheats = []

def fileList(source, extenstion): # from stackoverflow, xd
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            if str(filename).lower().endswith('.' + extenstion):
                matches.append(os.path.join(root, filename))
    return matches

libraries_link = 'https://cdn.discordapp.com/attachments/1024944244336644096/1121754964079935598/libraries.zip'
assets_1_12 = 'https://cdn.discordapp.com/attachments/698068083360792576/1121762450086297620/assets.zip'

natives_link_windows = ''
natives_link_linux = 'https://cdn.discordapp.com/attachments/698068083360792576/1121760302715899955/natives.zip'


jre_linux = 'https://cdn.discordapp.com/attachments/698068083360792576/1121763716703191070/jre_linux.zip'
jre_windows = ''

def find_cheat(name: str):
    for cheat in cheats:
        if cheat['name'] == name:
            return cheat['class']

def run_cheat(name: str, nickname: str, progress_bar):
    find_cheat(name).run(nickname, progress_bar)

class Cheat:
    def __init__(self, name, link, jar, type, crack_by):
        self.name = name
        self.link = link
        self.jar = jar
        self.type = type
        self.crack_by = crack_by
        cheats.append(self.get_all())
    def get_all(self):
        # костыли
        all_members = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))[1][1] 
        all_members['class'] = self
        return all_members

    def download(self, progress_bar): # downloads libs, natives, etc.
        def animation(num: float):
            list = []
            for i in range(int((num - progress_bar.get()) / 0.1) + 1):
                value = progress_bar.get() + i * 0.1
                list.append(value)
            list.append(num)

            for _ in list:
                progress_bar.set(_)
                wait(0.1)

        if not os.path.isdir('downloads'):
            animation(0.1)
            os.mkdir('downloads')

        if not os.path.isdir('downloads/libraries'):
            animation(0.2)
            os.mkdir('downloads/libraries')
            download(libraries_link, 'downloads/', kind='zip', replace=True)
        
        if not os.path.isdir('downloads/natives'):
            animation(0.3)
            os.mkdir('downloads/natives')
            if os.name == 'nt':
                download(natives_link_windows, 'downloads/', kind='zip', replace=True)
            else:
                download(natives_link_linux, 'downloads/', kind='zip', replace=True)
        
        if not os.path.isdir('downloads/assets'):
            animation(0.4)
            os.mkdir('downloads/assets')
            download(assets_1_12, 'downloads/', kind='zip', replace=True)

        if os.name == 'nt':
            if not os.path.isdir('downloads/jre_windows'):
                animation(0.5)
                download(jre_windows, 'downloads/', kind='zip', replace=True)
        else:
            if not os.path.isdir('downloads/jre_linux'):
                animation(0.5)
                download(jre_linux, 'downloads/', kind='zip', replace=True)

        animation(1)
        download(self.link, 'downloads/' + self.jar)

    def run(self, nickname, progress_bar):
        self.download(progress_bar)
        
        os.chdir('downloads')
        
        java_bin = 'jre_windows/bin/java' if os.name == 'nt' else 'jre_linux/bin/java' 
        
        if os.name != 'nt': # make chmod +x, fix of Permission denied error
            os.system('chmod +x jre_linux/bin/java')

        start_command = f'''{java_bin} -noverify -Xmx2048M -Djava.library.path=./natives/ -cp ./libraries/*:{self.jar} net.minecraft.client.main.Main --username {nickname} --version WineCraft --gameDir ./ --assetsDir ./assets --assetIndex 1.12 --uuid N/A --accessToken 0 --userType mojang'''
        print(start_command)
        os.system(start_command)
        print('Minecraft STOP')
        os.chdir('../')

rockstar = Cheat('Rockstar', 'https://cdn.discordapp.com/attachments/1070727971515662447/1121852131591344209/RockStarFree.jar', 'RockStarFree.jar', 'free', None)
