import datetime
import os
import xml.etree.ElementTree as ET
import zipfile
from urllib.request import urlopen, urlretrieve
from extractor.Vulnerabilty import Vulnerability
from extractor.Software import Software
from numpy import array, float32


#ACCESS_VECTOR = {'L':'Local access', 'A': 'Adjacent Network', 'N': 'Network'}
ACCESS_VECTOR = {'L':0, 'A': 1, 'N': 2}

#ACCESS_COMPLEXITY = {'H':'High', 'M':'Medium', 'L':'Low'}
ACCESS_COMPLEXITY = {'H':2, 'M':1, 'L':0}

#AUTHENTIFICATION = {'N':'None required', 'S':'Requires single instance', 'M':'Requires multiple instances'}
AUTHENTIFICATION = {'N':0, 'S':1, 'M':2}

#CONF_IMPACT = {'N':'None', 'P':'Partial','C':'Complete'}
CONF_IMPACT = {'N':0, 'P':1, 'C':2}

#INTEG_IMPACT = {'N':'None', 'P':'Partial','C':'Complete'}
INTEG_IMPACT = {'N':0, 'P':1, 'C':2}

#AVAIL_IMPACT = {'N':'None', 'P':'Partial','C':'Complete'}
AVAIL_IMPACT = {'N':0, 'P':1, 'C':2}

SEVERITY = {'Low':0, 'Medium':1, 'High':2}


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
                        sev = SEVERITY.get(str(child.attrib['severity']))
                        score = float(child.attrib['CVSS_score'])
                        bas_score = float(child.attrib['CVSS_base_score'])
                        imp_score = float(child.attrib['CVSS_impact_subscore'])
                        exp_score = float(child.attrib['CVSS_exploit_subscore'])
                        # vect = self.extract_vector(child.attrib['CVSS_vector'])
                        vect = [bas_score, imp_score, exp_score, sev]
                        vect. extend(self.extract_vector(child.attrib['CVSS_vector']))
                        descr = child[0][0].text
                        try:
                            soft_list = self.extract_software(child[4])
                        except IndexError as err:
                            print("\nError with vulnerability "+vname)
                            print("No software list found \n")
                            soft_list = []
                        '''self.dict[vname] = Vulnerability(vname, datetime.date(int(pub_date[0]), int(pub_date[1]), int(pub_date[2])),
                                                        datetime.date(int(mod_date[0]), int(mod_date[1]), int(mod_date[2])),
                                                        sev, score, bas_score, imp_score, exp_score, vect, descr, soft_list)'''
                        self.dict[vname] = Vulnerability(vname, datetime.date(int(pub_date[0]), int(pub_date[1]), int(pub_date[2])),
                            datetime.date(int(mod_date[0]), int(mod_date[1]), int(mod_date[2])), score, array(vect, dtype=float32),
                                                         descr, soft_list)
                        print("Saved vulnerability: "+vname)
                except KeyError:
                    print("There's a problem with vulnerability "+child.attrib['name'])
            os.remove(name[:-4])
            self.set_last_mod_today()
            print(str(self.year) + " dictionary updated")
            return 1
        else:
            print(str(self.year)+" dictionary is up to date")
            return 0


    def extract_vector(self, initialVector):
        new_vector = initialVector[1:-1].split('/')
        final_vector = []
        for i in range(len(new_vector)):
            final_vector.append(FEATURES_LIST[i][new_vector[i][-1]])
        return final_vector

    def extract_software(self, vuln_soft):
        software_list = []
        for i in range(len(vuln_soft)):
            version_list = []
            for j in range(len(vuln_soft[i])):
                ver = vuln_soft[i][j].get('num')
                ed = vuln_soft[i][j].get('edition')
                if ed != None:
                    ver = ver + " " + ed
                version_list.append(ver)
            software_list.append(Software(vuln_soft[i].get('name'), vuln_soft[i].get('vendor'), version_list))
        return software_list

    def to_string(self):
        res = "Vulnerabilities from year "+str(self.year)+":\n"
        for v in self.dict.values():
            res = res + v.to_string()+"\n"
        return res+"\n"