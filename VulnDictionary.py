import datetime
import xml.etree.ElementTree as ET
import zipfile
from urllib.request import urlopen, urlretrieve
import os
from Vulnerabilty import Vulnerability

ACCESS_VECTOR = {'L':'Local access', 'A': 'Adjacent Network', 'N': 'Network'}
ACCESS_COMPLEXITY = {'H':'High', 'M':'Medium', 'L':'Low'}
AUTHENTIFICATION = {'N':'None required', 'S':'Requires single instance', 'M':'Requires multiple instances'}
CONF_IMPACT = {'N':'None', 'P':'Partial','C':'Complete'}
INTEG_IMPACT = {'N':'None', 'P':'Partial','C':'Complete'}
AVAIL_IMPACT = {'N':'None', 'P':'Partial','C':'Complete'}

FEATURES_LIST = [ACCESS_VECTOR, ACCESS_COMPLEXITY, AUTHENTIFICATION, CONF_IMPACT, INTEG_IMPACT, AVAIL_IMPACT]


class VulnDictionary:
    def __init__(self,year):
        self.last_mod = datetime.date(2000,1,1)
        self.dict = {}
        self.year = year

    def set_last_mod_today(self):
        self.last_mod = datetime.date.today()

    def is_updated(self):
        meta_page = str(urlopen("https://nvd.nist.gov/download/nvdcve-"+str(self.year)+".meta").read())
        meta_date = datetime.date(int(meta_page[19:23]),int(meta_page[24:26]),int(meta_page[27:29]))
        return meta_date <= self.last_mod


    def update(self):
        if not self.is_updated():
            self.dict = {}
            name = "nvdcve-"+str(self.year)+".xml.zip"
            urlretrieve("https://nvd.nist.gov/download/"+name,name)
            zipfile.ZipFile(name).extractall()
            os.remove(name)

            root = ET.parse(name[:-4]).getroot()
            for child in root:
                try:
                    if child.get("reject")!="1":
                        vname = child.attrib['name']
                        pub_date = child.attrib['published'].split('-')
                        mod_date = child.attrib['modified'].split('-')
                        sev = str(child.attrib['severity'])
                        score = float(child.attrib['CVSS_score'])
                        bas_score = float(child.attrib['CVSS_base_score'])
                        imp_score = float(child.attrib['CVSS_impact_subscore'])
                        exp_score = float(child.attrib['CVSS_exploit_subscore'])
                        vect = self.extract_vector(child.attrib['CVSS_vector'])
                        descr = child[0][0].text
                        self.dict[vname] = Vulnerability(vname, datetime.date(int(pub_date[0]), int(pub_date[1]), int(pub_date[2])),
                                                        datetime.date(int(mod_date[0]), int(mod_date[1]), int(mod_date[2])),
                                                        sev, score, bas_score, imp_score, exp_score, vect, descr)
                        #print("Name: "+vname+"\n Description: "+descr)
                        print("Saved vulnerability: "+vname)
                except KeyError:
                    print("There's a problem with vulnerability "+child.attrib['name'])
            os.remove(name[:-4])
            self.set_last_mod_today()


    def extract_vector(self, initialVector):
        new_vector = initialVector[1:-1].split('/')
        final_vector = []
        for i in range(len(new_vector)):
            final_vector.append(FEATURES_LIST[i][new_vector[i][-1]])
        return final_vector