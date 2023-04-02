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

    def GetNodes(self, request, context):
        response = servicediscovery_pb2.NodesResponse()
        response.nodes.extend(self.nodes)
        return response

    def RegisterNode(self, request, context):
        self.nodes.append(request.ip_address)
        logging.info('Node with IP %s added',
                      request.ip_address
                    )
        return empty_pb2.Empty()