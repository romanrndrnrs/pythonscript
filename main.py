from parse_trame import *
from Trame import *
from Trace import *

outputCleanTrame(cleanStrTrame=get_clean_trame(file="./dns-mine.txt"),file="./cleanTrace.txt")
Trame.initId()
trace = []
with open("./cleanTrace.txt", "r") as cleanTrame:
    for line in cleanTrame:
        trace.append(Trame(line))
    cleanTrame.close()
try:
    traceObj = Trace(trace)
    with open("./output.json","w") as output:
        output.write(traceObj.toDictStr())
    #print(traceObj.toJson())
except:
    with open("./output.json","w") as output:
        output.write('{"Erreur":"Veuillez selectionner un fichier valide"}')