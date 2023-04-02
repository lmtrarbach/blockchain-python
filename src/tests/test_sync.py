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

class TestGrpcSync(unittest.TestCase):
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
        
        