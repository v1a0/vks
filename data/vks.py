# -*- coding: utf-8 -*-
"""
VKS v 1.1.5
"""

import os
import time
from getpass import getpass
import re
import json

# GET DATA FROM JSON
config = json.load(open('config.json', 'r'))
page_id = config.get("id") if config.get("id") else []
login = config.get("login")
password = config.get("password")
proxy = config.get("proxy")
st = config.get("sleep_time")
install = config.get("install")
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
            "[!] ERROR [!]  \n{0:s}  \n".format(error))

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

        self.conn = sqlite3.connect('data/db/user_{0:s}.db'.format(id))

        if tabname not in self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            self.__init__(tabname)

        self.conn.execute("INSERT INTO {0:s} (HOURS, MINUTES, STATE) \
                VALUES ({1:s}, {2:s}, {3:s})".format(tabname, hours, mins, state))

        # LOGGING
        log("SQL REQ: INSERT INTO {0:s} (HOURS, MINUTES, STATE) \
                VALUES ({1:s}, {2:s}, {3:s})".format(
            tabname, time.strftime("%H"), time.strftime("%M"), state))

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
            with open('data/html/{0:s}.html'.format(self.page_id), 'wb') as page_cache:
                page_cache.write(self.session.get(url, proxies=self.proxies).text.encode('utf-8'))

        except requests.exceptions.ConnectionError as _error:
            # CREATING
            with open('data/html/{0:s}.html'.format(self.page_id), 'w', encoding="utf8") as page_cache:
                page_cache.write(
                    '<meta charset="utf-8"><html><body><h1>CONNECTION ERROR</h1> error 1: Can’t connect to server : '
                    'requests.exceptions.ConnectionError : <a href=\"{0:s}\">URL</a></body></html>'.format(url))
            log(data="Get request of targeted page failed [person.getpage()]", error=_error.__str__())

    # GET 'LAST SEEN' INFO FORM CACHED HTML PAGE
    def getlastseen(self):
        page_cache = open('data/html/{0:s}.html'.format(self.page_id), 'r', encoding="utf8")
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
        page_cache = open('data/html/{0:s}.html'.format(self.page_id), 'r', encoding="utf8")
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
        page_cache = open('data/html/{0:s}.html'.format(self.page_id), 'r', encoding="utf8")
        soup = BeautifulSoup(page_cache, 'lxml')
        try:
            tpl = soup.find('div', class_="owner_panel profile_panel")
            link = re.search(r"https://\S{1,}ava=1", str(tpl)).group()
            req = requests.get(link, stream=True, proxies=self.proxies)
            if req.status_code == 200:
                log("{0:s} --> data/pic/profpic_{1:s}.jpeg".format(link, self.page_id))
                with open('data/pic/profpic_{0:s}.jpeg'.format(self.page_id), 'wb') as file:
                    for chunk in req:
                        file.write(chunk)

        except AttributeError as _error:
            print("{0} {1} : page close or does not exist (can't get profile picture)".format(_error, self.page_id))
            log(data="{0:s} : page close or does not exist (can't get profile picture)".format(self.page_id),
                error=_error.__str__())

    # GET PROFILE INFORMATION
    # tui - temporary user info
    def getinfo(self):
        open('data/info/user_{0:s}.vui'.format(self.page_id), 'w', encoding="utf8").write(self.name + '\n')

        url = 'https://m.vk.com/id{0:s}?act=info'.format(self.page_id)
        page = self.session.get(url, proxies=self.proxies).text.encode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        #tui = soup.find_all('div', class_="profile_info")

        title = ['Name']
        info = [self.name]
        menu = soup.find('div', class_="profile_info_cont").find_all('a')
        eng_ = {"Friends": "Friends",
                      "Друзья": "Friends",
                      "Photos": "Photos",
                      "Фотографии": "Photos",
                      "Videos": "Videos",
                      "Видео": "Videos",
                      "Music": "Music",
                      "Музыка": "Music",
                      "Аудиозаписи": "Music",
                      "Following": "Following",
                      "Подписки": "Following"
                      }

        for i in menu:
                title.append(eng_.get(i.find('div', class_="Menu__itemTitle").text))
                info.append(i.find('div', class_="Menu__itemCount").text)

        try:
            results_ = json.load(open('data/info/user_{0:s}.json'.format(self.page_id), 'r'))
        except FileNotFoundError:
            results_ = dict()
            #data/info/user_23444989.json

        results_.update(zip(title, info))

        with open('data/info/user_{0:s}.json'.format(self.page_id), 'w') as outfile:
            json.dump(results_, outfile)


        #for line in tui:
        #    open('data/info/user_{0:s}.vui'.format(self.page_id), 'a', encoding="utf8").write(str(line))


    def __str__(self):
        return '{0:s}: id = {1:s}, name = "{2:s}", lastseen = "{3:s}"'.format(self.__class__.__name__, self.page_id,
                                                                  self.name, self.lastseen)


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
log("""{0}
    {1:s} : New tracking session : {2:s}""".format(
    '- '*46, time.strftime("%d-%m-%Y %H:%M:%S"), str(page_id)))

log("Proxy settings: {0:s}".format(proxy) if proxy else "(No proxies)")

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
    db.conn = sqlite3.connect('data/db/user_{0:s}.db'.format(target.page_id))
    target.getpage()
    target.getname()
    target.getlastseen()
    target.getprofpic()
    target.getinfo()

    # UI
    if target.lastseen == '2':
        print('Something gose wrong with user id{0:s}...\n'.format(target.page_id),
              'Please, check the id correctness and restart script' if target.name == ''
              else 'Please, restart script and try to login')
        quit()
    else:
        print('Tracking started successfully\nUser: {0}'.format(target.name))

print('Status:')

# MAIN LOOP
while True:
    try:
        etime = time.time()  # ERROR TIME

        for target in p:
            target.getpage()
            target.getlastseen()
            db.add(id=target.page_id.__str__(), hours=time.strftime("%H"), mins=time.strftime("%M"),
                   state=target.lastseen, tabname=time.strftime("T%d_%m_%Y"))

            # UI
            print('{0}  :  {1} ({2})'.format(
                time.strftime("%d-%m-%Y %H:%M:%S"),
                'Online' if target.lastseen == '1' else 'Offline' if target.lastseen == '0' else 'ERROR',
                target.name
            ))

            # LOGGING
            log('{0}  :  {1}'.format(
                time.strftime("%d-%m-%Y %H:%M:%S"),
                target.__str__()
            ))

        # TIME FIXING AND PAUSE
        etime -= time.time()
        time.sleep(st + etime if abs(etime) < st else st)


    except NameError as _error:
        log(error=_error.__str__())
        print("!ERROR\n", _error.__str__())
