import datetime
import xml.etree.ElementTree as ET
import zipfile
from urllib.request import urlopen, urlretrieve
import os


class VulnDictionary:
    def __init__(self,year):
        self.__last_mod = datetime.date(2000,1,1)
        self.__dict = {}
        self.__year = year

    def setLastModToday(self):
        self.__last_mod = datetime.date.today()

    def isUpdated(self):
        meta_page = str(urlopen("https://nvd.nist.gov/download/nvdcve-"+str(self.__year)+".meta").read())
        meta_date = datetime.date(int(meta_page[19:23]),int(meta_page[24:26]),int(meta_page[27:29]))
        return meta_date <= self.__last_mod


    def update(self):
        if not self.isUpdated():
            self.__dict = {}
            name = "nvdcve-"+str(self.__year)+".xml.zip"
            urlretrieve("https://nvd.nist.gov/download/"+name,name)
            zipfile.ZipFile(name).extractall()
            os.remove(name)

            root = ET.parse(name[:-4]).getroot()
            count = 0
            for child in root:
                print("Name: " + child.attrib['name'])
                count+=1
            os.remove(name[:-4])
            print(count)
            self.setLastModToday()