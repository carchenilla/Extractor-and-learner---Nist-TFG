class Software:
    def __init__(self, name, vendor, versions):
        self.name = name
        self.vendor = vendor
        self.versions = versions

    def to_string(self):
        vers = ""
        for v in self.versions:
            vers = vers + v + " - "
        return "Name: "+self.name+" - Vendor: "+self.vendor+"\n Versions: "+vers