from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests

r = requests.get('https://nvd.nist.gov/download/nvdcve-2010.meta')