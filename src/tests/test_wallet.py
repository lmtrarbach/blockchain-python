import unittest
import blockchain_sync_pb2
import blockchain_sync_pb2_grpc
import block_creator
#from wallet import wallet, transaction
import grpc
import json
import logging
import pytest
import time
import os
logging.basicConfig(level=logging.DEBUG)

class TestWalletCreation(unittest.TestCase):
    def test_block_creation(self):
        self.directory = "tempdir"
        self.chain = block_creator.Blockchain(blockchain_dir=self.directory)
        self.chain.create_genesis_block()
        alice_wallet = wallet.Wallet(wallet_dir='alicdir')
        alice = alice_wallet.get_address()
        bob_wallet = wallet.Wallet(wallet_dir='bobdir')
        bob = bob_wallet.get_address()
        with open(alice_wallet.get_private_key_file(), 'r') as sender_key:
            message = transaction.Transaction(
                                    sender_address=alice, 
                                    sender_private_key=sender_key.read(),
                                    recipient_address=bob,
                                    amount=10
                                    )
            message.sign_transaction()
            print(json.dumps(message.to_dict()))
            self.chain.add_block([message.to_dict()])
        
        