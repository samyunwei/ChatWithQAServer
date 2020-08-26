import os

import jieba
import pickle
import numpy as np

nonghang_model_pkl = "pkl/nonghang_model.pkl"
nonghang_question = "pkl/nonghang.pkl"
stopword_path = "pkl/stopwords.txt"


class NongChatProcessor(object):
    def __init__(self):
        """
        init model
        """
        nonghang_model = pickle.load(open(nonghang_model_pkl, "rb"))
        self.index = nonghang_model["index"]
        self.tfidf = nonghang_model["tfidf"]
        self.dictionary = nonghang_model["dictionary"]
        self.model = nonghang_model
        # 获取停用词
        self.stopwords = set()
        file = open(stopword_path, 'r', encoding='UTF-8')
        with  open(stopword_path, 'r', encoding='UTF-8') as fin:
            for line in fin:
                self.stopwords.add(line.strip())

        dataset = pickle.load(open(nonghang_question, "rb"))
        self.reply = dataset["reply"]

    def process(self, msg):
        """
        model process msg
        如果调用QA置信度大于阈值则采用QA否则则采用Seq2Seq的回答
        :param msg:
        :return:
        """
        words = ' '.join(jieba.cut(msg)).split(' ')
        new_text = []
        for word in words:
            if word not in self.stopwords:
                new_text.append(word)

        new_vec = self.dictionary.doc2bow(new_text)
        new_vec_tfidf = self.tfidf[new_vec]  # 将待比较文档转换为tfidf表示方法
        sims = self.index[new_vec_tfidf]
        data = np.array(sims)

        return self.reply.iloc[np.argmax(data)]

    def calcRate(self, msg):
        if str.find(msg,"农行") != -1:
            return True
        else:
            return False
