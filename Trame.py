import json
from Paquet import Paquet
from utils import *
NORMPATH = "./pythonScript/normes/"
OUTPUTPATH = "./pythonScript/output/"
with open(NORMPATH+"ethtype.txt", "r")as ethtf:
    ethtf.readline()
    tempEthType = []
    for line in ethtf:
        lineTab = line.split(" ",1)
        tempEthType.append((lineTab[0], lineTab[1].rstrip()))
ethtf.close()
ETHTYPE = dict(tempEthType)


class Trame:
    id = 1

    def __init__(self, trame):
        # mise en forme pour harmonisation du traitement
        self.trame = trame.lower().rstrip("\n")
        self.entete = trame[0:28]
        self.data = trame[28:]
        self.id = Trame.id
        self.destMac = hexToMac(self.entete[0:12])
        self.srcMac = hexToMac(self.entete[12:24])
        self.type = {
            "Hexadecimal": self.entete[24:28], "Definition": ETHTYPE[self.entete[24:28]]}
        self.paquet = Paquet(self.data)
        Trame.id += 1

    @classmethod
    def initId(self):
        Trame.id = 1
    def outputTrame(self):
        with open(OUTPUTPATH+"output.txt", "a") as output:
            if(self.id != 1):
                output.write("\n")  # Retour a la ligne
            output.write(self.toString())
        output.close()

    # Convertir une valeur hexadecimale d'adresse mac en une adresse mac avec les separateurs

    def toString(self):
        return "Trame numero {}:\nEthernet:\n\tAdresse MAC Destination: {}\n\tAdresse MAC Source: {}\n\tType (Ox{}): {}".format(self.id, self.destMac, self.srcMac, self.type["Hexadecimal"], self.type["Definition"]) + self.paquet.toString()

    def toDict(self):
        dictStr = '"Trame numero {}":'.format(self.id)
        dictStr += '{"Ethernet":'
        dictStr += '{{"Adresse MAC Destination":"{}","Adresse Max Source":"{}","Type":{{"hexa":"{}","Definition":"{}"}}}},'.format(
            self.destMac, self.srcMac, "0x"+self.type["Hexadecimal"], self.type["Definition"])
        dictStr += self.paquet.toDict()
        dictStr += '}'
        return dictStr

    def toJson(self):
        return json.loads(self.toDict())


#f = open("udp.txt", "r")
#t = Trame(f.readline())
# t.outputTrame()
# print(t.toString())
# print(str(t.toJson()))
#jsonDict = t.toJson()
# with open(OUTPUTPATH+"output.json", "w") as joutput:
#    json.dump(jsonDict, joutput)
# print(t.toDict())

#dico = '{{"data":"Internet Protocol version 4 (IPv4)","test":{{"1":{},"2":{} }} }}'.format(2,1)
#res = json.loads(dico)
# print(str(res))
# Formatage d'ethtype pour creation de dico
# with open(NORMPATH+"ieee-802-numbers-1.txt", "r") as f:
#     with open(NORMPATH+"ethtype.txt", "w") as ethf:
#         for line in f:
#             lineTab = line.split(maxsplit=1)
#             typesEth = lineTab[0].split("-")
#             for typeEth in typesEth:
#                 typeEth = typeEth.zfill(4)
#                 ethf.write(typeEth+" "+lineTab[1])
#     ethf.close()
# f.close()
