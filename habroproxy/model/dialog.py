import uuid


class Dialog:
    def __init__(self, clientAddress):
        self._id = uuid.uuid4()
        self.clientHost, self.clientPort = clientAddress
        self.remoteHost = ''
        self.remotePort = 0
        self.conversation = []

    def addToConversation(self, message):
        message.dialog = self
        self.conversation.append(message)
