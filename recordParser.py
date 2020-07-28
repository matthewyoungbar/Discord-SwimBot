
def parseRecords(fileName):
    recordList = open(fileName).read().strip().split("\n")
    recordDict = dict()
    nameDict = dict()
    for record in recordList:
        splitRecord = record.split()
        if len(splitRecord) == 6:
            event = splitRecord[0] + " " + splitRecord[1]
            name = splitRecord[2] + " " + splitRecord[3]
            if recordDict.get(event) == None:
                recordDict[event] = [{"name": name, "time": splitRecord[4], "year": splitRecord[5]}]
            else:
                recordDict[event].append({"name": name, "time": splitRecord[4], "year": splitRecord[5]})
            if nameDict.get(name) == None:
                nameDict[name] = [{"event": event, "time": splitRecord[4], "year": splitRecord[5]}]
            else:
                nameDict[name].append({"event": event, "time": splitRecord[4], "year": splitRecord[5]})
    return recordDict, nameDict
