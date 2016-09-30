import pickle
from data_types.VulnDictionary import VulnDictionary

if __name__ == "__main__":
    count = 0
    for i in range(2002,2017):
        myDic = VulnDictionary(i)
        myDic.update()
        print()
        with open("dictionaries/VulnDictionary_"+str(i)+".p",'wb') as f:
            pickle.dump(myDic, f)
        count = count + len(myDic.dict.keys())
    print("Total: "+str(count))