# -*- coding: utf-8 -*-
import datetime
import os
import time

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
try:
    os.mkdir('html')
    os.mkdir('log')
except:
    pass
os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
# - - - - - - - - - - - - - - - - - - - #


# - - - - - C O U N T E R S - - - - - - #
a, on_c = 1, 0
# - - - - - - - - - - - - - - - - - - - #


# - - - - - - - S T A R T - - - - - - - #
print('Enter user id (Введите id  пользователя):', end=" ")
url = 'https://vk.com/id' + input()

html_requests.get_html(url)
start = '\nSTART: ' + time_dt + ' | ' + html_parser.get_name() + ' | URL: ' + url

log.add2log(start, time_d + '_log.txt')         # add start data to log
log.add2log(start, time_d + '_full_log.txt')    # add start data to full_log

print(start)
# - - - - - - - - - - - - - - - - - - - #


# - - - - M A I N  L O O P - - - - - - - #
while True:
    # Set/update time
    time_dt = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")    # date & time "dd-mm-yyyy hh:mm"
    time_t = datetime.datetime.now().strftime("%H:%M")              # time "hh:mm"
    time_d = datetime.datetime.now().strftime("%d-%m-%Y")           # date "dd-mm-yyyy"

    # get html page
    html_requests.get_html(url)

    try:
        result = time_dt + " | " + html_parser.lastseen()
        try:
            with open('./log/' + time_d + '_log.txt') as f:
                data = f.readlines()
                tail = data[-1:]
        except:
            tail = 'new file'
            a = 1

        if (html_parser.lastseen() == 'Online') and (tail != r'\d\d-\d\d-\d\d\d\d \d\d:\d\d | Online'):
            log.add2log(result, (time_d + '_log.txt'))
            a = 1
            on_c += 1
            # print('Online activity\n')
        else:
            if (html_parser.lastseen() != 'Online') and (a == 1):
                log.add2log(result, (time_d + '_log.txt'))
                a = 0
        f.close()
    except:
        result = time_dt + ' | [!] error 1: Can’t connect to the server [!]'

    print(result)
    log.add2log(result, (time_d + '_full_log.txt'))
    time.sleep(60) # time pause (sec)
