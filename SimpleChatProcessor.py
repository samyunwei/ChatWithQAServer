import os
from atten_model import AttentionChat
from ChatController import ChatController

class SimpleChatProcessor(object):
    def __init__(self):
        """
        init model
        """
        self.model = AttentionChat()


    def process(self, msg):
        """
        model process msg
        如果调用QA置信度大于阈值则采用QA否则则采用Seq2Seq的回答
        :param msg:
        :return:
        """
        retlist = self.model.process(msg)
        ret = "".join(retlist)
        return ret
