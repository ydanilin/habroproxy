from habroproxy.lib.logger import configure


log = configure('dialog')


class DialogService:
    def __init__(self, dialogClass, requestClass, responseClass, interceptors=[]):
        self.dialogClass = dialogClass
        self.requestClass = requestClass
        self.responseClass = responseClass
        self.dialogRepository = {}
        self.interceptors = interceptors

    def createDialog(self, clientAddress, initialClientRaw):
        dialog = self.dialogClass(clientAddress)
        _id = dialog._id
        self.dialogRepository[_id] = dialog
        request = self.makeRequestFromRaw(initialClientRaw, _id)
        dialog.remoteHost = request.host
        dialog.remotePort = request.port
        dialog.scheme = 'https' if request.form == 'authority' else 'http'
        # log.debug(request)
        return _id
        # makeRequestFromRaw
        # extract host name
        # check dialog repository and return if exists
        # otherwise create new one
        # add initial request
        # return dialog id

    def getDialogByHost(self, hostName):
        result = list(filter(lambda x: x[1].remoteHost == hostName, self.dialogRepository.items()))
        return result[0] if result else None

    def getDialogById(self, _id):
        return self.dialogRepository[_id]

    def getLastMessage(self, dialogId):
        msgRepo = self.dialogRepository[dialogId].conversation
        return msgRepo[-1] if msgRepo else None

    def makeRequestFromRaw(self, raw, dialogId):
        request = self.requestClass.createFromRaw(raw)
        self.dialogRepository[dialogId].addToConversation(request)
        # if request.form != 'authority':
        #     log.debug(request)
        return request

    def preparePyRequestArgs(self, request, dialogId):
        # dialog = self.dialogRepository[dialogId]
        # scheme = request.scheme if request.scheme else dialog.scheme
        # host = request.host if request.host else dialog.remoteHost
        # port = request.port if request.port else dialog.remotePort
        # url = f'{scheme}://{host}:{port}{request.path}'
        return request.method, request.getFullUrl(), dict(headers=request.headers, data=request.body, stream=True)

    def createPyResponseFormat(self):
        pass

    def makeRawFromPy(self, pyResponse, dialogId):
        response = self.responseClass.createFromPyResponse(pyResponse)
        self.dialogRepository[dialogId].addToConversation(response)
        # log.debug(response)
        # intercept response
        # import pudb; pudb.set_trace()
        t = list(map(lambda x: x.intercept(response), self.interceptors))
        return response.makeRaw()

    def makeEstablishedResponse(self, dialogId):
        req = self.getLastMessage(dialogId)
        return b'%s %d %s\r\n\r\n' % (
            req.http_version.encode(), 200, b'Connection established')
