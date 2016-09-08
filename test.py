import xml.etree.ElementTree as ET
import zipfile

name = "nvdcve-2007.xml.zip"
zipfile.ZipFile(name).extractall()

tree = ET.parse(name[:-4])
root = tree.getroot()


for i in range(3):
    print(root[i].attrib)
    print(root[i][0][0].text)
    print("Name: "+root[i].attrib['name'])
    print()