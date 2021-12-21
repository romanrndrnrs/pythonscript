def toIpAdress(hexIp):
    # print("hex ip is {}".format(hexIp))
    if(len(hexIp) == 8):
        res = ""
        res = res + str(int("0x"+hexIp[0:2], 16))+"."
        res = res + str(int("0x"+hexIp[2:4], 16))+"."
        res = res + str(int("0x"+hexIp[4:6], 16))+"."
        res = res + str(int("0x"+hexIp[6:8], 16))
        return res
    else:
        console.log("Erreur: Mauvaise taille hexa pour IP")
        return False

def hexToMac(hexMac):
    if(len(hexMac) == 12):
        res = hexMac[0:2] + ":" + hexMac[2:4] + ":" + hexMac[4:6] + \
            ":" + hexMac[6:8] + ":" + hexMac[8:10] + ":" + hexMac[10:12]
        return res
    else:
        console.log("Erreur : mauvaise taille d'adresse mac : {}".format(len(hexMac)))
        return False

def get_ascii(str):
    res = ""
    i = 0
    while(i < len(str)):
        curr = str[i : i + 2]
        if (curr == "00"):
            break
        res += chr(int("0x" + curr, 16))
        i += 2
    return res

# print(get_ascii("30313233343500000000000031231"))