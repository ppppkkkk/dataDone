import re
import os


def readConferData(filename):
    f = open(filename, 'r', encoding='utf-8')
    str1 = f.read()
    res = '\[c[0-9]+]\t\t.*:\n.*: [0-9]+-[0-9]+'
    ret = re.findall(res, str1)
    f.close()
    return ret


def writeConfer(conferData):
    fUserInfo = open("conferUserInfo.txt", 'a', encoding='utf-8')
    fUserPair = open("conferUserPair.txt", 'a', encoding='utf-8')
    name = []
    for i in range(len(conferData)):
        index1 = conferData[i].find('\n')
        index2 = conferData[i].rfind(':')
        nameStr = conferData[i][0:index1]
        res = '[a-zA-Zé]* [a-zA-Zé]*,|[a-zA-Zé]* [a-zA-Zé]*:|[a-zA-Zé]*-[a-zA-Zé]* [a-zA-Zé]*,|[a-zA-Zé]* [a-zA-Zé]*-[a-zA-Zé]*,|[a-zA-Zé]* [a-zA-Zé]* [a-zA-Zé]*,'
        name = re.findall(res, nameStr)

        for j in range(len(name)):
            name[j] = name[j].replace(':', ',').strip()

        conferStr = conferData[i][index1 + 1:index2]
        confer = conferStr.replace('.', ',')
        index3 = confer.rfind(',')
        confer = list(confer)
        confer[index3 + 1] = ''
        confer = ''.join(confer)
        year = confer[-4:]

        for j in range(len(name)):
            for k in range(len(name)):
                if j < k:
                    fUserPair.write(name[j] + name[k] + year + '\n')

        for j in range(len(name)):
            fUserInfo.write(name[j] + confer + '\n')

    nameTotal = name[0]
    fUserInfo.close()
    fUserPair.close()
    return nameTotal


def readJourData(filename):
    f = open(filename, 'r', encoding='utf-8')
    str1 = f.read()
    res = '\[j[0-9]+]\t\t.*:\n.*'
    ret = re.findall(res, str1)
    f.close()
    return ret


def writeJourData(jourData):
    fUserInfo = open("jourUserInfo.txt", 'a', encoding='utf-8')
    fUserPair = open("jourUserPair.txt", 'a', encoding='utf-8')
    nameTotal = []
    for i in range(len(jourData)):
        index1 = jourData[i].find('\n')
        nameStr = jourData[i][0:index1]
        res = '[a-zA-Zé]* [a-zA-Zé]* [a-zA-Zé]* [a-zA-Zé]*,|[a-zA-Zé]* [a-zA-Zé]*,|[a-zA-Zé]* [a-zA-Zé]*:|[a-zA-Zé]*-[a-zA-Zé]* [a-zA-Zé]*,|[a-zA-Zé]* [a-zA-Zé]*-[a-zA-Zé]*,|[a-zA-Zé]* [a-zA-Zé]* [a-zA-Zé]*,'
        name = re.findall(res, nameStr)

        for j in range(len(name)):
            name[j] = name[j].replace(':', ',').strip()

        jourStr = jourData[i][index1 + 1:]
        year = jourStr[-6:]
        year = year[1:5]

        res = '.*[a-z]'
        jourStr = re.findall(res, jourStr)
        jourStr = "".join(jourStr)
        index2 = jourStr.find('.')
        articleName = jourStr[:index2]
        jourName = jourStr[index2 + 1:].strip()
        for j in range(len(name)):
            for k in range(len(name)):
                if j < k:
                    fUserPair.write(name[j] + name[k] + year + '\n')

        for j in range(len(name)):
            fUserInfo.write(name[j] + articleName + ',' + jourName + ',' + year + '\n')

    nameTotal = name[0]
    # print(nameTotal)
    fUserInfo.close()
    fUserPair.close()
    return nameTotal


def searchFile(dirPath):
    dirs = os.listdir(dirPath)
    name = []
    for currentFile in dirs:
        fullPath = dirPath + '/' + currentFile
        if currentFile.split('_')[-1] == 'huiyi.txt':
            conferData = readConferData(fullPath)
            name1 = writeConfer(conferData)
            name.append(name1)

        if currentFile.split('_')[-1] == 'qikan.txt':
            JourData = readJourData(fullPath)
            name2 = writeJourData(JourData)
            name.append(name2)


def setID(namelist):
    f = open("idName.txt", 'w', encoding='utf-8')
    i = 0
    length = len(namelist)
    idAndName = {}
    while length > 0:
        length = length - 1
        key = 'p' + str(i)
        value = namelist[i]
        idAndName[key] = value
        f.write(key + ',' + value + '\n')
        i = i + 1
    f.close()


def readIdName():
    f = open("idName.txt", 'r', encoding='utf-8')
    idAndName = {}
    str1 = f.readlines()
    for i in range(len(str1)):
        key = str1[i].split(',')[0]
        value = str1[i].split(',')[1]
        idAndName[key] = value

    f.close()
    return idAndName


def readNameArticle():
    f = open("rejourUserInfo.txt", 'r', encoding='utf-8')
    nameAndArticle = {}
    str1 = f.readlines()
    for i in range(len(str1)):
        key = str1[i].split(',', 2)[1]
        value = str1[i].split(',', 2)[2].rstrip('\n')
        #nameAndArticle[key] = [].append(value)
        nameAndArticle.setdefault(key, []).append(value)
    f.close()
    return nameAndArticle


def readNameConfer():
    f = open("reconferUserInfo.txt", 'r', encoding='utf-8')
    nameAndConfer = {}
    str1 = f.readlines()
    for i in range(len(str1)):
        key = str1[i].split(',', 2)[1]
        value = str1[i].split(',', 2)[2].rstrip('\n')
        nameAndConfer.setdefault(key, []).append(value)
    f.close()
    return nameAndConfer


