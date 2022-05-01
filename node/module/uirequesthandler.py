import base64
import json
import logging
import os
import mimetypes
from http.server import BaseHTTPRequestHandler
from typing import Optional
from urllib.parse import urlparse
from pathlib import Path

from interface.iapp import IApp


logger = logging.getLogger(__name__)


class UIRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asset_root = None
        self.app: Optional[IApp] = None

    def do_GET(self):
        self.app = self.server.app
        self.asset_root = os.path.join(self.app.code_root, "ui-assets")
        url = urlparse(self.path)
        # clean and convert to os specific path.
        request_path = url.path.strip().rstrip("/").lower()
        asset_path = os.path.normpath(os.path.join(self.asset_root, *request_path.split("/")))
        if request_path == "" or request_path == "/":
            return self.do_asset(os.path.join(self.asset_root, "index.html"))
        elif request_path == "/api/generate-wallet-ack":
            return self.do_generate_wallet_ack()
        elif Path(asset_path).is_file():
            return self.do_asset(asset_path)
        return self.do_error(404, asset_path)

    def do_error(self, error: int, path: str):
        logger.debug("ERROR: %d: %s.", error, path)
        self.send_response(error)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(os.path.join(self.asset_root, str(error) + ".html"), "rb") as f:
            self.wfile.write(f.read())

    def do_asset(self, path: str):
        logger.debug("Serving static asset: %s.", path)
        # Prevent vending out files outside the asset_root folder.
        if not path.startswith(self.asset_root):
            return self.do_error(400, path)
        (type_str, encoding) = mimetypes.guess_type(path)
        self.send_response(200)
        self.send_header("Content-type", type_str)
        self.end_headers()
        with open(path, "rb") as f:
            self.wfile.write(f.read())

    def do_generate_wallet_ack(self):
        wallet_credentials = self.app.crypto_provider.generate_wallet()

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(wallet_credentials).encode("utf-8"))
