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
"""
""""
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

"""

class TestWalletCreation(unittest.TestCase):
    def test_block_grpc(self):
        new_blocks = []
        channel = grpc.insecure_channel('localhost:50051')
        stub = blockchain_sync_pb2_grpc.BlockchainSyncServiceStub(channel)
        txn1 = blockchain_sync_pb2.Transaction(sender='Alice', recipient='Bob', amount=10)
        txn2 = blockchain_sync_pb2.Transaction(sender='Bob', recipient='Charlie', amount=5)
        request = blockchain_sync_pb2.SyncRequest()
        block = blockchain_sync_pb2.Block(transactions=[txn1, txn2])
        transaction = block.transactions.add()
        block.timestamp = str(time.time())
        block.previous_hash = block.hash
        print(time.time())
        request.blocks.append(block)
        response = stub.SyncBlockchain(request)
        logging.info('%s', str(response))
        print(request.blocks)
        
        