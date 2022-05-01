# import os, sys
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'node'))


from unittest import TestCase
from module.cryptoprovider import CryptoProvider


class TestCryptoProvider(TestCase):
    def test_generate_wallet(self):
        provider = CryptoProvider()
        wallet_credentials = provider.generate_wallet()
        self.assertIn("wallet-id", wallet_credentials.keys())
        self.assertIn("secret-key", wallet_credentials.keys())

    def test_wallet_id_checksums(self):
        provider = CryptoProvider()
        wallet_credentials = provider.generate_wallet()
        wallet_id = wallet_credentials["wallet-id"]

