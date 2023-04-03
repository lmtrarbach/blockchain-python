from concurrent import futures
import grpc
import blockchain_sync_pb2_grpc
import servicediscovery_pb2_grpc
import servicediscovery_pb2
import discovery
import communication
import logging
import socket
import argparse
import time


class RunNode:
    def __init__(self, grpc_port, seed_node):
        self.grpc_port = grpc_port
        self.seed_node = seed_node
        self.get_ip_address()
        self.start_grpc()

    def get_ip_address(self):
        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_connection.connect(('8.8.8.8', 80))
        ip_address = socket_connection.getsockname()[0]
        socket_connection.close()
        self.node_ip = ip_address

    def start_grpc(self):
        node = self.node_ip
        discovery_service = discovery.DiscoveryService(node)
        if self.seed_node is None:
            discovery_service.peers.add(node)
        else:
            with grpc.insecure_channel(self.seed_node) as channel:
                discovery_stub = servicediscovery_pb2_grpc.DiscoveryStub(channel)
                response = discovery_service.RegisterNode(servicediscovery_pb2.Peer(address=node), None)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        servicediscovery_pb2_grpc.add_DiscoveryServicer_to_server(discovery_service, server)
        bind_node = '[::]:{}'.format(self.grpc_port)
        server.add_insecure_port(bind_node)
        server.start()
        if self.seed_node is not None:
            with grpc.insecure_channel(self.seed_node) as channel:
                discovery_stub = servicediscovery_pb2_grpc.DiscoveryStub(channel)
                response = discovery_service.FindPeers(servicediscovery_pb2.Peer(), None)
                print(response)
        logging.info(f"Peers: {discovery_service.GetPeers()}")
        # Wait until the discovery service is ready
        while discovery_service.ready != True:
            time.sleep(1)
        blockchain_sync_pb2_grpc.add_BlockchainSyncServiceServicer_to_server(communication.BlockchainSyncServiceServicer(discovery_service.GetPeers()), server)
        server.wait_for_termination()

def node_cli():
        parser = argparse.ArgumentParser()
        parser.add_argument('--port', type=int, default=50051, help='Port number to listen on')
        parser.add_argument('--seed-node', type=str, default=None, help='The seed node')
        args = parser.parse_args()
        return args

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    arguments = node_cli()
    logging.info('Starting node on port %s with %s as seed node',
                 arguments.port,
                 arguments.seed_node
                 )
    start = RunNode(
        arguments.port, 
        arguments.seed_node
        )
    