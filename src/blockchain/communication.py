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
    def __init__(self, peers):
        self.blockchain = block_creator.Blockchain(
            blockchain_dir="/data/blockchain", 
            peers = peers
            )
        
    def AddBlock(self, blocks):
        """
        Uses the block_creator module to add a new block
        Input:
            blocks List
        Return:
            GRPC response
        """
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
        """
        Get the blocks from the chain and returns in GRPC
        Input:
            request GRPC object
            context GRPC object
        Return:
            blocks GRPC
        """
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

    def SyncBlockchain(self, request):
        """
        Sync the blockchain called in the GRPC
        Input:
            request GRPC object
        Return:
            Empity GRPC
        """
        logging.info("Sync Service invoked")
        for block in request.blocks:
            transactions = []
            for txn in block.transactions:
                transactions.append(
                    {
                    "sender": txn.sender,
                    "recipient": txn.recipient,
                    "amount": txn.amount,
                    }
                )
            self.blockchain.add_block(transactions)   
        return empty_pb2.Empty()

    def GetPeerBlocks(self, request):
        """
        Get peers blocks from GRPC
        Input:
            request GRPC object
        Return:
            Blocks List
        """
        blocks = []
        for block in self.blockchain.chain:
            logging.info(str(block.hash))
            pb_block = blockchain_sync_pb2.Block(
                timestamp=str(block.timestamp),
                previous_hash=str(block.previous_hash),
                nonce=int(block.nonce),
                hash=str(block.hash),
                transactions=block.transactions
            )
            if block.transactions is not None:
                for txn in block.transactions:
                    pb_txn = blockchain_sync_pb2.Transaction(
                        sender=txn["sender"],
                        recipient=txn["recipient"],
                        amount=txn["amount"]
                    )
                    pb_block.transactions.append(pb_txn)
            blocks.append(pb_block)
        return blockchain_sync_pb2.SyncResponse(blocks=blocks)

    def BroadcastMessage(self, request, context):
        for peer in self.blockchain.peers:
            with grpc.insecure_channel(peer) as channel:
                stub = blockchain_sync_pb2.BlockchainStub(channel)
                stub.ReceiveMessage(request)
        return empty_pb2.Empty()
    
    def ReceiveMessage(self, request, context):
        print(request.message)
        return empty_pb2.Empty()
    