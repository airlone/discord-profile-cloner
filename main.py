import requests
import asyncio
import sys
import os
import threading
import time
import json
from typing import Union
import base64

os.system('')

os.system('cls' if os.name == 'nt' else 'clear')
token = input("\x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mToken  -  ")

headers = {
    'Authorization': token,
    
}

def printf(text:str):
    if 'failed' in text.lower():
       
        return print(f"                                       \x1b[38;5;56m(\033[37m-\x1b[38;5;56m) \033[37m{text}")
    else:
        return print(f"                                       \x1b[38;5;201m(\033[37m+\x1b[38;5;201m) \033[37m{text}")

class User:
    def __init__(self, user_id:str):
        r = requests.get(f'https://discord.com/api/v9/users/{user_id}/profile?with_mutual_guilds=true&with_mutual_friends_count=false', headers=headers)
        
        self.data = r.json()
        
    @property
    def global_name(self) -> str:
        return self.data['user']['global_name']
        
    @property
    def avatar_url(self) -> str:
        exten = None
        if self.data['user']['avatar'] == None:
            return None
            
        avatar = self.data['user']['avatar']
        if avatar.startswith('a_'):
            exten = '.gif'
        else:
            exten = '.png'        
        return 'https://cdn.discordapp.com/avatars/' + self.data['user']['id'] + '/' + self.data['user']['avatar'] + exten + '?size=1024'
        
    @property
    def banner_url(self) -> str:
        exten = None
        if self.data['user']['banner'] == None:
            return None
            
        banner = self.data['user']['banner']
        if banner.startswith('a_'):
            exten = '.gif'
        else:
            exten = '.png'        
        return 'https://cdn.discordapp.com/banners/' + self.data['user']['id'] + '/' + self.data['user']['banner'] + exten + '?size=1024'
        
    @property
    def bio(self) -> str:
        return self.data["user_profile"]["bio"]
     
    @property
    def banner_color(self) -> Union[str, int, list]:
        return self.data["user"]["banner_color"]
        
    @property
    def accent_color(self) -> Union[str, int, list]:
        return self.data["user"]["accent_color"]

    @property
    def theme_color(self) -> Union[int, list]:
    
        theme_colors = None
        if self.data["premium_type"] == None:
            theme_colors = [0,0]
        elif self.data["premium_type"] == 2:
            theme_colors = self.data['user_profile']['theme_colors']
        else:
            theme_colors = [0,0]
            
        return theme_colors
        
    @property
    def hype_squad(self) -> str:
        hype_squad = None
    
        if self.data["badges"][0]["id"] == 'hypesquad_house_1':
            hype_squad = '1'
            
        elif self.data["badges"][0]["id"] == 'hypesquad_house_2':
            hype_squad = '2'
        elif self.data["badges"][0]["id"] == 'hypesquad_house_3':
            hype_squad = '3'
        else:
            hype_squad = None
        
        return hype_squad        
     
class Downloader:

    
     
    def download(self, type:str, url):
        if type == "avatar":
            if url != None:
                exten = 'gif' if url.split('/')[5].startswith('a_') else 'png'
                f = requests.get(url) 
                with open(f'assets/avatars/{url.split("/")[5].split(".")[0]}.{exten}', 'wb') as d:
                    d.write(f.content)
                with open(f'assets/avatars/{url.split("/")[5].split(".")[0]}.{exten}', 'rb') as ifile:
                    encoded_str = base64.b64encode(ifile.read())
                return f"data:image/{exten};base64,{(encoded_str.decode('utf-8'))}"
                
        elif type == "banner":
            if url != None:
                exten = 'gif' if url.split('/')[5].startswith('a_') else 'png'
                f = requests.get(url) 
                with open(f'assets/banners/{url.split("/")[5].split(".")[0]}.{exten}', 'wb') as d:
                    d.write(f.content)
                with open(f'assets/banners/{url.split("/")[5].split(".")[0]}.{exten}', 'rb') as ifile:
                    encoded_str = base64.b64encode(ifile.read())
                return f"data:image/{exten};base64,{(encoded_str.decode('utf-8'))}"
                
        else:
            raise SyntaxError  # lol
    
    def clear_paths(self):
        try:
            for file in os.listdir('assets/avatars'):
                file_path = os.path.join('assets/avatars', file)
                os.remove(file_path)
                
            for file in os.listdir('assets/banners'):
                file_path = os.path.join('assets/banners', file)
                os.remove(file_path)
        except:
            pass 

                

