# -*- coding: utf-8 -*-
import argparse
import os
import time
from getpass import getpass
import re


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# ARGUMENTS
opt = argparse.ArgumentParser(description='Print an argument several times')
opt.add_argument('-i', '--page_id', dest='page_id', type=str,
                 default='', metavar='1234567890',
                 help='Enter id of page (for analysis)')
opt.add_argument('-l', '--login', dest='login', type=str,
                 default='', metavar='+71234567890',
                 help='Enter login data (email or phone number)')
opt.add_argument('-p', '--password', dest='password', type=str,
                 default='', metavar='pwned1234',
                 help='Enter login data (password)')
opt.add_argument('-t', '--timesleep', dest='ts', type=int,
                 default='60', metavar='60',
                 help='Request frequency [sec] (default = 60)')
opt.add_argument('-in', '--install', dest='installer', action='store_true',
                 help='Install all necessary for script modules')
opt.add_argument('-x', '--proxy', dest='proxy', type=str,
                 default='', metavar='https://10.10.1.0:8080',
                 help='Proxies settings to connect. Use format "[type]://[ip]:[port]"')
args = opt.parse_args()

# MODULES INSTALLING
if args.installer:
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
def log(data='', dir='log/log_vks.txt'):
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
    def add(self, tabname, hours, mins, state):
        # SQLITE REQUEST

        if tabname not in self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            self.__init__(tabname)

        self.conn.execute("INSERT INTO " + tabname + " (HOURS, MINUTES, STATE) \
        VALUES (" + hours + ", " + mins + ", " + str(state) + ")")

        # LOGGING
        log("SQL REQ: INSERT INTO " + tabname + " (HOURS, MINUTES, STATE) \
        VALUES (" + time.strftime("%H") + ", " + time.strftime("%M") + ", " + str(state) + ")")
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

        login_get = self.session.get('https://m.vk.com/login', headers=headers, proxies=self.proxies)  # GET REQUEST OF LOGIN PAGE
        soup = BeautifulSoup(login_get.content, 'lxml')  # SOUP
        login_form = soup.find('form')['action']  # FINDING LOGIN FORM
        self.session.post(login_form, data=payload, headers=headers, proxies=self.proxies)  # POST REQUEST + SESSION SAVING

    # GET TARGETED PAGE
    def getpage(self):
        url = 'https://vk.com/id' + self.page_id

        # GET REQUEST + CACHING PAGE INTO HTML FILE
        try:
            with open('data/html/' + self.page_id + '.html', 'wb') as page_cache:
                page_cache.write(self.session.get(url, proxies=self.proxies).text.encode('utf-8'))
        except requests.exceptions.ConnectionError:
            # CREATING
            with open('data/html/' + self.page_id + '.html', 'w', encoding="utf8") as page_cache:
                page_cache.write(
                    '<meta charset="utf-8"><html><body><h1>CONNECTION ERROR</h1> error 1: Can’t connect to server : '
                    'requests.exceptions.ConnectionError : <a href=\"' + url + '\">URL</a></body></html>')
            log("Get request of targeted page failed [person.getpage()]")

    # GET 'LAST SEEN' INFO FORM CACHED HTML PAGE
    def getlastseen(self):
        page_cache = open('data/html/' + self.page_id + '.html', 'r', encoding="utf8")
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
        page_cache = open('data/html/' + self.page_id + '.html', 'r', encoding="utf8")
        soup = BeautifulSoup(page_cache, 'lxml')

        # SOUP SEARCHING
        try:
            self.name = soup.find('title').next_element
        except AttributeError:
            self.name = 'error'

        # LOGGING
        log("Get name request: " + self.name)
        page_cache.close()

    # GET PROFILE PICTURE
    # tpl - temporary picture link
    def getprofpic(self):
        page_cache = open('data/html/' + self.page_id + '.html', 'r', encoding="utf8")
        soup = BeautifulSoup(page_cache, 'lxml')
        try:
            tpl = soup.find('div', class_="owner_panel profile_panel")
            link = re.search(r'https://\S{1,}ava=1', str(tpl)).group()
            req = requests.get(link, stream=True, proxies=self.proxies)
            if req.status_code == 200:
                log(link + " --> " + 'data/pic/profpic_' + str(self.page_id) + '.jpeg')
                with open('data/pic/profpic_' + str(self.page_id) + '.jpeg', 'wb') as file:
                    for chunk in req:
                        file.write(chunk)

        except AttributeError:
            print(self.page_id + " : page close or does not exist (can't get profile picture)")
            log(self.page_id + " : page close or does not exist (can't get profile picture)")

    # GET PROFILE INFORMATION
    # tui - temporary user info
    def getinfo(self):
        open('data/info/user_' + str(self.page_id) + '.vui', 'w', encoding="utf8").write(self.name + '\n')

        url = 'https://m.vk.com/id' + self.page_id + '?act=info'
        page = self.session.get(url, proxies=self.proxies).text.encode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        tui = soup.find_all('div', class_="profile_info")

        for line in tui:
            open('data/info/user_' + str(self.page_id) + '.vui', 'a', encoding="utf8").write(str(line))




    def __str__(self):
        return '{}: id = {}, name = "{}", lastseen = "{}"'.format(self.__class__.__name__, self.page_id,
                                                                  self.name, self.lastseen)


