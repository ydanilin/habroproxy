from proxy import Server

if __name__ == '__main__':
    server = Server(('', 8080), None, None)
    server.start()
    server.serveForever()