def rewriteConferUserPair(idAndName):
    fr = open("conferUserPair.txt", 'r', encoding='utf-8')
    fw = open("reconferUserPair.txt", 'w', encoding='utf-8')
    str1 = fr.readlines()
    idList = []
    namelist = []
    str2 = ""
    for key, value in idAndName.items():
        idList.append(key)
        namelist.append(value)

    for i in range(len(str1)):
        str2 = ""
        name1 = str1[i].split(',')[0] + '\n'
        if name1 in namelist:
            id1Index = namelist.index(name1)
            id1 = idList[id1Index]
            str2 = str2 + id1 + ","
        name2 = str1[i].split(',')[1] + '\n'
        if name2 in namelist:
            id2Index = namelist.index(name2)
            id2 = idList[id2Index]
            str2 = str2 + id2 + ","
        year = str1[i].split(',')[2]
        str2 = str2 + year
        fw.write(str2)

    fr.close()
    fw.close()


def rewriteJourUserPair(idAndName):
    fr = open("jourUserPair.txt", 'r', encoding='utf-8')
    fw = open("rejourUserPair.txt", 'w', encoding='utf-8')
    str1 = fr.readlines()
    idList = []
    namelist = []
    str2 = ""
    for key, value in idAndName.items():
        idList.append(key)
        namelist.append(value)

    for i in range(len(str1)):
        str2 = ""
        name1 = str1[i].split(',')[0] + '\n'
        if name1 in namelist:
            id1Index = namelist.index(name1)
            id1 = idList[id1Index]
            str2 = str2 + id1 + ","
        name2 = str1[i].split(',')[1] + '\n'
        if name2 in namelist:
            id2Index = namelist.index(name2)
            id2 = idList[id2Index]
            str2 = str2 + id2 + ","
        year = str1[i].split(',')[2]
        str2 = str2 + year
        fw.write(str2)

    fr.close()
    fw.close()


def rewriteConferUserInfo(idAndName):
    fr = open("conferUserInfo.txt", 'r', encoding='utf-8')
    fw = open("reconferUserInfo.txt", 'w', encoding='utf-8')
    str1 = fr.readlines()
    idList = []
    namelist = []
    str2 = ""
    for key, value in idAndName.items():
        idList.append(key)
        namelist.append(value)

    for i in range(len(str1)):
        str2 = ""
        str3 = str1[i].rsplit(',', 1)[0]
        name1 = str3.split(',', 1)[0] + '\n'
        if name1 in namelist:
            id1Index = namelist.index(name1)
            id1 = idList[id1Index]
            str2 = str2 + id1 + "," + str3 + '\n'
        fw.write(str2)

    fr.close()
    fw.close()


def rewriteJourUserInfo(idAndName):
    fr = open("jourUserInfo.txt", 'r', encoding='utf-8')
    fw = open("rejourUserInfo.txt", 'w', encoding='utf-8')
    str1 = fr.readlines()
    idList = []
    namelist = []
    str2 = ""
    for key, value in idAndName.items():
        idList.append(key)
        namelist.append(value)

    for i in range(len(str1)):
        str2 = ""
        str3 = str1[i].rsplit(',', 2)[0]
        name1 = str3.split(',', 1)[0] + '\n'
        if name1 in namelist:
            id1Index = namelist.index(name1)
            id1 = idList[id1Index]
            str2 = str2 + id1 + "," + str3 + '\n'
        fw.write(str2)

    fr.close()
    fw.close()


def reRewriteJourUserInfo(idAndName, nameAndArticle):
    #print(idAndName)
    fw = open("rerejourUserInfo.txt", 'w', encoding='utf-8')
    idList = []
    namelist = []
    str1 = ""
    for key, value in idAndName.items():
        idList.append(key)
        namelist.append(value.rstrip('\n'))
    for name, articles in nameAndArticle.items():
        str1 = ""
        if name in namelist:
            id1Index = namelist.index(name)
            id1 = idList[id1Index]
            str1 = str1 + id1 + ',' + name + ','
            articles1 = []
            for i in articles:
                if i not in articles1:
                    articles1.append(i)

            for article in articles1:
                str1 = str1 + article + ','
        str1 = str1[0:-1]
        str1 = str1 + '\n'
        #print(str1)
        fw.write(str1)
    fw.close()


def reRewriteConferUserInfo(idAndName, nameAndConfer):
    #print(idAndName)
    fw = open("rereconferUserInfo.txt", 'w', encoding='utf-8')
    idList = []
    namelist = []
    str1 = ""
    for key, value in idAndName.items():
        idList.append(key)
        namelist.append(value.rstrip('\n'))
    for name, confers in nameAndConfer.items():
        str1 = ""
        if name in namelist:
            id1Index = namelist.index(name)
            id1 = idList[id1Index]
            str1 = str1 + id1 + ',' + name + ','
            confers1 = []
            for i in confers:
                if i not in confers1:
                    confers1.append(i)

            for confer in confers1:
                str1 = str1 + confer + ','
        str1 = str1[0:-1]
        str1 = str1 + '\n'
        #print(str1)
        fw.write(str1)
    fw.close()


if __name__ == '__main__':
    idAndName = readIdName()
    #rewriteConferUserInfo(idAndName)
    nameAndArticle = readNameArticle()
    nameAndConfer = readNameConfer()
    reRewriteConferUserInfo(idAndName, nameAndConfer)
    reRewriteJourUserInfo(idAndName, nameAndArticle)
    # rewriteConferUserPair(idAndName)
    # rewriteJourUserPair(idAndName)

    #rewriteJourUserInfo(idAndName)
    # name = searchFile('B:/BaiduNetdiskDownload/data')

