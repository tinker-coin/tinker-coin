import base64
import zlib
from nacl.public import PrivateKey

from constants.tinkerconstants import TINKER_WALLET_VERSION
from interface.icryptoprovider import ICryptoProvider


class CryptoProvider(ICryptoProvider):

    def generate_wallet(self, passcode: str):
        key_pair = PrivateKey.generate()

        public_key_bytes = int(TINKER_WALLET_VERSION).to_bytes(1, 'little') + key_pair.public_key.encode()

        checksum = zlib.crc32(public_key_bytes)
        enriched_public_key_bytes = checksum.to_bytes(4, 'little') + public_key_bytes

        public_key = base64.urlsafe_b64encode(enriched_public_key_bytes).decode("utf-8").rstrip("=")
        private_key = base64.urlsafe_b64encode(key_pair.encode()).decode("utf-8").rstrip("=")
        return {
            "wallet-id": public_key,
            "secret-key": private_key
        }

