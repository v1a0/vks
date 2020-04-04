# -*- coding: utf-8 -*-
"""
VKS v 1.1.5
"""

import os
import time
from getpass import getpass
import re
import json
import converter

# GET DATA FROM JSON
config = json.load(open('config.json', 'r'))
page_id = config.get("id") if config.get("id") else []
login = config.get("login")
password = config.get("password")
proxy = config.get("proxy")
st = config.get("sleep_time")
install = config.get("install")
auto_convert = bool(config.get("autoconvert"))
del config

# MODULES INSTALLING
if install == '1':
    os.system('pip install sqlite3')
    os.system('pip install argparse')
    os.system('pip install bs4')
    os.system('pip install lxml')
    os.system('pip install requests')
    os.system('pip install Pillow')
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

import sqlite3
import requests
from bs4 import BeautifulSoup

# CREATING DIRECTORIES
os.makedirs('log', exist_ok=True)
os.makedirs('data/html/', exist_ok=True)
os.makedirs('data/db/', exist_ok=True)
os.makedirs('data/pic/', exist_ok=True)
os.makedirs('data/info/', exist_ok=True)


# LOGGING FUNCTION
def log(data='', dir='log/log_vks.txt', error=''):
    if error:
        open(dir, 'a', encoding="utf8").write(
            f"[!] ERROR [!]  \n{error}  \n")

    open(dir, 'a', encoding="utf8").write(data + '\n')


# DATABASE CLASS
class database:
    conn = sqlite3.connect('')

    # CREATING NEW TABLE
    def __init__(self, tablename):
        self.conn.execute('CREATE TABLE IF NOT EXISTS ' + tablename + '''
                        (
                        NUM	        INTEGER     NOT NULL    PRIMARY KEY  AUTOINCREMENT UNIQUE,                        
                        HOURS       INTEGER     NOT NULL,
                        MINUTES     INTEGER     NOT NULL,
                        STATE       INTEGER     NOT NULL
                        );''')

    # ADDING NEW NOTE
    def add(self, id, tabname, hours, mins, state):
        # SQLITE REQUEST

        self.conn = sqlite3.connect(f'data/db/user_{id}.db')

        if tabname not in self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            self.__init__(tabname)

        self.conn.execute(f"INSERT INTO {tabname} (HOURS, MINUTES, STATE) \
                VALUES ({hours}, {mins}, {state})")

        # LOGGING
        log(f"SQL REQ: INSERT INTO {tabname} (HOURS, MINUTES, STATE) \
                VALUES ({time.strftime('%H')}, {time.strftime('%M')}, {state})")

        self.conn.commit()


# PERSON CLASS
class person:
    session = requests.Session()
    page_id = '1'
    name = ''
    lastseen = ''
    proxies = {}

    # PARAMETERS EDITING
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    # AUTHORISATION
    def loginsession(self, login='', password='', useragent='Mozilla/5.0 (Macintosh; Intel Mac OS X'
                                                            ' 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'):

        log("Login session: login=" + login)
        payload = {
            'act': 'login',
            'email': login,
            'pass': password,
            'role': 'al_frame',
            '_origin': 'https://vk.com'
        }
        headers = {
            "Referer": "https://m.vk.com/login?role=fast&to=&s=1&m=1&email=" + login,
            'User-Agent': useragent
        }

        login_get = self.session.get('https://m.vk.com/login', headers=headers,
                                     proxies=self.proxies)  # GET REQUEST OF LOGIN PAGE
        soup = BeautifulSoup(login_get.content, 'lxml')  # SOUP
        login_form = soup.find('form')['action']  # FINDING LOGIN FORM
        self.session.post(login_form, data=payload, headers=headers,
                          proxies=self.proxies)  # POST REQUEST + SESSION SAVING

    # GET TARGETED PAGE
    def getpage(self):
        url = 'https://vk.com/id' + self.page_id

        # GET REQUEST + CACHING PAGE INTO HTML FILE
        try:
            with open(f'data/html/{self.page_id}.html', 'wb') as page_cache:
                page_cache.write(self.session.get(url, proxies=self.proxies).text.encode('utf-8'))

        except requests.exceptions.ConnectionError as _error:
            # CREATING
            with open(f'data/html/{self.page_id}.html', 'w', encoding="utf8") as page_cache:
                page_cache.write(
                    '<meta charset="utf-8"><html><body><h1>CONNECTION ERROR</h1> error 1: Can’t connect to server : '
                    f'requests.exceptions.ConnectionError : <a href=\"{url}\">URL</a></body></html>')
            log(data="Get request of targeted page failed [person.getpage()]", error=_error.__str__())

    # GET 'LAST SEEN' INFO FORM CACHED HTML PAGE
    def getlastseen(self):
        page_cache = open(f'data/html/{self.page_id}.html', 'r', encoding="utf8")
        soup = BeautifulSoup(page_cache, 'lxml')

        # SEARCHING 'LAST SEEN' INFORMATION (I know it looks disgusting but I'll change it later)
        # tls - temporary last seen note
        try:
            tls = soup.find('span', class_='pp_last_activity_offline_text').next_element
        except AttributeError:
            try:
                tls = soup.find('span', class_='pp_last_activity_text').next_element
            except AttributeError:
                try:
                    tls = soup.find('div', class_='profile_online_lv').next_element
                except AttributeError:
                    tls = 'ERROR'

        self.lastseen = '1' if tls == 'Online' else '2' if tls == 'ERROR' else '0'
        page_cache.close()

    # GET NAME OF TARGETED USER FORM CACHED HTML PAGE
    def getname(self):
        page_cache = open(f'data/html/{self.page_id}.html', 'r', encoding="utf8")
        soup = BeautifulSoup(page_cache, 'lxml')

        # SOUP SEARCHING
        try:
            self.name = soup.find('title').next_element
        except AttributeError as _error:
            self.name = 'error'
            log(error=_error.__str__())

        # LOGGING
        log("Get name request: " + self.name)
        page_cache.close()

    # GET PROFILE PICTURE
    # tpl - temporary picture link
    def getprofpic(self):
        page_cache = open(f'data/html/{self.page_id}.html', 'r', encoding="utf8")
        soup = BeautifulSoup(page_cache, 'lxml')
        try:
            tpl = soup.find('div', class_="owner_panel profile_panel")
            link = re.search(r"https://\S{1,}ava=1", str(tpl)).group()
            req = requests.get(link, stream=True, proxies=self.proxies)
            if req.status_code == 200:
                log(f"{link} --> data/pic/profpic_{self.page_id}.jpeg")
                with open(f'data/pic/profpic_{self.page_id}.jpeg', 'wb') as file:
                    for chunk in req:
                        file.write(chunk)

        except AttributeError as _error:
            print(f"{_error} {self.page_id} : page close or does not exist (can't get profile picture)")
            log(data=f"{self.page_id} : page close or does not exist (can't get profile picture)",
                error=_error.__str__())

    # GET PROFILE INFORMATION
    # tui - temporary user info
    def getinfo(self):
        url = f'https://m.vk.com/id{self.page_id}?act=info'
        page = self.session.get(url, proxies=self.proxies).text.encode('utf-8')
        soup = BeautifulSoup(page, 'lxml')

        page_block = soup.find(class_="PageBlock PageBlock_overflow").__str__()

        try:
            results_ = json.load(open(f'data/info/user_{self.page_id}.json', 'r', encoding='utf8'))
        except FileNotFoundError:
            results_ = dict()

        results_.update({'page_block':page_block})

        with open(f'data/info/user_{self.page_id}.json', 'w', encoding="utf8") as outfile:
            json.dump(results_, outfile)

    def __str__(self):
        return f'{self.__class__.__name__}: id = {self.page_id}, name = "{self.name}", lastseen = "{self.lastseen}"'