class Cloner:
    def __init__(self, user_id:str):
        self.user = User(user_id)
        self.downloader = Downloader()
        
    def copy_avatar(self):
        url = self.user.avatar_url
        if url == None:
            return requests.patch(f'https://discord.com/api/v9/users/@me', headers=headers, json={'avatar': None})
            
            
        
        base = self.downloader.download("avatar", url)
        
        r = requests.patch(f'https://discord.com/api/v9/users/@me', headers=headers, json={'avatar': base})
        if r.status_code == 200:
            return printf('Changed pfp')
            
        else:
            return printf('Failed to change pfp')
            
    def copy_banner_color(self):
        color = self.user.banner_color
        
        r = requests.patch(f'https://discord.com/api/v9/users/@me', headers=headers, json={'banner_color': color})
        if r.status_code == 200:
            return printf('Changed banner color')
        else:
            return printf('Failed to change banner color')
            
    def copy_accent_color(self):
        color = self.user.accent_color
        
        r = requests.patch(f'https://discord.com/api/v9/users/@me/profile', headers=headers, json={'accent_color': color})
        if r.status_code == 200:
            return printf('Changed accent color')
        else:
            return printf('Failed to change accent color')
            
    def copy_theme_colors(self):
        colors = self.user.theme_color
        
        r = requests.patch(f'https://discord.com/api/v9/users/@me/profile', headers=headers, json={'theme_colors': colors})
        if r.status_code == 200:
            return printf('Changed theme colors')
        else:
            return printf('Failed to theme colors')
            
    def copy_banner(self):
        url = self.user.banner_url
        if url == None:
            return requests.patch(f'https://discord.com/api/v9/users/@me/profile', headers=headers, json={'banner': None})
            
            
        downloader = Downloader()
        base = self.downloader.download("banner", url)
        
        r = requests.patch(f'https://discord.com/api/v9/users/@me/profile', headers=headers, json={'banner': base})
        if r.status_code == 200:
            return printf('Changed banner')
            
        else:
            return printf('Failed to change banner')
            
            
    def copy_bio(self):
        bio = self.user.bio
        
        r = requests.patch(f'https://discord.com/api/v9/users/@me/profile', headers=headers, json={'bio': bio})
        
        if r.status_code == 200:
            return printf('Changed bio')
            
        else:
            return printf('Failed to change bio')
            
    def copy_global_name(self):
        name = self.user.global_name
        
        r = requests.patch(f'https://discord.com/api/v9/users/@me', headers=headers, json={'global_name': name})
        
        if r.status_code == 200:
            return printf('Changed name')
            
        else:
            return printf('Failed to change name')
        
    def copy_hype_squad(self):
        badge = self.user.hype_squad
        
        if badge == None:
            return requests.delete('https://discord.com/api/v9/hypesquad/online', headers=headers, json={'house_id': None})
            
        r = requests.post('https://discord.com/api/v9/hypesquad/online', headers=headers, json={'house_id': badge})
        if r.status_code == 204:
            return printf('Changed hypesquad')
            
        else:
            return printf('Failed to change hypesquad')
       
