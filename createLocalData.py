from VulnDictionary import VulnDictionary
import pickle

if __name__ == "__main__":
    count = 0
    for i in range(2002,2017):
        myDic = VulnDictionary(i)
        print(myDic.is_updated())
        myDic.update()
        print(myDic.is_updated())
        print()
        with open("VulnDictionary_"+str(i)+".p",'wb') as f:
            pickle.dump(myDic, f)
        count = count + len(myDic.dict.keys())
    print("Total: "+str(count))