# -*- coding: utf-8 -*-
import argparse
import datetime
import os
import time
import requests
from bs4 import BeautifulSoup as bs

# custom modules
import html_parser
import html_requests
import log_editor as log

# - - - - - T I M E  &  D A T E - - - - - - - #
time_dt = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")    # date & time "dd-mm-yyyy hh:mm"
time_t = datetime.datetime.now().strftime("%H:%M")              # time "hh:mm"
time_d = datetime.datetime.now().strftime("%d-%m-%Y")           # date "dd-mm-yyyy"
# - - - - - - - - - - - - - - - - - - - - - - #

# - - - - - - - OS THINGS - - - - - - - #
os.system('cls' if os.name == 'nt' else 'clear')                # Clear the console
try:
    os.mkdir('html')                                            # Make dir html
    os.mkdir('log')                                             # Make dir log
except:
    pass

# - - - - - - - ARGUMENTS - - - - - - - - #
opt = argparse.ArgumentParser(description='Print an argument several times')
opt.add_argument('-i', '--id', dest='id', type=str,
                    default='', metavar='1234567890',
                    help='Enter id of page (for analysis)')
opt.add_argument('-l', '--login', dest='logn', type=str,
                    default='', metavar='+71234567890',
                    help='Enter login data (email or phone number)')
opt.add_argument('-p', '--password', dest='pwd', type=str,
                    default='', metavar='pwned1234',
                    help='Enter login data (password)')
opt.add_argument('-t', '--timesleep', dest='ts', type=int,
                    default='60', metavar='60',
                    help='Request frequency [sec] (default = 60)')
args = opt.parse_args()
# - - - - - - - - - - - - - - - - - - - #


# - - - - - C O U N T E R S - - - - - - #
a, on_c = 1, 0
# - - - - - - - - - - - - - - - - - - - #

# - - - - - - - S T A R T - - - - - - - #
if args.id == '':
    print('Enter user id (Введите id  пользователя):', end=" ")
    url = 'https://vk.com/id' + input()
else:
    url = 'https://vk.com/id' + args.id
# - - - - - - - - - - - - - - - - - - - #

# - - - - - CREATING SESSION - - - - - - #
headers={
    "Referer":"https://m.vk.com/login?role=fast&to=&s=1&m=1&email=" + args.logn,
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'
}

payload = {
            'act': 'login',
            'email' : args.logn,
            'pass' : args.pwd,
            'role' : 'al_frame',
            '_origin' : 'https://vk.com'
}
S = requests.Session()
page = S.get('https://m.vk.com/login')                  # get request
soup = bs(page.content, 'lxml')                          # bs converting
login_url = soup.find('form')['action']                 # serching data
p = S.post(login_url, data=payload, headers=headers)    # post request (active session)
# - - - - - - - - - - - - - - - - - - - #

# - - - - - - - - - - - - - - - - - - - #
html_requests.get_html(url, S, args.id)         # first request (to get page name)
start = '\nSTART: ' + time_dt + ' | ' + \
        str(html_parser.get_name(args.id)) + \
        ' | URL: ' + url
print(start)                                    # print start data:  DATE | NAME | URL
log.add2log(start, time_d + '_log.txt')         # add start data to log
log.add2log(start, time_d + '_full_log.txt')    # add start data to full_log
# - - - - - - - - - - - - - - - - - - - #


# - - - - M A I N  L O O P - - - - - - - #
while True:
    # Set/update time
    time_dt = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")    # date & time "dd-mm-yyyy hh:mm"
    time_t = datetime.datetime.now().strftime("%H:%M")              # time "hh:mm"
    time_d = datetime.datetime.now().strftime("%d-%m-%Y")           # date "dd-mm-yyyy"

    # get html page
    html_requests.get_html(url, S, args.id)                         # get request (update)

    try:
        result = time_dt + " | " + html_parser.lastseen(args.id)    # result = time + lastseen
        try:
            with open('./log/' + time_d + '_log.txt') as f:         # add data to log
                data = f.readlines()
                tail = data[-1:]
        except:
            tail = 'new file'
            a = 1

        if (html_parser.lastseen(args.id) == 'Online') and (tail != r'\d\d-\d\d-\d\d\d\d \d\d:\d\d | Online'):
            log.add2log(result, (time_d + '_log.txt'))
            a = 1
            on_c += 1
            # print('Online activity\n')
        else:
            if (html_parser.lastseen(args.id) != 'Online') and (a == 1):
                log.add2log(result, (time_d + '_log.txt'))
                a = 0
        f.close()
    except:
        result = time_dt + ' | [!] error 1: Can’t connect to the server [!]'

    print(result)
    log.add2log(result, (time_d + '_full_log.txt'))
    time.sleep(args.ts) # time pause (sec)
