from concurrent import futures
import grpc
import logging
import servicediscovery_pb2
import servicediscovery_pb2_grpc
import google.protobuf.empty_pb2 as empty_pb2
import time

logging.basicConfig(level=logging.DEBUG)
class DiscoveryService(servicediscovery_pb2_grpc.DiscoveryServicer):
    def __init__(self, nodes):
        self.nodes = nodes
        self.peers = set()
        self.ready = True

    def GetNodes(self, request, context):
        response = servicediscovery_pb2.NodesResponse()
        response.nodes.extend(self.nodes)
        return response

    def RegisterNode(self, request, context):
        logging.info(f"Current registered peers {self.peers}")
        self.peers.add(request.address)
        logging.info(f"Registered peer {request.address}")
        return servicediscovery_pb2.Peers(
            peers=[servicediscovery_pb2.Peer(address=peer) for peer in self.peers]
            )

    def FindPeers(self, request, context):
        logging.info(f"Current registered peers {self.peers}")
        return servicediscovery_pb2.Peers(
            peers=[servicediscovery_pb2.Peer(address=peer) for peer in self.peers]
            )

    def GetPeers(self):
        peers = [servicediscovery_pb2.Peer(address=peer) for peer in self.peers]
        return peers