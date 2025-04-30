from http.server import HTTPServer
from api_handler import APIHandler

def run_server(host='localhost', port=8000):
    """Запускает HTTP-сервер."""
    server_address = (host, port)
    server = HTTPServer(server_address, APIHandler)
    server.timeout = 60

    print(f"Server running on http://{host}:{port}")
    server.serve_forever()

if __name__ == '__main__':
    run_server(port=8000)