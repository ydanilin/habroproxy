""" main proxy server application """
import socket
import select
import threading
import requests
from OpenSSL import SSL
from .lib.logger import configure


LOG = configure('dialog')


class Server:
    """
    server class.
    address: address to bind, tuple (host, port). host typically is ''
    """
    def __init__(self, address, dialog_service, tls_service):
        self.address = address
        self.dialog_service = dialog_service
        self.tls_service = tls_service
        self.socket = None
        self.poll_interval = 0.1

    def start(self):
        """ binds and listens """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.bind(self.address)
        self.socket.listen()
        print(f"Habroproxy server is listening to '{self.address[0]}': {self.address[1]}")

    def serve_forever(self, poll_interval=0.1):
        """ endless loop with select """
        try:
            while True:
                read_sock, _, _ = select.select([self.socket], [], [], poll_interval)
                if self.socket in read_sock:
                    client_socket, client_address = self.socket.accept()
                    thread = threading.Thread(
                        target=self.handle_connection, args=(client_socket, client_address)
                    )
                    thread.start()
        except KeyboardInterrupt:
            if self.socket:
                self.socket.close()

    def handle_connection(self, client_socket, client_address):
        """ performs main workflow. callback to be executed by thread """
        # print(f'connection from {client_address}')
        raw_message = read(client_socket)
        if not raw_message:
            # LOG.error(f'Empty request from {client_address[1]}, socket closed\n\n')
            client_socket.close()
            return
        dialog_id = self.dialog_service.create_dialog(client_address, raw_message)
        request = self.dialog_service.get_last_message(dialog_id)
        if request.form == 'authority':
            try:
                target_socket, final_request = self.handle_secure_connection(
                    client_socket, request, dialog_id
                )
            except SSL.Error as err:
                LOG.error(f"SSL handshake error for {client_address[1]}: {repr(err)}")
                return
        else:
            target_socket = client_socket
            final_request = request
        # send request object to remote and receive into response object
        method, url, kwargs = self.dialog_service.prepare_py_request_args(final_request)
        kwargs['allow_redirects'] = False
        response = requests.request(method, url, **kwargs)
        # send response object to client
        raw_to_client = self.dialog_service.make_raw_from_py(response, dialog_id)
        # print(raw_to_client[:300])
        try:
            target_socket.sendall(raw_to_client)
        except SSL.Error as err:
            LOG.error(f"SSL write to client socket error for {client_address[1]}: {repr(err)}")
        # LOG.debug(f'closed connection for {dialog.clientPort}')
        target_socket.close()

    def handle_secure_connection(self, client_socket, request, dialog_id):
        """ performs all TLS stuff with client
            returns (wrapped secure_socket socket, client request after CONNECT)
        """
        client_socket.sendall(self.dialog_service.make_established_response(dialog_id))
        context = self.tls_service.create_ssl_context(request.host)
        secure_socket = SSL.Connection(context, client_socket)
        secure_socket.set_accept_state()
        try:
            secure_socket.do_handshake()
        except SSL.Error as err:
            secure_socket.close()
            raise SSL.Error(err)
            # return secure_socket, None
        # read application data request after handshake
        post_handshake_raw = read(secure_socket)
        final_request = self.dialog_service.make_request_from_raw(post_handshake_raw, dialog_id)
        return secure_socket, final_request

def read(sock):
    """
        traditional read from a socket
        maybe need this:
        https://stackoverflow.com/questions/23056805/how-to-continuously-read-data-from-socket-in-python
    """
    raw_message = b''
    while True:
        try:
            chunk = sock.recv(4096)
        except socket.error as err:
            print('Socket error: ', str(err))
            break
        if not chunk:
            break
        raw_message += chunk
        if len(chunk) < 4096:  # dirty, refactor
            break
    return raw_message
