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

    def download(self): # downloads libs, natives, etc.
        if not os.path.isdir('downloads'):
            os.mkdir('downloads')

        if not os.path.isdir('downloads/libraries'):
            os.mkdir('downloads/libraries')
            download(libraries_link, 'downloads/', kind='zip', replace=True)
        
        if not os.path.isdir('downloads/natives'):
            os.mkdir('downloads/natives')
            if os.name == 'nt':
                download(natives_link_windows, 'downloads/', kind='zip', replace=True)
            else:
                download(natives_link_linux, 'downloads/', kind='zip', replace=True)
        
        if not os.path.isdir('downloads/assets'):
            os.mkdir('downloads/assets')
            download(assets_1_12, 'downloads/', kind='zip', replace=True)

        if os.name == 'nt':
            if not os.path.isdir('downloads/jre_windows'):
                download(jre_windows, 'downloads/', kind='zip', replace=True)
        else:
            if not os.path.isdir('downloads/jre_linux'):
                download(jre_linux, 'downloads/', kind='zip', replace=True)

        download(self.link, 'downloads/' + self.jar)

    def run(self, nickname):
        self.download()

        libraries_folder = 'downloads/libraries/' # тут либы от 1.12.2
        #print(f'java -noverify -Xmx2048M -Djava.library.path=downloads/natives -cp {libraries_folder}*;downloads/{self.jar} net.minecraft.client.main.Main --username {nickname} --version WineCraft --gameDir downloads/ --assetsDir ./downloads/assets --assetIndex 1.12 --uuid N/A --accessToken 0 --userType mojang')
        
        os.chdir('downloads')
        
        #java_bin = 'jre_windows/bin/java' if os.name == 'nt' else 'jre_linux/bin/java' 
        java_bin = 'java'
        if os.name == 'posix': # make chmod +x, fix of Permission denied
            os.system('chmod +x jre_linux/bin/java')

        start_command = f'''{java_bin} -noverify -Xmx2048M -Djava.library.path=natives/ -cp {':'.join(fileList('libraries', 'jar'))}:{self.jar} net.minecraft.client.main.Main --username {nickname} --version WineCraft --gameDir ./ --assetsDir assets --assetIndex 1.12 --uuid N/A --accessToken 0 --userType mojang'''
        print(start_command)
        os.system(start_command)
        os.chdir('../')

norender = Cheat('NoRender', 'https://cdn.discordapp.com/attachments/698068083360792576/1121757384914784278/NoRenderCrack.jar', 'NoRenderCrack.jar', 'crack', 'HCU')
osium = Cheat('Osium', 'link', '123123', 'crack','WhiteWhess')

norender.run('Purpl3_YT')