# - - - - - - - - - M A I N - - - - - - - - - - - #
os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

# USER INTERFACE (UI)
while not page_id[0]:
    page_id[0] = input('Enter user id: ')

if not login or not password:
    if input("Are you sure you want to continue without authorisation?\n(y/n) : ") == 'n':
        login = input("Enter login: ")
        password = getpass('Enter password: ')

# LOGGING
log(f"""{'- ' * 46}
    {time.strftime("%d-%m-%Y %H:%M:%S")} : New tracking session : {str(page_id)}""")

log(f"Proxy settings: {proxy if proxy else '(No proxies)'}")

# CREATING A TARGET
p = []
for t_id in page_id:
    p.append(person(page_id=t_id, proxies=proxy))  # SET ID

# LOGIN REQUEST + CREATING SESSION
if password:
    p[0].loginsession(login, password)
    del password  # REMOVING PASSWORD FROM MEMORY

db = database(tablename=time.strftime("T%d_%m_%Y"))  # CREATING NEW TABLE IN DATABASE

# FIRST TRY
for target in p:
    target.session = p[0].session
    db.conn = sqlite3.connect(f'data/db/user_{target.page_id}.db')
    target.getpage()
    target.getname()
    target.getlastseen()
    target.getprofpic()
    target.getinfo()

    # UI
    if target.lastseen == '2':
        print(f'Something goes wrong with user id{target.page_id}...\n',
              'Please, check the id correctness and restart script' if target.name == ''
              else 'Please, restart script and try to login')
        quit()
    else:
        print(f'Tracking started successfully\nUser: {target.name}')

print('Status:')

# MAIN LOOP
while True:
    try:
        etime = time.time()  # ERROR TIME

        for target in p:
            target.getpage()
            target.getlastseen()
            db.add(id=target.page_id.__str__(),
                   hours=time.strftime("%H"),
                   mins=time.strftime("%M"),
                   state=target.lastseen,
                   tabname=time.strftime("T%d_%m_%Y"))

            # UI
            online_status = 'Online' if target.lastseen == '1' else 'Offline' if target.lastseen == '0' else 'ERROR'
            current_time = time.strftime("%d-%m-%Y %H:%M:%S")
            print(f"""{current_time}  :  {online_status} ({target.name})""")

            # LOGGING
            log(f'{current_time}  :  {target.__str__()}')

        if auto_convert: converter.convert(log=False)

        # TIME FIXING AND PAUSE
        etime -= time.time()
        time.sleep(st + etime if abs(etime) < st else st)

    except NameError as _error:
        log(error=_error.__str__())
        print("!ERROR\n", _error.__str__())
        converter.convert()
