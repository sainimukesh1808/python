from lxml import html
import requests
import re
def data():
    psge=requests.get("http://www.espncricinfo.com/scores")
    tree=html.fromstring(psge.content)
    l=tree.xpath("//span[@class='cscore_notes_game']/text()")
    won=[]
    for i in l:
        if re.search('England won by',i):
            won=i.split("won")
    print(won)
    print(l)
data()