# - - - - - - - - - M A I N - - - - - - - - - - - #
os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

# USER INTERFACE (UI)
while args.page_id == '':
    args.page_id = input('Enter user id: ')

if args.login == '' or args.password == '':
    if input("Are you sure you want to continue without authorisation?\n(y/n) : ") == 'n':
        args.login = input("Enter login: ")
        args.password = getpass('Enter password: ')

# PROXY SET
proxy = {}
if 'https' in args.proxy:
    proxy.update({'https': args.proxy})
else:
    if 'http' in args.proxy:
        proxy.update({'http': args.proxy})
if 'ftp' in args.proxy:
    proxy.update({'ftp': args.proxy})

# LOGGING
log('- ' * 46 + '\n' + time.strftime("%d-%m-%Y %H:%M:%S") + ' : New tracking session : ' + args.page_id)
log("Proxy settings:" + str(proxy)) if proxy else log("(No proxies)")

# CREATING A TARGET
p = person(page_id=args.page_id, proxies=proxy)  # SET ID
if args.password != '':  # IF PASSWORD NOT NULL
    p.loginsession(args.login, args.password)  # LOGIN REQUEST + SESSION
    del args.password  # REMOVING PASSWORD FROM MEMORY

p.getpage()
p.getname()
p.getlastseen()
p.getprofpic()
p.getinfo()

db = database(tablename=time.strftime("T%d_%m_%Y"))  # CREATING NEW TABLE IN DATABASE
db.conn = sqlite3.connect('data/db/user_' + p.page_id + '.db')

# UI
if p.lastseen == '2':
    print('Something gose wrong...\n',
          'Please, check the id correctness and restart script' if p.name == ''
          else 'Please, restart script and try to login')
    quit()
else:
    print('Tracking started successfully\nUser: ' + p.name + '\nStatus:')

# MAIN LOOP
while True:
    etime = time.time()  # ERROR TIME
    p.getpage()
    p.getlastseen()
    db.add(hours=time.strftime("%H"), mins=time.strftime("%M"),
           state=p.lastseen, tabname=time.strftime("T%d_%m_%Y"))

    # UI
    print(time.strftime("%d-%m-%Y %H:%M:%S"), ' : ',
          'Online' if p.lastseen == '1' else 'Offline' if p.lastseen == '0' else 'ERROR')

    # LOGGING
    log(time.strftime("%d-%m-%Y %H:%M:%S") + ' : ' + str(p))

    # TIME FIXING AND PAUSE
    etime -= time.time()
    time.sleep(args.ts + etime if abs(etime) < args.ts else args.ts)
