from bs4 import BeautifulSoup       #BeautifulSoup
from urllib.request import Request,urlopen  #to open urls

if __name__ == "__main__":
    req = Request("https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-9798")
    #req.add_header('User-Agent','Magic Browser')    #headers for scraping
    content = urlopen(req)
    scrapper = BeautifulSoup(content.read(), "lxml")  # open html with lxml
    for tag in scrapper.find_all("span"):
        try:
            if tag.string=="Impact Score:":
                print(tag.parent.contents[-1].strip())
        except KeyError as err:
            pass