from concurrent import futures
import grpc
import logging
import blockchain_sync_pb2_grpc
import blockchain_sync_pb2
import block_creator
import google.protobuf.empty_pb2 as empty_pb2
import time

logging.basicConfig(level=logging.DEBUG)
Empty = empty_pb2.Empty()

class BlockchainSyncServiceServicer(blockchain_sync_pb2_grpc.BlockchainSyncService):
    def __init__(self):
        self.blockchain = block_creator.Blockchain(blockchain_dir="/data/blockchain")

    def AddBlock(self, blocks):
        transactions = []
        for txn in blocks:
            transactions.append({
                "sender": txn.sender,
                "recipient": txn.recipient,
                "amount": txn.amount,
            })
        self.blockchain.add_block(transactions)
        return blockchain_sync_pb2.SyncResponse()
    
    def GetBlocks(self, request, context):
        blocks = []
        for block in self.blockchain.chain:
            pb_block = blockchain_sync_pb2.Block(
                timestamp=block.timestamp,
                previous_hash=block.previous_hash,
                nonce=block.nonce,
                hash=block.hash
            )
            for txn in block.transactions:
                pb_txn = blockchain_sync_pb2.Transaction(
                    sender=txn["sender"],
                    recipient=txn["recipient"],
                    amount=txn["amount"]
                )
                pb_block.transactions.append(pb_txn)
            blocks.append(pb_block)
        return blockchain_sync_pb2.GetBlocksResponse(blocks=blocks)

    def SyncBlockchain(self, request, context):
        for block in request.blocks:
            transactions = []
            for txn in block.transactions:
                transactions.append({
                    "sender": txn.sender,
                    "recipient": txn.recipient,
                    "amount": txn.amount,
                })
        self.blockchain.add_block(transactions)   
        return empty_pb2.Empty()

    def GetPeerBlocks(self, request, context):
        blocks = []
        for block in self.blockchain.chain:
            pb_block = blockchain_sync_pb2.Block(
                timestamp=block.timestamp,
                previous_hash=block.previous_hash,
                nonce=block.nonce,
                hash=block.hash
            )
            for txn in block.transactions:
                pb_txn = blockchain_sync_pb2.Transaction(
                    sender=txn["sender"],
                    recipient=txn["recipient"],
                    amount=txn["amount"]
                )
                pb_block.transactions.append(pb_txn)
            blocks.append(pb_block)
        return blockchain_sync_pb2.GetBlocksResponse(blocks=blocks)

    def BroadcastMessage(self, request, context):
        for peer in self.blockchain.peers:
            with grpc.insecure_channel(peer) as channel:
                stub = blockchain_sync_pb2.BlockchainStub(channel)
                stub.ReceiveMessage(request)
        return empty_pb2.Empty()
    
    def ReceiveMessage(self, request, context):
        print(request.message)
        return empty_pb2.Empty()


def start_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    blockchain_sync_pb2_grpc.add_BlockchainSyncServiceServicer_to_server(BlockchainSyncServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_grpc()
