import requests

# Update page information
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }  # COMING SOON
    # Try to get html page
    try:
        r = requests.get(url)
        # print(r)
        with open('./html/' + 'test.html', 'wb') as output_file:
            output_file.write(r.text.encode('utf-8'))
    # If something wrong - creating default "error 1" page
    except:
        with open('./html/' + 'test.html', 'w', encoding="utf8") as output_file:
            output_file.write('<html><body><h1>CONNECTION ERROR</h1></br>error 1: Can’t connect to the server at <a '
                              'href=\"' + url + '\">URL</a></body></html>')

