import json
from http.server import BaseHTTPRequestHandler


# noinspection PyPep8Naming
class UIRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"name": "UIRequestHandler"}).encode("utf-8"))
