def createDF(title, variables):
    file = open(f"{title}.data", "w+")
    data = ""
    for variable in variables:
        data += f"{variable}=\n"
    data = data[:-1]
    file.write(data)
    file.close()

def writeVar(title, variable, towrite):
    file = open(f"{title}.data", "r")
    data = file.readlines()
    file.close()
    file = open(f"{title}.data", "w+")
    strdata = ""    
    for line in data:
        loc = line.find("=")
        if line[:loc] == variable:
            strdata += line[:loc] + "=" + towrite + "\n"
        else:
            strdata += f"{line}"
    print(strdata)
    file.write(strdata)
    file.close()

def readVar(title, variable):
    file = open(f"{title}.data", "r")
    data = file.readlines()
    for line in data:
        loc = line.find("=")
        if line[:loc] == variable:
            file.close()
            return line[loc+1:].replace("\n", "")
    file.close()
