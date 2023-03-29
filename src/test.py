import unittest
import block_creator
import pytest
import time

class TestBlockCreator:
    def setup_method(self):
        self.chain = block_creator.Blockchain("/tmp")
        self.chain.create_genesis_block('{"sender": "Alice", "recipient": "Bob", "amount": 5}')
    def test_block_creation(self):
        self.chain.add_block('{"sender": "Alice", "recipient": "Bob", "amount": 5}')
        for each in self.chain.chain:
            print(each.hash)