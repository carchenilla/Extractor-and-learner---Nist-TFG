import datetime
import xml.etree.ElementTree as ET
import zipfile
import urllib.request
import os
from bs4 import BeautifulSoup


class VulnDict:
    def __init__(self,year):
        self.__last_mod = datetime.date(2000,1,1)
        self.__dict = {}
        self.__year = year

    def setLastModToday(self):
        self.__last_mod = datetime.date.today()

    def isUpdated(self):
        meta_page = urllib.request.urlopen("https://nvd.nist.gov/download/nvdcve-"+str(self.__year)+".meta")
        soup = BeautifulSoup(meta_page.read(), "lxml")
        return datetime.date.today() <= self.__last_mod

    def update(self):
        if not self.isUpdated():
            self.__dict = {}
            name = "nvdcve-"+str(self.__year)+".xml.zip"
            urllib.request.urlretrieve("https://nvd.nist.gov/download/"+name,name)
            zipfile.ZipFile(name).extractall()
            os.remove(name)

            root = ET.parse(name[:-4]).getroot()
            for child in root:
                print("Name: " + child.attrib['name'])
            os.remove(name[:-4])
            self.setLastModToday()