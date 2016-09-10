import xml.etree.ElementTree as ET
import zipfile
from urllib.request import urlretrieve
import os
from Software import Software

if __name__ == "__main__":

    name = "nvdcve-2002.xml.zip"
    urlretrieve("https://nvd.nist.gov/download/" + name, name)
    zipfile.ZipFile(name).extractall()
    os.remove(name)

    root = ET.parse(name[:-4]).getroot()
    for p in root:
        if p.get('name')=="CVE-2000-0288":
            my_child = p
            break
    print(len(my_child))
    vuln_soft = my_child[4]
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
    for x in software_list:
        print(x.to_string())