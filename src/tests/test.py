import unittest
from  blockchain import block_creator
from wallet import wallet
import pytest
import time
import os

"""
class TestBlockCreator(unittest.TestCase):
    def test_block_creation(self):
        self.directory = "tempdir"
        self.chain = block_creator.Blockchain(blockchain_dir=self.directory)
        self.chain.create_genesis_block()
        self.chain.add_block('{"sender": "Alice", "recipient": "Bob", "amount": 5}')
        self.chain.add_block('{"sender": "Bob", "recipient": "Alice", "amount": 5}')
        self.assertTrue(os.path.isdir(self.directory))
        self.assertTrue(os.path.isfile('{}/merkle_tree.json'.format(self.directory)))
"""

class TestWalletCreation(unittest.TestCase):
    def test_block_creation(self):
        self.directory = "tempdir"
        self.chain = block_creator.Blockchain(blockchain_dir=self.directory)
        self.chain.create_genesis_block()
        alice_wallet = wallet.Wallet(wallet_dir='alicdir')
        alice = alice_wallet.get_address()
        print(alice)
        bob_wallet = wallet.Wallet(wallet_dir='bobdir')
        bob = bob_wallet.get_address()
        transaction = '''{"sender": %s, "recipient": %s, "amount": 5}''' % (str(alice),str(bob))
        print(transaction)
        self.chain.add_block(transaction)