import requests
from bs4 import BeautifulSoup as bs

# Update page information
def get_html(url, S, id):

    # Try to get html page
    try:
        r = S.get(url)
        # print(r)
        with open('./html/' + id + '.html', 'wb') as output_file:
            output_file.write(r.text.encode('utf-8'))

    # If something wrong - creating default "error 1" page
    except:
        with open('./html/' + id +'.html', 'w', encoding="utf8") as output_file:
            output_file.write('<html><body><h1>CONNECTION ERROR</h1></br>error 1: Can’t connect to the server at <a '
                              'href=\"' + url + '\">URL</a></body></html>')

