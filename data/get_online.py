# -*- coding: utf-8 -*-
import datetime
import os
import time

import requests
from bs4 import BeautifulSoup

# - - - - - T I M E  &  D A T E - - - - - - - #
time_dt = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")  # date & time "dd-mm-yyyy hh:mm"
time_t = datetime.datetime.now().strftime("%H:%M")  # time "hh:mm"
time_d = datetime.datetime.now().strftime("%d-%m-%Y")  # date "dd-mm-yyyy"
# - - - - - - - - - - - - - - - - - - - - - - #

# Update page information
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }  # COMMING SOON
    # Try to get html page
    try:
        r = requests.get(url)
        #print(r)
        with open('test.html', 'wb') as output_file:
            output_file.write(r.text.encode('utf-8'))
    # If something wrong - creating default "error 1" page
    except:
        with open('test.html', 'w', encoding="utf8") as output_file:
            output_file.write('<html><body><h1>CONNECTION ERROR</h1></br>error 1: Can’t connect to the server at <a href=\"' + url + '\">URL</a></body></html>')


# Get last seen information
def lastseen():
    html_ = open('test.html', 'r', encoding="utf8")  # opening HTML file +encoding
    soup = BeautifulSoup(html_, 'lxml')  # creating soup-object
    # Searching right place
    try:
        info = soup.find('span', class_='pp_last_activity_offline_text').next_element  # searching info about
    except:
        try:
            info = soup.find('span', class_='pp_last_activity_text').next_element  # searching info about
        except:
            try:
                info = soup.find('div', class_='profile_online_lv').next_element
            except:
                return IOError
    return info


def get_name():
    html_ = open('test.html', 'r', encoding="utf8")  # opening HTML file + encoding
    soup = BeautifulSoup(html_, 'lxml')  # creating soup-object
    # Searching right place
    try:
        info = soup.find('h2', class_='op_header').next_element  # searching info about
    except:
        info = 'error'
    return info


#Universal func for add data to log
def log(data, file):
    open(file, 'a', encoding="utf8").write(data + '\n')


# - - - - - S E T T I N G S - - - - - - #
a = 1  # counter 1
b = 0
on_c = 0
off_c = 0
# - - - - - - - - - - - - - - - - - - - #


# - - - - - - - S T A R T - - - - - - - #
os.system('cls' if os.name == 'nt' else 'clear') # Clear the console
print('Enter user id (Введите id  пользователя):', end=" ")
url = 'https://vk.com/id' + input()
get_html(url)
start = '\nSTART: ' + time_dt + ' | ' + get_name() + ' | URL: ' + url

log(start, time_d + '_log.txt') # add start data to log
log(start, time_d + '_full_log.txt') # add start data to full_log
print(start)
# - - - - - - - - - - - - - - - - - - - #


# - - - - M A I N  L O O P - - - - - - - #
while True:
    #Set/update time
    time_dt = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")  # date & time "dd-mm-yyyy hh:mm"
    time_t = datetime.datetime.now().strftime("%H:%M")  # time "hh:mm"
    time_d = datetime.datetime.now().strftime("%d-%m-%Y")  # date "dd-mm-yyyy"

    #get html page
    get_html(url)

    try:
        result = time_dt + " | " + lastseen()
        try:
            with open(time_d +'_log.txt') as f:
                data = f.readlines()
                tail = data[-1:]
        except:
            tail = 'new file'
            a = 1

        if (lastseen() == 'Online') and (tail != r'\d\d-\d\d-\d\d\d\d \d\d:\d\d | Online'):
            log(result, (time_d + '_log.txt'))
            a = 1
            on_c += 1
            # print('Online activity\n')
        else:
            if (lastseen() != 'Online') and (a == 1):
                log(result, (time_d + '_log.txt'))
                a = 0
        f.close()
    except:
        result = time_dt + ' | [!] error 1: Can’t connect to the server [!]'

    print(result)
    log(result, (time_d + '_full_log.txt'))
    time.sleep(60)
