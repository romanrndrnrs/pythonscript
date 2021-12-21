from utils import toIpAdress
from Datagramme import Datagramme
import json
NORMPATH = "./normes/"
with open(NORMPATH+"protocol.txt", "r") as protf:
    protf.readline()
    tempProtType = []
    for line in protf:
        lineTab = line.split(" ",1)
        if(len(lineTab) > 1):
            tempProtType.append((lineTab[0].zfill(2), lineTab[1].rstrip()))
protf.close()
PROTTYPE = dict(tempProtType)


class Paquet:
    def __init__(self, paquet):
        self.paquet = paquet.lower()
        self.version = self.paquet[0:1]
        self.headerLength = self.paquet[1:2]
        self.tos = self.paquet[2:4]
        self.totalLength = self.paquet[4:8]
        self.identifier = self.paquet[8:12]
        self.fragment = self.paquet[12:16]
        self.ttl = self.paquet[16:18]
        self.protocol = self.paquet[18:20]
        self.headerChecksum = self.paquet[18:24]
        self.srcIp = self.paquet[24:32]
        self.dstIp = self.paquet[32:40]
        self.entete = paquet[0:40]
        self.optionBool = False
        self.intHL = int("0x"+self.headerLength, 16)*4*2
        if(self.headerLength != "5"):
            self.optionBool = True
            self.option = paquet[40:self.intHL]
            self.optionType = self.option[0:2]
            self.optionLength = self.option[2:4]
            intOptionLength = int("0x"+self.optionLength, 16)*2
            self.optionPointeur = self.option[4:6]
            self.optionData = self.option[6:6+intOptionLength]
            self.optionPadding = self.option[6+intOptionLength:]
        self.icmpBool = False
        if(self.protocol == "01"):
            self.icmpBool = True
            self.messageIcmp = paquet[self.intHL:]
            self.icmpType = self.messageIcmp[0:2]
            self.icmpCode = self.messageIcmp[2:4]
            self.icmpChecksum = self.messageIcmp[4:8]
            self.icmpIdentifier = self.messageIcmp[8:12]
            self.icmpSequenceNumber = self.messageIcmp[12:16]
            self.icmpData = self.messageIcmp[16:]
        # if(self.protocol == "01"):
        if(self.optionBool):
            self.data = paquet[self.intHL:]
        else:
            self.data = paquet[40:]
        self.datagramme = Datagramme(self.data)



    def hexToDec(self, hex):
        return int("0x"+hex, 16)

    def fragmentToString(self, hex):
        valBin = bin(int("0x"+hex, 16))
        valBin = str(valBin)
        valBin = valBin[2:]
        valBin = valBin.zfill(16)
        valBin = "0b" + valBin
        return "Fragmentation: "+valBin+" (Reserve: {} - Don't Fragment: {} - More Fragments: {} - Fragment Offset: {})\n".format(valBin[2:3], valBin[3:4], valBin[4:5], int("0b"+valBin[5:], 2))

    def toString(self):
        res = "IP:\n"
        res += "\tVersion: {}\n\tLongueur de l'entete: {} ({} octets)\n\tType of Service: {} ({})\n".format(
            self.version, "0x"+self.headerLength, int("0x"+self.headerLength, 16)*4, "0x"+self.tos, int("0x"+self.tos, 16))
        res += "\tLongueur Totale: {} ({} octets)\n\tIdentification: {} ({})\n\t{}".format("0x"+self.totalLength, int(
            "0x"+self.totalLength, 16), "0x"+self.identifier, int("0x"+self.identifier, 16), self.fragmentToString(self.fragment))
        res += "\tTime To Live: {} ({})\n\tProtocole: {} ({})\n\tChecksum Entete: {}\n".format("0x"+self.ttl, int(
            "0x"+self.ttl, 16), int("0x"+self.protocol, 16), PROTTYPE[self.protocol], "0x"+self.headerChecksum)
        res += "\tAdresse Ip Source: {}\n\tAdresse Ip Destination: {}\n".format(
            toIpAdress(self.srcIp), toIpAdress(self.dstIp))
        if(self.optionBool):
            pass  # a faire plus tard
        if(self.icmpBool):
            pass  # a faire plus tard
        return res + self.datagramme.toString()

    def toDict(self):
        dictStr = '"IP":'
        dictStr += '{{"Version":"{}","Longueur Entete":{{"hexa":"{}","octet":"({} octets)"}},"TOS": {{"hexa":"{}","octet":"({})"}},'.format(
            self.version, "0x"+self.headerLength, int("0x"+self.headerLength, 16)*4, "0x"+self.tos, int("0x"+self.tos, 16))
        dictStr += '"Longueur Totale":{{"hexa":"{}","octet":"({} octets)"}},"Identification": {{"hexa":"{}","octet":"({})"}},"Fragmentation":"{}",'.format(
            "0x"+self.totalLength, int("0x"+self.totalLength, 16), "0x"+self.identifier, int("0x"+self.identifier, 16), self.fragmentToString(self.fragment)[:-1])
        dictStr += '"Time to live":{{"hexa":"{}","octet":"({})"}},"Protocole":{{"hexa":"{}","valeur":"{}" }},"Checksum Entete":"{}",'.format(
            "0x"+self.ttl, int("0x"+self.ttl, 16), int("0x"+self.protocol, 16), PROTTYPE[self.protocol], "0x"+self.headerChecksum)
        dictStr += '"Adresse Ip Source":"{}", "Adresse Ip Destination":"{}"}},'.format(
            toIpAdress(self.srcIp), toIpAdress(self.dstIp)) + self.datagramme.toDict()
        return dictStr

    def toJson(self):
        return json.loads(self.toDict())

# print(Paquet.fragmentToString("0A26"))
