import os
from atten_model import AttentionChat
from ChatController import ChatController
from NongChatProcessor import NongChatProcessor
import string


class SimpleChatProcessor(object):
    def __init__(self):
        """
        init model
        """
        self.atteen_model = AttentionChat()
        self.nongChat_model_processor = NongChatProcessor()

    def process(self, msg, chat_type):
        """
        model process msg
        如果调用QA置信度大于阈值则采用QA否则则采用Seq2Seq的回答
        :param msg:
        :return:
        """
        retlist = []
        if self.nongChat_model_processor.calcRate(msg) is True:
            chat_type = 1
            retlist = self.nongChat_model_processor.process(msg)
        else:
            chat_type = 2
            retlist = self.atteen_model.process(msg)
        ret = "".join(retlist)
        return ret, chat_type

    def process_NongHang(self, msg):
        retlist = self.nongChat_model_processor.process(msg)
        ret = "".join(retlist)
        return ret, 1

    def process_Attention(self, msg):
        retlist = self.atteen_model.process(msg)
        ret = "".join(retlist)
        return ret, 2
