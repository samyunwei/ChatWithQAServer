from server_rpc.pb import SimpleChatbot_pb2_grpc
from server_rpc.pb.SimpleChatbot_pb2 import ChatReply
from ChatController import ChatController

controller = ChatController()


class SimpleChatBotServicerImp(SimpleChatbot_pb2_grpc.SimpleChatBotServerServicer):
    def __init__(self, processor):
        self.processor = processor

    def Chat(self, request, context):
        print("Seq2SeqChatBot:New Req  ids %s" % request.ids)
        id = request.ids
        seq = controller.addUserSeq(id)
        chat_type = 0
        controller.logMessage(id, seq, 1, request.data)
        rep = ChatReply()
        rep.ids = request.ids
        rep.data = controller.getAsk(request.data)
        if rep.data is None:
            rep.data, chat_type = self.processor.process(request.data, chat_type)
        seq = controller.addUserSeq(id)
        controller.logMessage(id, seq, 2, rep.data)
        return rep
