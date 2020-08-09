import os

class SimpleChatProcessor(object):
    def __init__(self):
        """
        init model
        """
        pass

    def process(self, msg):
        """
        model process msg
        如果调用QA置信度大于阈值则采用QA否则则采用Seq2Seq的回答
        :param msg:
        :return:
        """
        intent = "test"

        return intent
