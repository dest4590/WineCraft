from time import sleep as wait
from download import download
import inspect
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

cheats = []

def fileList(source): # from stackoverflow, xd
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            matches.append(os.path.join(root, filename))
 
    return matches

def createFolder(folder: str):            
    if not os.path.isdir(folder):
        os.mkdir(folder)

libraries_link = 'https://cdn.discordapp.com/attachments/1042843016316076135/1122174397621469304/libraries.zip'
assets_1_12 = 'https://cdn.discordapp.com/attachments/698068083360792576/1121762450086297620/assets.zip'

natives_link_windows = 'https://cdn.discordapp.com/attachments/1042843016316076135/1122507634763902976/natives.zip'
natives_link_linux = 'https://cdn.discordapp.com/attachments/698068083360792576/1121760302715899955/natives.zip'


jre_linux = 'https://cdn.discordapp.com/attachments/698068083360792576/1121763716703191070/jre_linux.zip'
jre_windows = 'https://cdn.discordapp.com/attachments/1042843016316076135/1122498814981439548/jre_windows.zip'

def find_cheat(name: str):
    for cheat in cheats:
        if cheat['name'] == name:
            return cheat['class']

def run_cheat(name: str, nickname: str, progress_bar):
    class_ = find_cheat(name)
    if type(class_) == Cheat:
        class_.run(nickname, progress_bar)
    elif type(class_) == ForgeCheat:
        class_.run_forge(nickname, progress_bar)

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
            if os.name == 'nt':
                download(natives_link_windows, 'downloads/', kind='zip', replace=True)
            else:
                download(natives_link_linux, 'downloads/', kind='zip', replace=True)
        
        if not os.path.isdir('downloads/assets'):
            animation(0.4, progress_bar)
            os.mkdir('downloads/assets')
            download(assets_1_12, 'downloads/', kind='zip', replace=True)

        if os.name == 'nt':
            if not os.path.isdir('downloads/jre_windows'):
                animation(0.5, progress_bar)
                download(jre_windows, 'downloads/', kind='zip', replace=True)
        else:
            if not os.path.isdir('downloads/jre_linux'):
                animation(0.5, progress_bar)
                download(jre_linux, 'downloads/', kind='zip', replace=True)
        
        if not forge:
            if not os.path.isfile('downloads/' + self.jar):
                if not str(self.link).endswith('.zip'):
                    download(self.link, 'downloads/' + self.jar, replace=True)
                else:
                    download(self.link, 'downloads/', kind='zip', replace=True)

        animation(1, progress_bar)

    def run(self, nickname, progress_bar, custom_params = '', custom_params_java = '', forge = False):
        if self.os == 'windows' and os.name != 'nt':
            print('Error, this cheat only on Windows!')
            return
        
        elif self.os == 'posix' and os.name == 'nt':
            print('Error, this cheat only on linux!')
            return

        self.download(progress_bar, forge)
        
        os.chdir('downloads')
        
        java_bin = 'jre_windows/bin/java' if os.name == 'nt' else 'jre_linux/bin/java' 
        
        if os.name != 'nt': # make chmod +x, fix of Permission denied error
            os.system('chmod +x jre_linux/bin/java')
        if forge:
            self.jar = 'forge_1.12.2.jar'
        
        start_command = f'''{java_bin} -noverify -Xmx2048M -Djava.library.path=./natives/ {custom_params_java} -cp {':'.join(fileList('libraries'))}:{self.jar} {self.main_class} --username {nickname} --version WineCraft --gameDir ./ --assetsDir ./assets --assetIndex 1.12 --uuid N/A --accessToken 0 --userType legacy ''' + custom_params
        #print(start_command)
        progress_bar.set(0)
        os.system(start_command)

        print('Minecraft STOP')
        os.chdir('../')

class ForgeCheat(Cheat):
    indexes = {'1.12.2': 'https://cdn.discordapp.com/attachments/1042843016316076135/1122167783589957642/forge_1.12.2.jar'}
    
    def __init__(self, name, link, jar, type, crack_by, os):
        super().__init__(name, link, jar, type, crack_by, os, 'net.minecraft.launchwrapper.Launch')
    
    def run_forge(self, nickname, progress_bar):
        self.download(progress_bar, True)
        
        createFolder('downloads/mods')

        for mod in fileList('downloads/mods'):
            mod_name = str(os.path.basename(mod).split('/')[-1])
            if mod_name != self.jar and not mod_name.endswith('.disabled') and not mod_name.lower().startswith('optifine'):
                print('Found another mod!')
                os.rename(mod, mod + '.disabled')
            
            elif mod_name.startswith(self.jar) and mod_name.endswith('.disabled'):
                print('Found disabled necessery mod')
                print(str(mod).replace('.disabled'))
                os.rename(mod, str(mod).replace('.disabled'))

        if not os.path.isfile('downloads/mods/' + self.jar):
            download(self.link, 'downloads/mods/' + self.jar)

        if not os.path.isfile('downloads/forge_1.12.2.jar'):
            download(self.indexes['1.12.2'], 'downloads/forge_1.12.2.jar')

        self.run(nickname, progress_bar, '--tweakClass net.minecraftforge.fml.common.launcher.FMLTweaker --versionType Forge', '-Dminecraft.client.jar=forge_1.12.2.jar', True)

rockstar = Cheat('Rockstar', 'https://cdn.discordapp.com/attachments/1070727971515662447/1121882108554653756/RockStarFree.jar', 'RockStarFree.jar', 'free', None, 'any')
celestial = Cheat('Celestial', 'https://cdn.discordapp.com/attachments/1121892223324278916/1121914336248610837/Celestial.zip', 'Celestial.jar', 'crack', 'HCU', 'windows')
rusherhack = ForgeCheat('RusherHack (Forge)', 'https://cdn.discordapp.com/attachments/1042843016316076135/1122165341934592102/rushercrack.jar', 'rushercrack.jar', 'crack', 'PlutoSolutions', 'any')


class progress_bar:
    def get():
        return 2.0
    def set(a):
        return None

rusherhack.run_forge('test', progress_bar)
