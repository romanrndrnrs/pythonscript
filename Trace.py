import json
from Trame import Trame
from parse_trame import get_clean_trame

class Trace:
    def __init__(self, trameTab):
        self.trameTab = trameTab
        pass

    def toDictStr(self):
        dictRes = "{"
        for trame in self.trameTab:
            dictRes += trame.toDict() + ","
        dictRes = dictRes[:-1] + "}"
        return dictRes

    def toJson(self):
        return json.loads(self.toDictStr())

    def outputJson(self):
        # print("joutput")
        jsonDict = self.toJson()
        with open("./output/output.json", "w") as joutput:
            json.dump(jsonDict, joutput,indent=4)
        joutput.close()

    def outputTrace(self):
        for trame in self.trameTab:
            trame.outputTrame()

    def toString(self):
        res = ""
        for trame in self.trameTab:
            res += trame.toString() + '\n'
        res = res[:-1]
        return res

        
        
Folder = "trames/"
FILES = ["trameEntree.txt", "2trameEntree.txt", 
         "trameEntree_1invalid_line.txt", "trameEntree_inval.txt"]

def get_Trace():
    tabData = get_clean_trame(Folder + FILES[0])
    tab_trame = []

    for line in tabData :
        print(line)
        tab_trame += [Trame(line)]
    t = Trace(tab_trame)
    print(t.outputTrace())