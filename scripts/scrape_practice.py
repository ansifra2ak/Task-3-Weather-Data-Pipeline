"""Optional hands-on HTML scraping exercise, offline by default.
Use a local saved public weather page you have permission to process.
"""
from html.parser import HTMLParser
from pathlib import Path
import argparse
class TitleParser(HTMLParser):
    def __init__(self): super().__init__(); self.in_title=False; self.title=[]
    def handle_starttag(self, tag, attrs):
        if tag=='title': self.in_title=True
    def handle_endtag(self,tag):
        if tag=='title': self.in_title=False
    def handle_data(self,data):
        if self.in_title: self.title.append(data)
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('html_file',nargs='?'); a=p.parse_args()
    parser=TitleParser(); parser.feed(Path(a.html_file).read_text() if a.html_file else '<html><head><title>Example weather bulletin (practice fixture)</title></head></html>'); print('Extracted title:', ''.join(parser.title))
