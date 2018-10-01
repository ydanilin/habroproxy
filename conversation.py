class conversationService:
    def __init__(self, dialogClass):
        self.dialogClass = dialogClass
        self.dialogRepository = {}

    def createDialog(self, initialClientRaw):
        # makeRequestFromRaw
        # extract host name
        # check dialog repository and return if exists
        # otherwise create new one
        # add initial request
        # return dialog id
        pass

    def makeRequestFromRaw(self, raw, dialogId):
        pass

    def makeResponseFromRaw(self, raw, dialogId):
        pass

    def makeEstablishedResponse(self, dialogId):
        pass
