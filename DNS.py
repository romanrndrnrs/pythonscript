# Si deux fois nb <= 31 lors de la lecture question ou reponse -> fin du mot (pas des caracteres)
# Q -> NAME / TYPE / CLASS
# A -> NAME / TYPE / CLASS / TTL / DATA LENGTH / TYPE ATTRIBUTE (cname/adress)
FLAGDICT = {"8180":"Standard Query Response","0100":"Standard Query"}

from utils import toIpAdress
class DNS:
    def __init__(self,dns):
        self.dns = dns.rstrip("\n")
        self.identification = self.dns[0:4]
        self.flags = self.dns[4:8] #0x8180 -> std query response #0x0100 Standard Query
        self.questions = self.dns[8:12]
        self.intQuestions = int("0x"+self.questions,16)
        self.answerRRs = self.dns[12:16]
        self.intAnswerRRs = int("0x" + self.answerRRs,16)
        self.authorityRRs = self.dns[16:20]
        self.intAuthorityRRs = int("0x"+self.authorityRRs,16)
        self.additionalRRs = self.dns[20:24]
        self.intAdditionalRRs = int("0x"+self.additionalRRs,16)
        self.pointeur = 24
        self.questionNameTab = []
        self.questionTypeTab = []
        self.questionClassTab = []
        for q in range(self.intQuestions):
            res = self.lectureHexName(self.pointeur)
            self.questionNameTab.append(self.hexToAscii(res["res"]))
            self.pointeur = res["pointeur"]
            self.questionTypeTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4
            self.questionClassTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4

        self.answerNameTab = []
        self.answerTypeTab = []
        self.answerClassTab = []
        self.answerTtlTab = []
        self.answerDataLengthTab = []
        self.intAnswerDataLengthTab = []
        self.answerDataTab = []
        for a in range(self.intAnswerRRs):
            res = self.lectureHexName(self.pointeur)
            self.answerNameTab.append(self.hexToAscii(res["res"]))
            self.pointeur = res["pointeur"]
            self.answerTypeTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4
            self.answerClassTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4
            self.answerTtlTab.append(self.dns[self.pointeur:self.pointeur+8])
            self.pointeur += 8
            self.answerDataLengthTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4
            self.intAnswerDataLengthTab.append(int("0x"+self.answerDataLengthTab[-1],16))
            curr = ""
            tempPointeur = self.pointeur
            for l in range(self.intAnswerDataLengthTab[-1]*2):
                curr+=self.dns[self.pointeur:self.pointeur+1]
                self.pointeur += 1
            type = int("0x"+self.answerTypeTab[-1],16)
            if type == 5:
                res = self.lectureHexName(tempPointeur)
                self.answerDataTab.append(self.hexToAscii(res["res"]))
            elif type == 1:
                self.answerDataTab.append(toIpAdress(str(curr)))
            else:
                self.answerDataTab.append(curr)
        
        self.authorityNameTab = []
        self.authorityTypeTab = []
        self.authorityClassTab = []
        self.authorityTtlTab = []
        self.authorityDataLengthTab = []
        self.intAuthorityDataLengthTab = []
        self.authorityDataTab = []
        for a in range(self.intAuthorityRRs):
            res = self.lectureHexName(self.pointeur)
            self.authorityNameTab.append(self.hexToAscii(res["res"]))
            self.pointeur = res["pointeur"]
            self.authorityTypeTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4
            self.authorityClassTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4
            self.authorityTtlTab.append(self.dns[self.pointeur:self.pointeur+8])
            self.pointeur +=8
            self.authorityDataLengthTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4
            self.intAuthorityDataLengthTab.append(int("0x"+self.authorityDataLengthTab[-1],16))
            curr = ""
            tempPointeur = self.pointeur
            for l in range(self.intAuthorityDataLengthTab[-1]*2):
                curr+=self.dns[self.pointeur:self.pointeur+1]
                self.pointeur += 1
            type = int("0x"+self.authorityTypeTab[-1],16)
            if type == 1:
                res = self.lectureHexName(tempPointeur)
                self.authorityDataTab.append(self.hexToAscii(res["res"]))
            elif type == 5:
                self.authorityDataTab.append(toIpAdress(curr))
            else:
                self.authorityDataTab.append(curr)
        self.additionalNameTab = []
        self.additionalTypeTab = []
        self.additionalClassTab = []
        self.additionalTtlTab = []
        self.additionalDataLengthTab = []
        self.intAdditionalDataLengthTab = []
        self.additionalDataTab = []
        for a in range(self.intAdditionalRRs):
            res = self.lectureHexName(self.pointeur)
            self.additionalNameTab.append(self.hexToAscii(res["res"]))
            self.pointeur = res["pointeur"]
            self.additionalTypeTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4
            self.additionalClassTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4
            self.additionalTtlTab.append(self.dns[self.pointeur:self.pointeur+8])
            self.pointeur += 8
            self.additionalDataLengthTab.append(self.dns[self.pointeur:self.pointeur+4])
            self.pointeur += 4
            self.intAdditionalDataLengthTab.append(int("0x"+self.additionalDataLengthTab[-1],16))
            curr = ""
            tempPointeur = self.pointeur
            for l in range(self.intAdditionalDataLengthTab[-1]*2):
                curr+=self.dns[self.pointeur:self.pointeur+1]
                self.pointeur += 1
            type = int("0x"+self.additionalTypeTab[-1],16)
            if type == 1:
                res = self.lectureHexName(tempPointeur)
                self.additionalDataTab.append(self.hexToAscii(res["res"]))
            elif type == 5:
                self.additionalDataTab.append(toIpAdress(curr))
            else:
                self.additionalDataTab.append(curr)

    def hexToAscii(self,tab):
        res = ""
        for elt in tab:
            val =  int("0x"+elt,16)
            if val > 31:
                res+= str(chr(val))
            else:
                res+= "."
        return res[1:-1]

    def lectureHexName(self,pointeur):
        res = []
        while(True):
            if pointeur >= len(self.dns):
                return {"res":res,"pointeur":len(self.dns)-1}
            curr = self.dns[pointeur:pointeur+2]
            if(int("0x"+curr,16) == 192):
                pointeur += 2
                valPointeur = int("0x"+self.dns[pointeur:pointeur+2],16)*2
                res += self.lectureHexName(valPointeur)["res"]
                pointeur += 2
                return {"res":res,"pointeur":pointeur}
            elif(int("0x"+curr,16) != 0):
                res.append(curr)
                pointeur += 2
            else:
                res.append(curr)
                pointeur += 2
                return {"res":res,"pointeur":pointeur}

    
    def toDict(self):
        res = '"DNS":'
        res += '{{"Identification":"{}","Flags":{{"val":"{}","text":"({})"}},"Questions":"{}",'.format("0x"+self.identification,"0x"+self.flags,FLAGDICT[self.flags],self.intQuestions)
        res += '"Answer RRs":"{}","Authority RRs":"{}","Additional RRs":"{}",'.format(self.intAnswerRRs,self.intAuthorityRRs,self.intAdditionalRRs)
        if(self.intQuestions > 0):
            res += '"Queries":{'
            for q in range(self.intQuestions):
                res +='"{}":{{"Name" : "{}","Type":"{}","Class":"{}"}},'.format(q,self.questionNameTab[q],"0x"+self.questionTypeTab[q],"0x"+self.questionClassTab[q])
            res = res[:-1]
            res+= "}"
            
            
            if(self.intAnswerRRs > 0):
                res += ',"Answers":{'
                for a in range(self.intAnswerRRs):
                    res+= '"{}":{{"Name":"{}","Type":"{}","Class":"{}",'.format(a,self.answerNameTab[a],"0x"+self.answerTypeTab[a],"0x"+self.answerClassTab[a])
                    res+= '"Time to live":"{}","Data length":"{}","Data":"{}"}},'.format("0x"+self.answerTtlTab[a],"0x"+self.answerDataLengthTab[a],self.answerDataTab[a])
                res = res[:-1]
                res += "}"
            if(self.intAuthorityRRs > 0):
                res += ',"Authority":{'
                for a in range(self.intAuthorityRRs):
                    res+= '"{}":{{"Name":"{}","Type":"{}"","Class":"{}",'.format(a,self.authorityNameTab[a],"0x"+self.authorityTypeTab[a],"0x"+self.authorityClassTab[a])
                    res+= '"Time to live":"{}","Data length":"{}","Data":"{}"}},'.format("0x"+self.authorityTtlTab[a],"0x"+self.authorityDataLengthTab[a],self.authorityDataTab[a])
                res = res[:-1]
                res += "}"
            if(self.intAdditionalRRs > 0):
                res += ',"Additional":{'
                for a in range(self.intAdditionalRRs):
                    res+= '"{}":{{"Name":"{}","Type":"{}"","Class":"{}",'.format(a,self.additionalNameTab[a],"0x"+self.additionalTypeTab[a],"0x"+self.additionalClassTab[a])
                    res+= '"Time to live":"{}","Data length":"{}","Data":"{}"}},'.format("0x"+self.additionalTtlTab[a],"0x"+self.additionalDataLengthTab[a],self.additionalDataTab[a])
                res = res[:-1]
                res += "}"
        res += "}"
        return res