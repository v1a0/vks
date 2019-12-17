# -*- coding: utf-8 -*-
import argparse
import os
import time
from getpass import getpass

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# ARGUMENTS
opt = argparse.ArgumentParser(description='Print an argument several times')
opt.add_argument('-id', '--page_id', dest='page_id', type=str,
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
opt.add_argument('-i', '--install', dest='installer', action='store_true',
                 help='Install all necessary for script modules')
args = opt.parse_args()

# MODULES INSTALLING
if args.installer:
    os.system('pip install sqlite3')
    os.system('pip install argparse')
    os.system('pip install bs4')
    os.system('pip install lxml')
    os.system('pip install requests')
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

import sqlite3
import requests
from bs4 import BeautifulSoup

# CREATING DIRECTORIES
os.makedirs('log', exist_ok=True)
os.makedirs('data/html/', exist_ok=True)
os.makedirs('data/db/', exist_ok=True)


# LOGGING FUNCTION
def log(data='', dir='log/log_vks.txt'):
    open(dir, 'a', encoding="utf8").write(data + '\n')


# DATABASE CLASS
class database:
    dbname = 'db'
    conn = sqlite3.connect('data/db/vks.db')

    # CREATING NEW TABLE
    def __init__(self, tablename):
        self.dbname = tablename
        self.conn.execute('CREATE TABLE IF NOT EXISTS ' + tablename + '''
                        (
                        NUM	        INTEGER     NOT NULL    PRIMARY KEY  AUTOINCREMENT UNIQUE,                        
                        TIME        REAL        NOT NULL,
                        STATE       INTEGER         NOT NULL
                        );''')

    # ADDING NEW NOTE
    def add(self, ttime, state):
        # SQLITE REQUEST
        self.conn.execute("INSERT INTO " + self.dbname + " (TIME,STATE) \
        VALUES (" + str(ttime) + ", " + str(state) + ")")

        # LOGGING
        log("SQL REQ: INSERT INTO " + self.dbname + " (TIME,STATE) VALUES (" + str(ttime) + ", " + str(
            state) + ")")
        self.conn.commit()


# PERSON CLASS
class person:
    session = requests.Session()
    page_id = '1'
    name = ''
    lastseen = ''

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

        login_get = self.session.get('https://m.vk.com/login')  # GET REQUEST OF LOGIN PAGE
        soup = BeautifulSoup(login_get.content, 'lxml')  # SOUP
        login_form = soup.find('form')['action']  # FINDING LOGIN FORM
        self.session.post(login_form, data=payload, headers=headers)  # POST REQUEST + SESSION SAVING

    # GET TARGETED PAGE
    def getpage(self):
        url = 'https://vk.com/id' + self.page_id

        # GET REQUEST + CACHING PAGE INTO HTML FILE
        try:
            with open('data/html/' + self.page_id + '.html', 'wb') as page_cache:
                page_cache.write(self.session.get(url).text.encode('utf-8'))
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

# LOGGING
log('- ' * 46 + '\n' + time.strftime("%d-%m-%Y %H:%M:%S") + ' : New tracking session : ' + args.page_id)

# CREATING A TARGET
p = person(page_id=args.page_id)  # SET ID
if args.password != '':  # IF PASSWORD NOT NULL
    p.loginsession(args.login, args.password)  # LOGIN REQUEST + SESSION
    del args.password  # REMOVING PASSWORD FROM MEMORY

p.getpage()
p.getname()
p.getlastseen()
db = database(tablename="user_" + args.page_id)  # CREATING NEW TABLE IN DATABASE

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
    db.add(ttime=time.time(), state=p.lastseen)

    # UI
    print(time.strftime("%d-%m-%Y %H:%M:%S"), ' : ',
          'Online' if p.lastseen == '1' else 'Offline' if p.lastseen == '0' else 'ERROR')

    # LOGGING
    log(time.strftime("%d-%m-%Y %H:%M:%S") + ' : ' + str(p))

    # TIME FIXING AND PAUSE
    etime -= time.time()
    time.sleep(args.ts + etime)
