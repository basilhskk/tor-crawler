from lib.parser import Parser
from lib.db import Database
import os,requests,time,html,ast,urllib3,json,concurrent
import concurrent.futures



urllib3.disable_warnings()

# constants
PATH            = os.path.dirname(os.path.abspath(__file__))
# WARNING THIS URL MAY CHANGE
STARTURL        = "http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page" #hidden wiki http://wiki5kauuihowqi5.onion/
TORBUNDLEHEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}
 

#create tor session
def connect_to_tor()-> requests.Session:
    session = requests.session()
    session.proxies = {'http':  'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'}
    return session

def crawl(urloc:str) -> (str,list):
    db      = Database(PATH)
    parser  = Parser()
    session = connect_to_tor()

    # select here to find if in db 
    try:
        urlindb = db.select(urloc)
        if len(urlindb) > 0:
            print("url already crawled")
            return urloc,[]
    except Exception as e:
        print(e)


    try:
        try:
            r = session.get(urloc,headers=TORBUNDLEHEADER)
            r.raise_for_status()
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            urls = parser.urlExtractor(urloc,r.text)
            protocol = urloc.split("://")[0]
            insert_data = {
            "protocol" : protocol,
            "url"      : urloc,
            "data"     : html.escape(r.text),
            "lastvisit": int(time.time()),
            }
            try:
                db.insert(insert_data)
            except Exception as e:
                # if urloc in db dont crawl it again and return
                if "UNIQUE constraint failed" in str(e):
                    print("url already crawled")
                    return urloc,[]
                else:
                    print(str(e))


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
        print(str(e))
        return urloc,[]

if __name__ == "__main__":
    

    urls = [STARTURL]
    # check if we have logged urls to crawl
    try:
        with open("urls.log","r")as rf:
            data = rf.read()
            if len(data)>0 :
                urls = json.loads(data)["urls"]
    except:
        os.mknod("urls.log")

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
                        # fix this
                        try:
                            data[1].remove(data[0])
                            newUrls.remove(data[0])
                        except:
                            pass

                if len(data[1])> 0 :
                        newUrls.extend(data[1])
            except:
                pass

        urls = newUrls

        # save urls log in case of unexpected exit
        with open("urls.log","w")as f:
                json.dump({"urls":urls},f)
        print(f"Urls to be crawled: {len(urls)}")