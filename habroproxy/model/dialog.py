"""
    represents a single client cycle:
    - request client - proxy (with handshake procedure if necessary)
    - request proxy - remote
    - response remote - proxy
    - response proxy - client
"""
import uuid


class Dialog:  # pylint:disable=too-few-public-methods
    """ single client cycle is called Dialog """
    def __init__(self, client_address):
        self._id = uuid.uuid4()
        self.client_host, self.client_port = client_address
        self.remote_host = ''
        self.remote_port = 0
        self.conversation = []

    def add_to_conversation(self, message):
        """ saves to conversation repository """
        message.dialog = self
        self.conversation.append(message)
