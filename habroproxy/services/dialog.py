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
        return result[0] if result else None

    def getLastMessage(self, dialogId):
        msgRepo = self.dialogRepository[dialogId].conversation
        return msgRepo[-1] if msgRepo else None

    def makeRequestFromRaw(self, raw, dialogId):
        request = self.requestClass.createFromRaw(raw)
        self.dialogRepository[dialogId].conversation.append(request)
        return request

    def preparePyRequestArgs(self, request, dialogId):
        # TODO refactor in a way that dialog class grabs scheme, host, port asap from conversation flow
        if request.form == 'relative':
            pass
        t = f'{self.scheme}://{self.host}:{self.port}{self.path}'
        pass
        # return method, url, kwargs
        # headers dict, stream=True

    def createPyResponseFormat(self):
        pass

    def makeResponseFromRaw(self, raw, dialogId):
        pass

    def makeEstablishedResponse(self, dialogId):
        req = self.getLastMessage(dialogId)
        return b'%s %d %s\r\n\r\n' % (
            req.http_version, 200, b'Connection established')
