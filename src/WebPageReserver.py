# coding: utf-8
# # WebPageReserver

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, unquote
import os

class WebPageReserver(object):

    def __init__(self):
        pass
    
    def getIn(self, working_dir, parent, target):
        print("="*40)
        cur_url = urljoin(parent, target)
        print(cur_url)
        
        res = requests.get(cur_url)
        soup = bs(res.content, "html.parser")

        is_dir = "text/html" in res.headers['Content-Type'].split(";")
        
        if 'html' in target.split('.'):
            is_dir = False
        
        if is_dir:
            working_dir = os.path.join(working_dir, unquote(target))
            os.mkdir(working_dir)
            self.downloadThisPage(working_dir, "index.html", res.content)
            a_list = soup.find_all("a")
            for a in a_list[5:]:
                self.getIn(working_dir ,cur_url, a['href'])
                
        else :
            self.downloadThisPage(working_dir, target, res.content)

    def downloadThisPage(self, working_dir, target, res):
        with open(os.path.join(working_dir, unquote(target)) , "wb") as f:
            f.write(res)


def main():
    print("="*40)
    print("Preserve Start!")
    wpr = WebPageReserver()
    wpr.getIn("./cs224d","https://cs224d.stanford.edu/lectures/","")
    print("done!")

if __name__ == '__main__':
    main()


