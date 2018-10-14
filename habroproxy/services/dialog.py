"""
    The service provides functions to handle the habroproxy
    request/response flow, both client's and remote's
"""
from habroproxy.lib.logger import configure


LOGGER = configure('dialog')


class DialogService:
    """ The service class """
    def __init__(self, dialog_class, request_class, response_class, interceptors=None):
        self.dialog_class = dialog_class
        self.request_class = request_class
        self.response_class = response_class
        self.dialog_repository = {}
        self.interceptors = interceptors if interceptors else []

    def create_dialog(self, client_address, initial_client_raw):
        """ See /models/dialog.py for details """
        dialog = self.dialog_class(client_address)
        _id = dialog._id
        self.dialog_repository[_id] = dialog
        request = self.make_request_from_raw(initial_client_raw, _id)
        dialog.remote_host = request.host
        dialog.remote_port = request.port
        dialog.scheme = 'https' if request.form == 'authority' else 'http'
        # LOGGER.debug(request)
        return _id
        # makeRequestFromRaw
        # extract host name
        # check dialog repository and return if exists
        # otherwise create new one
        # add initial request
        # return dialog id

    def get_dialog_by_host(self, host_name):
        """ Scans repository of dialogs to get by host name """
        # pylint: disable=line-too-long
        result = list(filter(lambda x: x[1].remote_host == host_name, self.dialog_repository.items()))
        return result[0] if result else None

    def get_dialog_by_id(self, _id):
        """ Get by uuid id from the repository of dialogs """
        return self.dialog_repository[_id]

    def get_last_message(self, dialog_id):
        """ Returns last saved message from the dialig specified by id """
        msg_repo = self.dialog_repository[dialog_id].conversation
        return msg_repo[-1] if msg_repo else None

    def make_request_from_raw(self, raw, dialog_id):
        """ Make from raw http string """
        request = self.request_class.create_from_raw(raw)
        self.dialog_repository[dialog_id].add_to_conversation(request)
        return request

    def prepare_py_request_args(self, request):  # pylint: disable=no-self-use
        """ Arguments to create Request class in requests library """
        return (request.method,
                request.get_full_url(),
                dict(headers=request.headers, data=request.body, stream=True))

    def make_raw_from_py(self, py_response, dialog_id):
        """ Raw http string from requests library response """
        response = self.response_class.create_from_py_response(py_response)
        self.dialog_repository[dialog_id].add_to_conversation(response)
        # LOGGER.debug(response)
        # intercept response
        list(map(lambda x: x.intercept(response), self.interceptors))
        return response.make_raw()

    def make_established_response(self, dialog_id):
        """ byte string 'HTTP/1.1 200 Connection established' """
        req = self.get_last_message(dialog_id)
        return b'%s %d %s\r\n\r\n' % (
            req.http_version.encode(), 200, b'Connection established')
