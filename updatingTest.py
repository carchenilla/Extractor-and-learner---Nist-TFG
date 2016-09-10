import pickle

if __name__ == "__main__":
    count = 0
    dictionary_list = []
    for i in range(2002, 2017):
        with open("VulnDictionary_"+str(i)+".p", 'rb') as f:
            dictionary_list.append(pickle.load(f))
    for d in dictionary_list:
        d.update()
        count = count + len(d.dict.keys())
    print("Total: "+str(count))