import pickle
from data_types.VulnDictionary import VulnDictionary


def saveAsignationToDisk(asig, dictionary_list):
    for x in asig:
        found = False
        i = 0
        while ((not found) and (i <= len(dictionary_list))):
            d = dictionary_list[i]
            v = d.dict.get(x[0])
            if v != None:
                v.group = x[1]
                found = True
            i = i + 1
    saveDictionariesToDisk(dictionary_list)


def loadDictionaries(list_of_years):
    dictionary_list = []
    for i in list_of_years:
        try:
            with open("../dictionaries/VulnDictionary_" + str(i)+ ".p", 'rb') as f:
                dictionary_list.append(pickle.load(f))
        except IOError as err:
            print("Error with dictionary " + str(i) + " - " + str(err))
            print("Creating dictionary from scratch")
            dictionary_list.append(VulnDictionary(i))
    return dictionary_list


def saveDictionariesToDisk(dictionary_list):
    for d in dictionary_list:
        try:
            with open("../dictionaries/VulnDictionary_" + str(d.year) + ".p", 'wb') as f:
                pickle.dump(d, f)
        except IOError as err:
            print("Error with dictionary " + str(d.year) + " - " + str(err))
    print("Done!")