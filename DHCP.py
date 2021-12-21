from utils import *
from parse_trame import *
import Paquet
import time

dhcp_type = {} 
NORMPATH = "./normes/"
OUTPUTPATH = "./output/"

with open(NORMPATH+"DHCP_type.csv", "r")as dchpf:
    dchpf.readline()
    tempDhcpType = []
    for line in dchpf:
        lineTab = line.split(",")
        # print(lineTab)
        tempDhcpType.append((lineTab[0], lineTab[1]))
dchpf.close()
DHCPTYPE = dict(tempDhcpType) 
# print(DHCPTYPE)

dhcp_type = {} 

with open(NORMPATH+"dhcp_options.csv", "r")as dchpf:
    dchpf.readline()
    tempDhcpOpt = []
    for line in dchpf:
        lineTab = line.split(",")
        # print(lineTab)
        tempDhcpOpt.append((lineTab[0], lineTab[1]))
dchpf.close()
DHCPOPTION = dict(tempDhcpOpt) 
# print(DHCPOPTION)


class DHCP:
    def __init__(self, dhcp):
        self.dhcp = dhcp.rstrip("\n")
        # self.dhcp = dhcp
        self.op = self.dhcp[0:2] #1 = requete, 2 = reponse
        self.htype = self.dhcp[2:4] #type d'@ physique - > 1 = Mac Eth
        self.hlen = self.dhcp[4:6] #len @physique
        self.hops = self.dhcp[6:8] # saut incremente de 1 par routeur
        self.xid = self.dhcp[8:16] # num id unique doit etre identique a celui envoye par client
        self.secs = self.dhcp[16:20] # nb sec depuis init de demande
        self.flags = self.dhcp[20:24] # seul premier bit checke -> B= bit broadcast
        self.ciaddr = self.dhcp[24:32] # @ IP client si il la connait
        self.yiaddr = self.dhcp[32:40] # @ IP affecte par serveur 
        self.siaddr = self.dhcp[40:48]
        self.giaddr = self.dhcp[48:56]
        self.chaddr = self.dhcp[56:68]
        self.chap = self.dhcp[68:88]
        self.sname = get_ascii(dhcp[88:216])
        self.file = get_ascii(dhcp[216:472])
        self.magicCookie = self.dhcp[472:480]
        self.option, next = self.get_option(dhcp[480:])
        self.dhcp_type_name = self.get_dhcp_type_name(self.option)
        self.padding = self.dhcp[480 + next:] 

    def get_dhcp_type_name(self, option):
        for (type, len, content) in option :
            if (type == 53):
                return DHCPTYPE[str(int("0x" + content, 16))]
        return "ret" 
    
    def get_option(self, option):
        ret = []
        i = 0
        while(i < len(option)): 
            type = int("0x" + option[i : i + 2], 16)
            i += 2
            length = int("0x" + option[i : i + 2], 16)
            i += 2
            content = option[i : i + length * 2]
            ret += [(type, length, content)]
            if (type == 255):
                break
            i += length*2
        return ret, i
            
    def flagToString(self, hex):
        valBin = bin(int("0x" + hex, 16))[2:]
        while (len(valBin) < 16):
            valBin = '0' + valBin
        ret = "\tBootp flags: 0x{} ({})\n".format(self.flags, "Broadcast" if(valBin[0] == "1") else "Unicast") 
        ret += "\t\t{}... .... .... .... = Broadcast flag: {}\n".format(valBin[0], "Broadcast" if(valBin[0] == "1") else "Unicast") 
        ret += "\t\t.{} {} {} {} = Reserved flags: 0x{}\n".format(valBin[1:4], valBin[4:8], valBin[8:12], valBin[12:16], hex) 
        return ret

    def flagToStringDict(self, hex):
        valBin = bin(int("0x" + hex, 16))[2:]
        while (len(valBin) < 16):
            valBin = '0' + valBin
        ret = '"Bootp flags": "0x{} ({})",'.format(self.flags, "Broadcast" if(valBin[0] == "1") else "Unicast") 
        ret += '"{}... .... .... .... ": "Broadcast flag: {}",'.format(valBin[0], "Broadcast" if(valBin[0] == "1") else "Unicast") 
        ret += '".{} {} {} {}" : "Reserved flags: 0x{}",'.format(valBin[1:4], valBin[4:8], valBin[8:12], valBin[12:16], hex) 
        return ret
    
    def convertTime(self, seconds):
        convert = time.strftime("%H:%M:%S", time.gmtime(seconds))
        convert = convert.split(":")
        if (int(convert[0]) == 0 and int(convert[1]) == 0):
            return convert[2] + " seconds"
        elif (convert[0] == "00"):
            return convert[1] + " minutes," + convert[2] + " seconds"
        return convert[0] + " hours," + convert[1] + " minutes," + convert[2] + " seconds"
    
