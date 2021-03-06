import logging
from concurrent import futures
import grpc

import SimpleChatProcessor
import server_rpc.SimpleChatBotServerImp
import server_rpc.pb.SimpleChatbot_pb2
import server_rpc.pb.SimpleChatbot_pb2_grpc

ADDR = "[::]:50052"

def serve():
    s = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    processor = SimpleChatProcessor.SimpleChatProcessor()
    imp = server_rpc.SimpleChatBotServerImp.SimpleChatBotServicerImp(processor)
    server_rpc.pb.SimpleChatbot_pb2_grpc.add_SimpleChatBotServerServicer_to_server(imp, s)
    s.add_insecure_port(ADDR)
    s.start()
    print("SimpleChatBot Begin to Serve at:%s" % ADDR)
    s.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
