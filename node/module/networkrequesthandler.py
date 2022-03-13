import json
from http.server import BaseHTTPRequestHandler


# noinspection PyPep8Naming
class NetworkRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps({"name": "NetworkRequestHandler"}).encode("utf-8"))
