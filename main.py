from lib.parser import Parser
from lib.db import Database

import requests

parser = Parser()
db = Database()

START = ["http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page"]
    
#create tor session
def connect_to_tor() -> requests.session:
    session = requests.session()
    session.proxies = {'http':  'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'}
    return session


session = connect_to_tor()

r = session.get(START[0])

print(r)
parser.urlExtractor(r.text)