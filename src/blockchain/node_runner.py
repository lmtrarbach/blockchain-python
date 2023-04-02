from concurrent import futures
import grpc
import blockchain_sync_pb2_grpc
import servicediscovery_pb2_grpc
import discovery
import communication
import logging
import socket
import argparse


class RunNode:
    def __init__(self, grpc_port):
        self.grpc_port = grpc_port
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
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        servicediscovery_pb2_grpc.add_DiscoveryServicer_to_server(discovery_service, server)
        blockchain_sync_pb2_grpc.add_BlockchainSyncServiceServicer_to_server(communication.BlockchainSyncServiceServicer(), server)
        bind_node = '[::]:{}'.format(self.grpc_port)
        server.add_insecure_port(bind_node)
        server.start()
        server.wait_for_termination()

def node_cli():
        parser = argparse.ArgumentParser()
        parser.add_argument('--port', type=int, default=50051, help='Port number to listen on')
        args = parser.parse_args()
        return args

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    arguments = node_cli()
    logging.info('Starting node on port %s',
                 arguments.port
                 )
    start = RunNode(arguments.port)
    