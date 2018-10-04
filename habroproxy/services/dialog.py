class DialogService:
    def __init__(self, dialogClass, requestClass, responseClass):
        self.dialogClass = dialogClass
        self.requestClass = requestClass
        self.responseClass = responseClass
        self.dialogRepository = {}

    def createDialog(self, clientAddress, initialClientRaw):
        dialog = self.dialogClass(clientAddress)
        _id = dialog._id
        self.dialogRepository[_id] = dialog
        request = self.makeRequestFromRaw(initialClientRaw, _id)
        dialog.remoteHost = request.host
        dialog.remotePort = request.port
        dialog.scheme = 'https' if request.form == 'authority' else 'http'
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
        dialog = self.dialogRepository[dialogId]
        scheme = request.scheme.decode() if request.scheme else dialog.scheme
        host = request.host.decode() if request.host else dialog.remoteHost.decode()
        port = request.port if request.port else dialog.remotePort
        url = f'{scheme}://{host}:{port}{request.path.decode()}'
        decodedHeaders = dict(map(lambda x: (x[0], x[1].decode()), request.headers.items()))
        return request.method.decode(), url, dict(headers=decodedHeaders, stream=True)

    def createPyResponseFormat(self):
        pass

    def makeRawFromPy(self, pyResponse, dialogId):
        response = self.responseClass.createFromPyResponse(pyResponse)
        self.dialogRepository[dialogId].conversation.append(response)
        return response.makeRaw()

    def makeEstablishedResponse(self, dialogId):
        req = self.getLastMessage(dialogId)
        return b'%s %d %s\r\n\r\n' % (
            req.http_version, 200, b'Connection established')
