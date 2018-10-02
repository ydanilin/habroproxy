class DialogService:
    def __init__(self, dialogClass, requestClass):
        self.dialogClass = dialogClass
        self.requestClass = requestClass
        self.dialogRepository = {}

    def createDialog(self, clientAddress, initialClientRaw):
        dialog = self.dialogClass(clientAddress)
        _id = dialog._id
        self.dialogRepository[_id] = dialog
        request = self.makeRequestFromRaw(initialClientRaw, _id)
        dialog.remoteHost = request.host
        dialog.remotePort = request.port
        return _id
        # makeRequestFromRaw
        # extract host name
        # check dialog repository and return if exists
        # otherwise create new one
        # add initial request
        # return dialog id

    def getDialogByHost(self, hostName):
        result = list(filter(lambda x: x[1].remoteHost.decode() == hostName, self.dialogRepository.items()))
        return result if result else None

    def makeRequestFromRaw(self, raw, dialogId):
        request = self.requestClass.createFromRaw(raw)
        self.dialogRepository[dialogId].conversation.append(request)
        return request

    def makeResponseFromRaw(self, raw, dialogId):
        pass

    def makeEstablishedResponse(self, dialogId):
        pass