async def mainobj():
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('title made by: a1rlone')
    
    
    print('''
                                               \x1b[38;5;201m    ┌┐ ┬ ┬┌─┐┌─┐
                                                   ├┴┐└┬┘│  ├┤ 
                                                   └─┘ ┴ └─┘└─┘
        
                                       \x1b[38;5;201m(\033[37m1\x1b[38;5;201m) \033[37mCopy avatar       \x1b[38;5;201m(\033[37m5\x1b[38;5;201m) \033[37mCopy name
                                       \x1b[38;5;201m(\033[37m2\x1b[38;5;201m) \033[37mCopy banner       \x1b[38;5;201m(\033[37m6\x1b[38;5;201m) \033[37mCopy hypesquad
                                       \x1b[38;5;201m(\033[37m3\x1b[38;5;201m) \033[37mCopy theme        \x1b[38;5;201m(\033[37m7\x1b[38;5;201m) \033[37mCopy accent color    
                                       \x1b[38;5;201m(\033[37m4\x1b[38;5;201m) \033[37mCopy bio          \x1b[38;5;201m(\033[37m8\x1b[38;5;201m) \033[37mCopy banner color
                      
                                                 \x1b[38;5;201m(\033[37m9\x1b[38;5;201m) \033[37mCopy all
    
    ''')
    
    choice = input("                                       \x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mchoose  -  ")
    
    if choice == "1":
        user_id = input("                                       \x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mUser Id  -  ")
        cloner = Cloner(user_id)
        threading.Thread(target=cloner.copy_avatar).start()
        await asyncio.sleep(2)
        await mainobj()
        
    elif choice == "2":
        user_id = input("                                       \x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mUser Id  -  ")
        cloner = Cloner(user_id)
        threading.Thread(target=cloner.copy_banner).start()
        await asyncio.sleep(2)
        await mainobj()
        
    elif choice == "3":
        user_id = input("                                       \x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mUser Id  -  ")
        cloner = Cloner(user_id)
        threading.Thread(target=cloner.copy_theme_colors).start()
        await asyncio.sleep(2)
        await mainobj()
        
    elif choice == "4":
        user_id = input("                                       \x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mUser Id  -  ")
        cloner = Cloner(user_id)
        threading.Thread(target=cloner.copy_bio).start()
        await asyncio.sleep(2)
        await mainobj()
        
    elif choice == "5":
        user_id = input("                                       \x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mUser Id  -  ")
        cloner = Cloner(user_id)
        threading.Thread(target=cloner.copy_global_name).start()
        await asyncio.sleep(2)
        await mainobj()
        
    elif choice == "6":
        user_id = input("                                       \x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mUser Id  -  ")
        cloner = Cloner(user_id)
        threading.Thread(target=cloner.copy_hype_squad).start()
        await asyncio.sleep(2)
        await mainobj()
        
    elif choice == "7":
        user_id = input("                                       \x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mUser Id  -  ")
        cloner = Cloner(user_id)
        threading.Thread(target=cloner.copy_accent_color).start()
        await asyncio.sleep(2)
        await mainobj()    
        
    elif choice == "8":
        user_id = input("                                       \x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mUser Id  -  ")
        cloner = Cloner(user_id)
        threading.Thread(target=cloner.copy_banner_color).start()
        await asyncio.sleep(2)
        await mainobj()

    elif choice == "9":
        user_id = input("                                       \x1b[38;5;56m(\033[37m?\x1b[38;5;56m) \033[37mUser Id  -  ")
        cloner = Cloner(user_id)
        threads = []
        def cyc():

            cloner.copy_avatar()
            cloner.copy_hype_squad()
            cloner.copy_banner()
            cloner.copy_bio()
            cloner.copy_banner_color()
            cloner.copy_accent_color()
            cloner.copy_theme_colors()
            cloner.copy_global_name()
            
        
            
        t1 = threading.Thread(target=cyc)
        t1.start()
        t1.join()
        time.sleep(2)
        await mainobj()   

    else:
        await asyncio.sleep(1)
        await mainobj()        
    
if __name__ == "__main__":
    download = Downloader()
    download.clear_paths() 
    asyncio.run(mainobj())
