import unittest
import blockchain_sync_pb2
import servicediscovery_pb2_grpc
import servicediscovery_pb2
#from wallet import wallet, transaction
import grpc
import json
import logging
import pytest
import time
import os
logging.basicConfig(level=logging.DEBUG)

class TestNodeServiceDicsovery(unittest.TestCase):
    def test_service_discovery(self):
        with grpc.insecure_channel('172.17.0.2:50051') as channel:
            discovery_stub = servicediscovery_pb2_grpc.DiscoveryStub(channel)
        