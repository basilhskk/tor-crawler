from lib.parser import Parser
from lib.db import Database
import os 
import requests

PATH = os.path.dirname(os.path.abspath(__file__))
URL  = "http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page"



parser  = Parser()
db      = Database(PATH)

#create tor session
def connect_to_tor():
    session = requests.session()
    session.proxies = {'http':  'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'}
    return session


session = connect_to_tor()

r = session.get(URL)

data = parser.urlExtractor(URL,r.text)

print(data.keys())