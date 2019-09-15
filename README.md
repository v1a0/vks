# VkScrapper
 Program for monitor your own online activity in vk.com

## Libraries Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries.

```python
pip install requests | pip install bs4 | pip install BeautifulSoup
```

## Usage

### Before you start
Found id of your VK page.

### Let' begin
Run a script:
```bash
py get_online.py
```
```bash
Enter user id (Введите id  пользователя): 10000451
```
```bash
START: 05-01-1984 00:00 | Guy Montag | URL: https://vk.com/id10000451
15-09-2019 00:00 | заходил 41 минуту назад
15-09-2019 00:01 | заходил 42 минуты назад
15-09-2019 00:02 | Online
```

### After
After you collect some statistic, you can found 2 type of files `05-01-1984_full_log.txt` and `05-01-1984_log.txt`.
`05-01-1984_full_log` - it's log with every minute statistic
`05-01-1984_log` - it's only about online time

## Converting to HTML
For conver your logs to HTML table use [log2html](https://github.com/V1A0/log2html)
```bash
git clone https://github.com/V1A0/log2html.git
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)