import os
import json
import hashlib
from time import time
import logging
logging.basicConfig(level=logging.DEBUG)

class Block:
    def __init__(self, timestamp, transactions, previous_hash="", nonce=0):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce)
        logging.info("Hashing %s", hashlib.sha256(data.encode()).hexdigest())
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self, blockchain_dir, peers):
        self.blockchain_dir = blockchain_dir
        self.chain = []
        self.peers = peers
        chain_load = self.load_chain()
        if chain_load == True and self.peers == None:
            self.create_genesis_block()

    def create_genesis_block(self):
        logging.info("Creating Genesis block")
        transactions = [{"sender": "eu", "recipient": "rafa", "amount": 0}]
        genesis_block = Block(time(), transactions)
        genesis_block.previous_hash = "0" * 64
        self.chain.append(genesis_block)
        self.save_block(genesis_block)

    def load_chain(self):
        logging.info("Loading chain")
        if not os.path.exists(self.blockchain_dir):
            os.makedirs(self.blockchain_dir)
        for filename in os.listdir(self.blockchain_dir):
            if filename.endswith(".json") and filename != "merkle_tree.json":
                filepath = os.path.join(self.blockchain_dir, filename)
                with open(filepath, "r") as f:
                    block_dict = json.load(f)
                    block = Block(block_dict["timestamp"], block_dict["transactions"], block_dict["previous_hash"], block_dict["nonce"])
                    logging.info("Adding block to filesystem: %s", block)
                    self.chain.append(block)
        return True

    def save_block(self, block):
        logging.info("Saving blocks")
        filename = os.path.join(self.blockchain_dir, f"{block.hash}.json")
        with open(filename, "w") as f:
            block_dict = {"timestamp": block.timestamp, "transactions": block.transactions, "previous_hash": block.previous_hash, "nonce": block.nonce}
            json.dump(block_dict, f, indent=4)

        merkle_tree = [hashlib.sha256(json.dumps(block.transactions[i]).encode()).hexdigest() for i in range(len(block.transactions))]
        while len(merkle_tree) > 1:
            new_merkle_tree = []
            for i in range(0, len(merkle_tree), 2):
                if i == len(merkle_tree) - 1:
                    new_merkle_tree.append(merkle_tree[i])
                else:
                    new_merkle_tree.append(hashlib.sha256((merkle_tree[i] + merkle_tree[i+1]).encode()).hexdigest())
            merkle_tree = new_merkle_tree

        merkle_tree_filename = os.path.join(self.blockchain_dir, "merkle_tree.json")
        with open(merkle_tree_filename, "w") as f:
            json.dump({"root_hash": merkle_tree[0]}, f, indent=4)

    def add_block(self, transactions):
        logging.info("Adding new blocks")
        previous_block = self.chain[-1]
        new_block = Block(time(), transactions, previous_block.hash)
        self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.save_block(new_block)
        logging.info("New block saved")

    def proof_of_work(self, block, difficulty=2):
        logging.info("POW execution")
        while block.hash[:difficulty] != "0" * difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        logging.info("Hashing done")
