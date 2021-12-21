from DHCP import DHCP
from DNS import DNS
class Datagramme:
    def __init__(self, datagramme):
        self.datagramme = datagramme
        self.srcPort = self.datagramme[0:4]
        self.dstPort = self.datagramme[4:8]
        self.length = self.datagramme[8:12]
        self.checksum = self.datagramme[12:16]
        self.data = self.datagramme[16:]
        self.bool = False
        if (int("0x"+self.srcPort, 16) == 67 or int("0x"+self.srcPort, 16) == 68) and (int("0x"+self.dstPort, 16) == 67 or int("0x"+self.dstPort, 16) == 68):
            self.data =  DHCP(self.data)
            self.bool = True
        elif int("0x"+self.srcPort, 16) == 53 or int("0x" + self.dstPort, 16) == 53 :
            self.data =  DNS(self.data)
            self.bool = True
        else:
            pass

    def toString(self):
        res = "UDP:\n"
        res += "\tPort Source: {}\n\tPort Destination {}\n\tLongueur: {} ({} octets)\n\tChecksum: {}\n".format(int(
            "0x"+self.srcPort, 16), int("0x"+self.dstPort, 16), "0x"+self.length, int("0x"+self.length, 16), "0x"+self.checksum)
        return res

    def toDict(self):
        if(self.bool):
            dictStr = '"UDP":{{"Port Source": "{}", "Port Destination": "{}", "Longueur":{{"hexa":"{}","octet":"({} octets)"}},"Checksum":"{}" }},'.format(int(
            "0x"+self.srcPort, 16), int("0x"+self.dstPort, 16), "0x"+self.length, int("0x"+self.length, 16), "0x"+self.checksum)+self.data.toDict()
        else:
            dictStr = '"UDP":{{"Port Source": "{}", "Port Destination": "{}", "Longueur":{{"hexa":"{}","octet":"({} octets)"}},"Checksum":"{}" }}'.format(int(
            "0x"+self.srcPort, 16), int("0x"+self.dstPort, 16), "0x"+self.length, int("0x"+self.length, 16), "0x"+self.checksum)
        return dictStr