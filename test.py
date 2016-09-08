from VulnDictionary import VulnDictionary


if __name__ == "__main__":
    mydict = VulnDictionary(2010)
    print(mydict.isUpdated())
    mydict.update()
    print()
    print(mydict.isUpdated())