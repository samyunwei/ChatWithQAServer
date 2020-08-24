import os
from atten_model import AttentionChat
from ChatController import ChatController
from NongChatProcessor import NongChatProcessor


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
        chat_type += 1
        retlist = self.nongChat_model_processor.process(msg)
        if self.nongChat_model_processor.calcRate(msg) is False:
            chat_type += 1
            retlist = self.atteen_model.process(msg)

        ret = "".join(retlist)
        return ret, chat_type
