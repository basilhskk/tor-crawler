from lib.parser import Parser
from lib.db import Database
import os,requests,time,html,ast,urllib3,json,base64
import concurrent.futures,multiprocessing



urllib3.disable_warnings()

# constants
PATH            = os.path.dirname(os.path.abspath(__file__))
# WARNING THIS URL MAY CHANGE
WIKI            = "http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page" #hidden wiki
URLLISTING      = "http://dirnxxdraygbifgc.onion/" # url listing site
OLDWIKI         = "http://wiki5kauuihowqi5.onion/" # onion wiki old
TORBUNDLEHEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}


#create tor session
def connect_to_tor()-> requests.Session:
    session = requests.session()
    session.proxies = {'http':  'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'}
    return session


#crawler
def crawl(urloc:str) -> (str,list):
    db      = Database(PATH)
    parser  = Parser()
    session = connect_to_tor()

    # select here to find if in db 
    try:
        urlindb = db.isCrawled(urloc)
        if len(urlindb) > 0:
            # url already crawled
            del urlindb
            return urloc,[]
    except Exception as e:
        print(e)


    try:
        try:
            r = session.get(urloc,headers=TORBUNDLEHEADER,timeout=20)
            r.raise_for_status()

        except Exception as err:
            insert_data = {
            "protocol" : "Error",
            "url"      : urloc,
            "data"     : base64.b64encode(str(err).encode()),
            "lastvisit": int(time.time()),
            }

            try:
                db.insert(insert_data)
            except Exception as e:
                # if urloc in db dont crawl it again and return
                if "UNIQUE constraint failed" in str(e):
                    # update val
                    try:
                        db.update(insert_data)
                    except Exception as e:
                        pass    
        else:
            urls        = parser.urlExtractor(urloc,r.text)
            protocol    = urloc.split("://")[0]
            insert_data = {
            "protocol" : protocol,
            "url"      : urloc,
            "data"     : base64.b64encode(r.content),
            "lastvisit": int(time.time()),
            }
            
            try:
                db.insert(insert_data)
            except Exception as e:
                # if urloc in db dont crawl it again and return
                if "UNIQUE constraint failed" in str(e):
                    # update val
                    try:
                        db.update(insert_data)
                    except Exception as e:
                        pass

            retUrls = []
            for key, value in urls.items():
                if key == "http" or key == "https" :
                    # crawl only http protocol
                    for url in urls[key]:
                        tld = parser.tldExtractor(url)
                        # crawl only onion sites
                        if tld == "onion":
                            retUrls.append(url)
            return urloc, retUrls

    except Exception as e:
        return urloc,[]


if __name__ == "__main__":
    
    db   = Database(PATH)
    urls = [WIKI,URLLISTING,OLDWIKI]
    
    while len(urls)>0:
        
        # multi threading function TPE default max workers == cpu count * 5
        with concurrent.futures.ThreadPoolExecutor() as executor: # optimally defined number of threads
            
            urls = [executor.submit(crawl, url) for url in urls]
            concurrent.futures.wait(urls)
        
        newUrls = []
        
        for result in urls:
            try:
                data = result.result()
                if data[0] != None:
                    if data[0] != None:
                        try:
                            data[1].remove(data[0])
                            newUrls.remove(data[0])
                        except:
                            pass
                if len(data[1])> 0 :
                        newUrls.extend(data[1])
            except:
                pass

        urls = list(set(newUrls))
        del newUrls

        for url in urls:
            try:
                insert_data = {
                "protocol" : "http",
                "url"      : url,
                "data"     : "",
                "lastvisit": 0,
                }

                db.insert(insert_data)
            except Exception as e: 
                print(str(e))

        # get only 100 urls to minimize ram usage
        newUrls = db.query("SELECT url from Data WHERE lastvisit = 0 LIMIT 100")
        urls = [url[0] for url in newUrls]
        del newUrls
