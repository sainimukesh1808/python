from bs4 import BeautifulSoup
import requests


url=r"file:///C:/Users/msi26/Desktop/Intersite%20WS/FBT_Living_Heart_Simulation.html"
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
print(soup.prettify()) # print the parsed data of html
