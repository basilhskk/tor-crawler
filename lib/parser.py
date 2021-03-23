from bs4 import BeautifulSoup,SoupStrainer
from urllib.parse import urljoin
from tld import get_tld

class Parser():

    def urlExtractor(self, currentUrl: str, html: str) -> dict:
        href = {}
        try:
            current_protocol = currentUrl.split(":")[0]
            
            if html:
                for link in BeautifulSoup(html, parse_only=SoupStrainer('a'),features="html.parser"):
                    if link.has_attr("href"):
                        url = link["href"]
                        if url[0] not in ["#","/"]:
                            try:
                                protocol = url.split(":")[0]
                                if protocol in href:
                                    href[protocol].append(url)
                                else:
                                    href[protocol] = [url]
                            except Exception as e:
                                pass
                        elif url[0] == "/":
                            if current_protocol in href:
                                href[current_protocol].append(urljoin(currentUrl,url))
                            else:
                                href[current_protocol] = [urljoin(currentUrl,url)]
            return href
        except Exception as e:
            print(str(e))
            return href

    def tldExtractor(self,url:str)-> str:
        return get_tld(url, fail_silently=True)
