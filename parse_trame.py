
from string import *
from os import error

# supprime les elements parasite

def cleanByte(byte):
    res = ""
    hex_digits = set("0123456789abcdefABCDEF")
    # if (byte.hexdigits()):
    # return byte
    for c in byte:
        if (c in hex_digits):
            res += c
    return res

def is_hexa(byte):
    error = False
    try:
        dec_byte = int("0x" + byte, 16)
    except:
        print("hexa")
        error = True
    return not error


def is_new_trame(byte):
    error = False
    try:
        dec_byte = int("0x" + byte, 16)
    except:
        print("is new")
        error = True
    return dec_byte == 0


def is_valid_offset(byte, oldOffset, readByte):
    error = False
    try:
        dec_byte = int("0x" + byte, 16)
    except:
        print("is valid")
        error = True
    # print("dec_byte :" + str(dec_byte) + " oldOffset : " + str(oldOffset))
    # print(curOffset)
    # print("|old : " + str(oldOffset + dec_byte) + "| cur : " + str(curOffset)+ " |")
    return (error == False and dec_byte == oldOffset + readByte)

def get_clean_trame(file="./trames/trameEntree.txt"):
    result = ""
    offset = 0
    error = False

    with open(file, "r") as fd:
        canRead = True
        invalid_line = False
        nb_line = 0
        curOffset = 0
        oldOffset = 0
        readByte = 0
        isOffset = True
        # isInvalid

        for line in fd:
            nb_line += 1
            splitted = line.split()
            print(splitted)
            isOffset = True
            for byte in splitted:  # check if offset is good
                # check validite de l'offset et si nouvelle trame
                if isOffset:
                    isOffset = False
                    if result != "" and is_new_trame(byte):
                        readByte = 0
                        curOffset = 0
                        oldOffset = 0
                        result += "\n"
                    elif is_valid_offset(byte, oldOffset, readByte):
                        readByte = 0
                        continue
                    else:
                        print("Invalid offset line " + str(nb_line))
                        invalid_line = True
                        return
                # recuperation byte
                # byte = cleanByte(byte)
                if not is_hexa(byte) or (len(byte) != 2 and not isOffset):
                    continue
                result += byte
                readByte += 1
            if invalid_line == False and readByte != 0:
                oldOffset = curOffset
                curOffset += readByte
            else:
                invalid_line = False
    fd.close()
    print(result)
    return result
    
# get_clean_trame()

def outputCleanTrame(cleanStrTrame, file="./trames/trameEntreeClean.txt"):
    with open(file, "w") as output:
        output.write(cleanStrTrame)
    output.close()


# outputCleanTrame(cleanStrTrame=get_clean_trame(
    # file = "./trames/2trameEntree.txt"))
