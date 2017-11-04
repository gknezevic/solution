from hackathon.utils.utils import ResultsMessage, DataMessage

def saveReceivedStatus(msg:DataMessage, listOfStatuses):
    listOfStatuses.insert(0, msg)
    if len(listOfStatuses) > 1440:
        listOfStatuses = listOfStatuses[0:1440]
    return listOfStatuses

def saveSentStatus(res:ResultsMessage, listOfResponses):
    listOfResponses.insert(0, res)
    if len(listOfResponses) > 1440:
        listOfResponses = listOfResponses[0:1440]
    return listOfResponses