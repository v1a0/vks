from bs4 import BeautifulSoup

# Get last seen information
def lastseen():
    html_ = open('./html/' + 'test.html', 'r', encoding="utf8")  # opening HTML file +encoding
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

# Update name from html file
def get_name():
    html_ = open('./html/' + 'test.html', 'r', encoding="utf8")  # opening HTML file + encoding
    soup = BeautifulSoup(html_, 'lxml')  # creating soup-object
    # Searching right place
    try:
        info = soup.find('h2', class_='op_header').next_element  # searching info about
    except:
        info = 'error'
    return info
