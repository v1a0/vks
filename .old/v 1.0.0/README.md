# VkScrapper v 1.0.0 ![Python:3.7](https://img.shields.io/badge/Python-3.7-yellow) [![stability-unstable](https://img.shields.io/badge/stability-unstable-yellow.svg)](https://github.com/emersion/stability-badges#unstable) ![License:MIT](https://img.shields.io/github/license/V1A0/VkScrapper)
 
Program for monitor your own online activity on [vk.com](https://vk.com/)

## 1. Libraries Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) OR inline key (-i, --install) to install necessary for script modules.

```bash
pip install sqlite3
pip install argparse
pip install bs4
pip install lxml
pip install requests
```
OR
```
py vks.py --install
```



## 2. How to use
#### 2.1. First way - UI
For run use python 3.7+:
```bash
py vks.py
```
After that, enter id of your page on vk.com:
```bash
Enter user id: 10000451
```
Login (optional):
```bash
Are you sure you want to continue without authorisation?
(y/n) : n
Enter login: +79998887766
Enter password: [not displayed]
```
You don't must to login, but user page may be hidden from anonymous visits by privacy settings.<br/>
Script use login data only once, to create a web-session. After that password is erasing and will never be appear in memory.<br/>
If tracking session started successfully you'll get message like that in your terminal:
```bash
Tracking is started successfully
User: Guy Montag
Status:
05-01-1984 13:37:42  :  Offline
05-01-1984 13:38:42  :  Offline
05-01-1984 13:39:42  :  Online
05-01-1984 13:40:42  :  Online
```
---

#### 2.2. Second way - Manual
For run use python and some arguments:
```bash
py vks.py -id 10000451 -l +71234567890 -p pwned1234 -t 60
```
Arguments list:
- `-i` / `--install` -  install all necessary for script modules <b>[first run]</b>,
- `-id` / `--page_id` - id,
- `-l` / `--login` - phone or email,
- `-p` / `--password` - password,
- `-t` / `--timesleep` - request frequency (sec) <b>[debug tool]</b>


Script use login data only once, to create a session. After that password is erasing and will never be appear in memory.<br/>
If tracking session started successfully you'll get message like that in your terminal:
```bash
Tracking is started successfully
User: Guy Montag
Status:
05-01-1984 13:37:42  :  Offline
05-01-1984 13:38:42  :  Offline
05-01-1984 13:39:42  :  Online
05-01-1984 13:40:42  :  Online

```
Don't close the terminal until you didn't get enough data to analise.


#### 2.3. Errors and how to fix ⚠
If user hiding his page from anonymous visits, you'll see messages like this:
```bash
Tracking is started successfully
User: Guy Montag
Status:
05-01-1984 13:37:42  :  ERROR
05-01-1984 13:38:42  :  ERROR
05-01-1984 13:39:42  :  ERROR
05-01-1984 13:40:42  :  ERROR
```
Name displaying, but activity status is 'ERROR'.<br/>
To fix it authorise as 'real' user or friend of target. 

### 3. After
After you collect some statistic data, you can stop script. Just close console or press Ctrl + C some times.<br>
Now you need to analyze and/or visualize this information. After next updated it'll have inline tool for this <b>[COMING SOON]</b>.<br/>
Multiple targets support is <b>[COMING SOON]</b>.
###### ~~Converting to HTML~~ - Not supported at last versions

---

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)