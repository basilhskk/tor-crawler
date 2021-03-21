from bs4 import BeautifulSoup,SoupStrainer
from urllib.parse import urljoin
from tld import get_tld

class Parser():

    def urlExtractor(self, currentUrl: str, html: str) -> dict:
        href = {}
        
        if html:
            for link in BeautifulSoup(html, parse_only=SoupStrainer('a'),features="html.parser"):
                if link.has_attr("href"):
                    url = link["href"]
                    if url[0] not in ["#","/"]:
                        try:
                            protocol = url.split(":")[0]
                            print(url)
                            if protocol in href:
                                href[protocol].append(url)
                            else:
                                href[protocol] = [url]
                        except Exception as e:
                            pass
                    elif url[0] == "/":
                        print(urljoin(currentUrl,url))
                        
        return href

    def tldExtractor(self,url:str)-> str:
        return get_tld(url, fail_silently=True)