# tmpRet = '\tOption: ({}) {} ({})\n'.format(str(optType), DHCPOPTION[str(optType)], toIpAdress(content)) + ret
# tmpRet = '\tOption: ({}) {} ({})\n'.format(str(optType), DHCPOPTION[str(optType)], DHCPTYPE[type]) + ret
    def option_interpret(self, option):
        ret = ""
        for (optType, length, content) in option :
            tmpRet = ""
            tmpRet += '\tOption: ({}) {}{}\n'.format(str(optType), DHCPOPTION[str(optType)], "") #ajouter ecriture pour 53 et 1
            if (optType != 255):
                tmpRet += "\t\tLength: ({})\n".format(str(length))
            if (optType == 1):
                tmpRet += '\t\tSubnet Mask: ({})\n'.format(toIpAdress(content))
            elif (optType == 50):
                tmpRet += '\t\tRequested IP Address: {}\n'.format(toIpAdress(content))
            elif (optType == 53):
                type = str(int("0x" + content, 16))
                tmpRet += '\t\tDHCP: {} ({})\n'.format(DHCPTYPE[type], type)
            elif (optType == 54):
                ret += '\t\tDHCP Server Identifier: {}\n'.format(toIpAdress(content))
            elif (optType == 55):
                i = 0
                while (i < len(content)):
                    opt = str(int("0x" + content[i : i + 2], 16))
                    tmpRet += '\t\tParameter Requested List Item: ({}) {}\n'.format(opt, DHCPOPTION[opt])
                    i += 2
            elif (optType == 51 or optType == 58 or optType == 59):
                timeS = int("0x" + content, 16)
                timeM = self.convertTime(timeS)
                if optType == 51 :
                    tmpRet += '\t\tIP Address Lease Value: ({}s) {}\n'.format(str(timeS), timeM)
                else :
                    typeTime = "Renewal" if type == 58 else "Rebinding" 
                    tmpRet += '\t\t{} Time Value: ({}s) {}\n'.format(typeTime, str(timeS), timeM)
            elif (optType == 61):
                tmpRet += '\t\tHardware type: {} (0x{})\n'.format("Ethernet" if content[0:2] == "01" else "Not available", content[0:2])
                tmpRet += '\t\tClient MAC address: ({})\n'.format(hexToMac(content[2:14]))
            elif (optType == 255):
                tmpRet += '\t\tOption End: ({})\n'.format(str(optType))
            ret += tmpRet
        return ret 
            
    def option_interpret_Dict(self, option):
        ret = ""
        for (optType, length, content) in option :
            # print((optType, length, content))
            tmpRet = ""
            tmpRet += '"Option": "({}) {}",'.format(str(optType), DHCPOPTION[str(optType)]) #ajouter ecriture pour 53 et 1
            if (optType != 255):
                tmpRet += '"Length": "({})",'.format(str(length))
            if (optType == 1):
                tmpRet += '"Subnet Mask": "({})",'.format(toIpAdress(content))
            elif (optType == 50):
                tmpRet += '"Requested IP Address": "{}",'.format(toIpAdress(content))
            elif (optType == 53):
                type = str(int("0x" + content, 16))
                tmpRet += '"DHCP": "{} ({})",'.format(DHCPTYPE[type], type)
            elif (optType == 54):
                ret += '"DHCP Server Identifier": "{}",'.format(toIpAdress(content))
            elif (optType == 55):
                i = 0
                while (i < len(content)):
                    opt = str(int("0x" + content[i : i + 2], 16))
                    tmpRet += '"Parameter Requested List Item": "({}) {}",'.format(opt, DHCPOPTION[opt])
                    i += 2
            elif (optType == 51 or optType == 58 or optType == 59):
                timeS = int("0x" + content, 16)
                timeM = self.convertTime(timeS)
                if optType == 51 :
                    tmpRet += '"IP Address Lease Value": "({}s) {}",'.format(str(timeS), timeM)
                else :
                    typeTime = "Renewal" if type == 58 else "Rebinding" 
                    tmpRet += '"{} Time Value": "({}s) {}",'.format(typeTime, str(timeS), timeM)
            elif (optType == 61):
                tmpRet += '"Hardware type": "{} (0x{})",'.format("Ethernet" if content[0:2] == "01" else "Not available", content[0:2])
                tmpRet += '"Client MAC address": "({})",'.format(hexToMac(content[2:14]))
            elif (optType == 255):
                tmpRet += '"Option End": "({})",'.format(str(optType))
            ret += tmpRet
        # print("ret : " + ret)
        return ret 
    
    def toString(self):
        res = "Dynamic Host Configuration Protocole ({}):\n".format(self.dhcp_type_name)
        res += "\tMessage type: Boot {} ({})\n".format("Request" if self.op == 1 else "Reply", int("0x"+self.op, 16))
        res += "\tHardware type: {} (0x{})\n".format("Ethernet" if self.htype == "01" else "Not available", self.htype)
        res += "\tHardware address length: {}\n".format( int("0x" + self.hlen, 16))
        res += "\tHops: {}\n".format(int("0x" + self.hops, 16))
        res += "\tTransaction ID: 0x{}\n".format(self.xid)
        res += "\tSeconds elapsed: {}\n".format(int("0x" + self.secs, 16))
        res += self.flagToString(self.flags)
        res += "\tClient IP address : {}\n".format(toIpAdress(self.ciaddr))
        res += "\tYour (client) IP address : {}\n".format(toIpAdress(self.yiaddr))
        res += "\tNext server IP address : {}\n".format(toIpAdress(self.siaddr))
        res += "\tRelay agent IP address : {}\n".format(toIpAdress(self.giaddr))
        res += "\tClient MAC address : {}\n".format(hexToMac(self.chaddr))
        res += "\tClient hardware address padding : {}\n".format(self.chap)
        res += "\tServer host name: {}\n".format("not given" if self.sname == "" else self.sname) 
        res += "\tBoot file name : {}\n".format("not given" if self.file == "" else self.file)
        res += "\tMagic cookie: DHCP\n".format("DHCP" if self.magicCookie == "63825363" else "Bootp not supported")
        res += self.option_interpret(self.option)
        res += "\tPadding: {}\n".format(self.padding)
        return res

    def toDict(self):
        dictStr = '"Dynamic Host Configuration Protocole ({})":'.format(self.dhcp_type_name)
        dictStr += '{{"Message type": "Boot {} ({})",'.format("Request" if self.op == 1 else "Reply", int("0x"+self.op, 16))
        dictStr += '"Hardware type": "{} (0x{})",'.format("Ethernet" if self.htype == "01" else "Not available", self.htype)
        dictStr += '"Hardware address length": "{}",'.format( int("0x" + self.hlen, 16))
        dictStr += '"Hops": "{}",'.format(int("0x" + self.hops, 16))
        dictStr += '"Transaction ID": "0x{}",'.format(self.xid)
        dictStr += '"Seconds elapsed": "{}",'.format(int("0x" + self.secs, 16))
        dictStr += self.flagToStringDict(self.flags)
        dictStr += '"Client IP address" : "{}",'.format(toIpAdress(self.ciaddr))
        dictStr += '"Your (client) IP address" : "{}",'.format(toIpAdress(self.yiaddr))
        dictStr += '"Next server IP address" : "{}",'.format(toIpAdress(self.siaddr))
        dictStr += '"Relay agent IP address" : "{}",'.format(toIpAdress(self.giaddr))
        dictStr += '"Client MAC address" : "{}",'.format(hexToMac(self.chaddr))
        dictStr += '"Client hardware address padding" : "{}",'.format(self.chap)
        dictStr += '"Server host name": "{}",'.format("not given" if self.sname == "" else self.sname) 
        dictStr += '"Boot file name" : "{}",'.format("not given" if self.file == "" else self.file)
        dictStr += '"Magic cookie": "{}",'.format("DHCP" if self.magicCookie == "63825363" else "Bootp not supported")
        dictStr += self.option_interpret_Dict(self.option)
        # print(self.option_interpret_Dict(self.option))
        # print(dictStr)
        # dictStr += '"Padding": "{}"}}'.format(self.padding)
        dictStr += '"Padding": "{}"'.format(self.padding)
        dictStr += "}"
        # print(self.toString())
        return dictStr
    
# discover = "0101060000003d1d0000000000000000000000000000000000000000000b8201fc4200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000638253633501013d0701000b8201fc4232040000000037040103062aff00000000000000"
# offer = "0201060000003d1d0000000000000000c0a8000ac0a8000100000000000b8201fc4200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000638253633501020104ffffff003a04000007083b0400000c4e330400000e103604c0a80001ff0000000000000000000000000000000000000000000000000000"
# request = "0101060000003d1e0000000000000000000000000000000000000000000b8201fc4200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000638253633501033d0701000b8201fc423204c0a8000a3604c0a8000137040103062aff00"
# ack = "0201060000003d1e0000000000000000c0a8000a0000000000000000000b8201fc4200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000638253633501053a04000007083b0400000c4e330400000e103604c0a800010104ffffff00ff0000000000000000000000000000000000000000000000000000"
# test = get_clean_trame("dhcp.txt")
# eth = Paquet(test)
# udp = .data
# dhcp = udp.data
# print(dhcp)
# ex = DHCP(test)
# print(ex.toString())