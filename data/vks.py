# -*- coding: utf-8 -*-
"""
VKS v 1.1.9
"""

import os
import time
from getpass import getpass
import json
import converter
from rand_header import *
from getproxy import *

# GET DATA FROM JSON
config = json.load(open('config.json', 'r'))
page_id = config.get("id") if config.get("id") else []
login = config.get("login")
password = config.get("password")
proxy = config.get("proxy")
st = config.get("sleep_time")
install = config.get("install")
rand_proxy = bool(config.get("rand_proxy"))
rand_header = bool(config.get("rand_header"))
debug = bool(config.get("debug"))
auto_convert = bool(config.get("autoconvert"))
del config

# MODULES INSTALLING
if install == '1':
    if os.name == 'nt':
        os.system('''
                    pip install sqlite3
                    pip install lxml
                    pip install requests
                    pip install Pillow
                    ''')
    else:
        print("read install.py")
        quit()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

import sqlite3
import requests
from lxml import etree
import lxml.html as lx

# CREATING DIRECTORIES
os.makedirs('log', exist_ok=True)
os.makedirs('data', exist_ok=True)
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
    page = ''
    page_info = ''
    links = {"pp_img": "",
             "f0_img": "",
             "f1_img": "",
             "f2_img": ""
             }

    # PARAMETERS EDITING
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    # AUTHORISATION
    def loginsession(self, login='', password=''):

        log("Login session: login=" + login)
        payload = {
            'act': 'login',
            'email': login,
            'pass': password,
            'role': 'al_frame',
            '_origin': 'https://vk.com'
        }
        headers = randheader.get(upd={'Referer': 'https://m.vk.com/login?role=fast&to=&s=1&m=1&email=' + login})\
            if rand_header else {
            'Referer': 'https://m.vk.com/login?role=fast&to=&s=1&m=1&email=' + login,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'}

        login_get = self.session.get('https://m.vk.com/login', headers=headers,
                                     proxies=self.proxies)  # GET REQUEST OF LOGIN PAGE

        self.page = lx.fromstring(login_get.content)
        login_form = self.page.xpath('//form/@action')[0]

        self.session.post(login_form, data=payload, headers=headers,
                          proxies=self.proxies)  # POST REQUEST + SESSION SAVING

    # GET TARGETED PAGE
    def getpage(self):
        url = f'https://vk.com/id{self.page_id}'
        self.page = lx.fromstring(self.session.get(url, proxies=self.proxies).content)

        # GET REQUEST + CACHING PAGE INTO HTML FILE
        # XX
        if debug:
            try:
                with open(f'data/html/{self.page_id}.html', 'wb') as page_cache:
                    page_cache.write(self.session.get(url, proxies=self.proxies).text.encode('utf-8'))

            except requests.exceptions.ConnectionError as _error:
                log(data="Get request of targeted page failed [person.getpage()]", error=_error.__str__())

    # SCRAPPING 'LAST SEEN' INFORMATION
    def getlastseen(self):
        try:
            lastseen_str = \
                self.page.xpath('//div[@class="pp_last_activity"]/'
                                'span[@class="pp_last_activity_offline_text"]')[0].text_content()
        except IndexError:
            try:
                lastseen_str = self.page.xpath('//div[@class="pp_last_activity"]/'
                                               'span[@class="pp_last_activity_text"]')[0].text_content()
            except IndexError:
                try:
                    lastseen_str = self.page.xpath('//div[@class="pp_last_activity"]/'
                                                   'span[@class="profile_online_lv"]')[0].text_content()
                except IndexError:
                    lastseen_str = 'ERROR'
        self.lastseen = '1' if lastseen_str == 'Online' else '2' if lastseen_str == 'ERROR' else '0'

    # GET NAME OF TARGETED USER FORM CACHED HTML PAGE
    def getname(self):

        try:
            self.name = self.page.xpath('//div[@class="pp_cont"]/h2[@class="op_header"]')[0].text_content()
        except IndexError as _error:
            self.name = 'error'
            log(error=_error.__str__())

        # LOGGING
        log(f"Name ({self.page_id}): {self.name}")

    # GET PROFILE PICTURE
    # tpl - temporary picture link
    def getprofpics(self):
        try:
            link2pic = self.page.xpath('//div[@class="owner_panel profile_panel"]//a//'
                                       'img[@class="pp_img"]/@src')[0]
            req = requests.get(link2pic, stream=True, proxies=self.proxies)
            img_path = f'data/pic/profpic_{self.page_id}.jpeg'

            if req.status_code == 200:
                with open(img_path, 'wb') as file:
                    for chunk in req:
                        file.write(chunk)
                        self.links.update({"pp_img": link2pic})

                log(f"{link2pic} --> {img_path}")

            links2f_pics = self.page.xpath('//div[@class="Friends__mutualItem"]//'
                                           'img[@class="Friends__mutualItemImg"]/@src')

            for link in links2f_pics:
                i = links2f_pics.index(link)
                try:
                    req = requests.get(link, stream=True, proxies=self.proxies)
                except requests.exceptions.MissingSchema:
                    req = requests.get(f"https://vk.com{link}", stream=True, proxies=self.proxies)

                img_path = f'data/pic/friendpic_{self.page_id}_{i}.jpeg'

                if req.status_code == 200:
                    with open(img_path, 'wb') as file:
                        for chunk in req:
                            file.write(chunk)
                            self.links.update({f"f{i}_img": link})

                    log(f"{link} --> {img_path}")

        except AttributeError as _error:
            print(f"{_error} {self.page_id} : page close or does not exist (can't get profile picture)")
            log(data=f"{self.page_id} : page close or does not exist (can't get profile picture)",
                error=_error.__str__())

    def getinfo(self):
        # CONVERTING
        url = f'https://m.vk.com/id{self.page_id}?act=info'
        info_content = self.session.get(url, proxies=self.proxies).content
        self.page_info = lx.fromstring(info_content)
        self.page_info = self.page_info.xpath('//div[@class="PageBlock PageBlock_overflow"]')[0]
        self.page_info = etree.tostring(self.page_info, method='html', encoding="UTF-8").decode('utf-8')

        # REPLACING img links
        links_replace = {"pp_img": f"data/pic/profpic_{self.page_id}.jpeg",
                         "f0_img": f"data/pic/friendpic_{self.page_id}_1.jpeg",
                         "f1_img": f"data/pic/friendpic_{self.page_id}_2.jpeg",
                         "f2_img": f"data/pic/friendpic_{self.page_id}_3.jpeg"
                         }
        for (name, link) in self.links.items():
            if link:
                self.page_info = self.page_info.replace(link, links_replace.get(name))
        # ------------------ #

        try:
            results_ = json.load(open(f'data/info/user_{self.page_id}.json', 'r', encoding='utf8'))
        except FileNotFoundError:
            results_ = dict()
        except json.decoder.JSONDecodeError:
            results_ = dict()

        results_.update({'page_block': self.page_info})
        with open(f'data/info/user_{self.page_id}.json', 'w', encoding="utf8") as outfile:
            json.dump(results_, outfile)

    def get_all(self):
        self.getpage()
        self.getname()
        self.getlastseen()
        self.getprofpics()
        self.getinfo()

    def __str__(self):
        return f'{self.__class__.__name__}: id = {self.page_id}, name = "{self.name}", lastseen = "{self.lastseen}"'


# - - - - - - - - - M A I N - - - - - - - - - - - #
os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
print("""VKS v1.1.9 | vk.com opensource stalkerware
Running... 
""")

if rand_proxy and not proxy:
    while not proxy:
        proxy = r_proxy().get()

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
targets_list = []
for t_id in page_id:
    targets_list.append(person(page_id=t_id, proxies=proxy))  # SET ID

# LOGIN REQUEST + CREATING SESSION
if password:
    targets_list[0].loginsession(login, password)
    del password  # REMOVING PASSWORD FROM MEMORY

db = database(tablename=time.strftime("T%d_%m_%Y"))  # CREATING NEW TABLE IN DATABASE

# FIRST TRY
for target in targets_list:
    target.session = targets_list[0].session
    db.conn = sqlite3.connect(f'data/db/user_{target.page_id}.db')
    target.get_all()

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

        for target in targets_list:
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
