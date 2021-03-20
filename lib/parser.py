from bs4 import BeautifulSoup,SoupStrainer


class Parser():
    def __init__(self):
        self.urls = []

    def urlExtractor(self, html):
        href = {
            "irc" : []
            "http" : [],
            "xmpp" : [],
            "mailto" : [],
            "tel": [],
            
        }
        if html:
            for link in BeautifulSoup(html, parse_only=SoupStrainer('a')):
                if link.has_attr("href"):
                    url = link["href"]
                    