import unittest
import block_creator
import pytest
import time
import os

class TestBlockCreator(unittest.TestCase):
    def test_block_creation(self):
        self.directory = "tempdir"
        self.chain = block_creator.Blockchain(blockchain_dir=self.directory)
        self.chain.create_genesis_block()
        self.chain.add_block('{"sender": "Alice", "recipient": "Bob", "amount": 5}')
        self.chain.add_block('{"sender": "Bob", "recipient": "Alice", "amount": 5}')
        self.assertRaise(FileNotFoundError)