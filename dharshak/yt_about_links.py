from bs4 import BeautifulSoup
import urllib.request

html_page = urllib.request.urlopen("https://www.youtube.com/c/Cancercenter/about")
soup = BeautifulSoup(html_page, "html.parser")
# print(soup.prettify())
allDivs = soup.find_all("div", { "id" : "link-list-container" })
print(allDivs)