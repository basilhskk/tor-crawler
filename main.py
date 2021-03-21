from lib.parser import Parser
from lib.db import Database
import os 
import requests

# constants
PATH            = os.path.dirname(os.path.abspath(__file__))
URL             = "http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page" #hidden wiki
TORBUNDLEHEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}



#create tor session
def connect_to_tor()-> requests.Session:
    session = requests.session()
    session.proxies = {'http':  'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'}
    return session

def crawl(urloc:str):
    r = session.get(urloc,headers=TORBUNDLEHEADER)

    data = parser.urlExtractor(urloc,r.text)

    for key, value in data.items():
        if key == "http" or key == "https" :
            # crawl only http protocol
            for url in data[key]:
                tld = parser.tldExtractor(url)
                # crawl only onion sites
                if tld == "onion":
                    print(url)




if __name__ == "__main__":
    # init
    parser  = Parser()
    db      = Database(PATH)
    session = connect_to_tor()
    
    crawl(URL)