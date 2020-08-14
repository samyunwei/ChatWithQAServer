# -*- coding: utf-8 -*-
# @Time    : 2020/8/14 15:43
# @Author  : piguanghua
# @FileName: atten_model.py
# @Software: PyCharm

from collections import Counter
import numpy as np
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import jieba
import os
import pickle as pkl


path = "/Users/piguanghua/Downloads/ChatWithQAServer-master/"
data_pkl = path + "pkl/data.pkl"

def save_vocab(en_dict, en_total_words):
    if os.path.isfile(data_pkl):
        dataset = pkl.load(open(data_pkl, "rb"))
        en_dict = dataset['en_dict']
        en_total_words = dataset['en_total_words']

    else:
        dataset = {}
        dataset["en_dict"] = en_dict
        dataset["en_total_words"] = en_total_words
        pkl.dump(dataset, open(data_pkl, "wb"))

    return en_dict, en_total_words

if os.path.isfile(data_pkl):
    en_dict,en_total_words = save_vocab(None,None)
    cn_dict, cn_total_words = en_dict,en_total_words

else:
    pass


inv_en_dict = {v: k for k, v in en_dict.items()}
inv_cn_dict = {v: k for k, v in cn_dict.items()}


dropout = 0.15
embed_size = hidden_size = 300
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_size, enc_hidden_size, dec_hidden_size, dropout=0.2):
        super(Encoder, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.GRU(embed_size, enc_hidden_size, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(enc_hidden_size * 2, dec_hidden_size)

    def forward(self, x, lengths):
        sorted_len, sorted_idx = lengths.sort(0, descending=True)
        x_sorted = x[sorted_idx.long()]
        embedded = self.dropout(self.embed(x_sorted))

        packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded, sorted_len.long().cpu().data.numpy(),
                                                            batch_first=True)
        packed_out, hid = self.rnn(packed_embedded)
        out, _ = nn.utils.rnn.pad_packed_sequence(packed_out, batch_first=True)
        _, original_idx = sorted_idx.sort(0, descending=False)
        out = out[original_idx.long()].contiguous()
        hid = hid[:, original_idx.long()].contiguous()

        hid = torch.cat([hid[-2], hid[-1]], dim=1)
        hid = torch.tanh(self.fc(hid)).unsqueeze(0)

        return out, hid


class Attention(nn.Module):
    def __init__(self, enc_hidden_size, dec_hidden_size):
        super(Attention, self).__init__()

        self.enc_hidden_size = enc_hidden_size
        self.dec_hidden_size = dec_hidden_size

        self.linear_in = nn.Linear(enc_hidden_size * 2, dec_hidden_size, bias=False)
        self.linear_out = nn.Linear(enc_hidden_size * 2 + dec_hidden_size, dec_hidden_size)

    def forward(self, output, context, mask):
        # output: batch_size, output_len, dec_hidden_size
        # context: batch_size, context_len, 2*enc_hidden_size

        batch_size = output.size(0)
        output_len = output.size(1)
        input_len = context.size(1)

        context_in = self.linear_in(context.view(batch_size * input_len, -1)).view(
            batch_size, input_len, -1)  # batch_size, context_len, dec_hidden_size

        # context_in.transpose(1,2): batch_size, dec_hidden_size, context_len
        # output: batch_size, output_len, dec_hidden_size
        attn = torch.bmm(output, context_in.transpose(1, 2))
        # batch_size, output_len, context_len

        attn.data.masked_fill(mask, -1e6)

        attn = F.softmax(attn, dim=2)
        # batch_size, output_len, context_len

        context = torch.bmm(attn, context)
        # batch_size, output_len, enc_hidden_size

        output = torch.cat((context, output), dim=2)  # batch_size, output_len, hidden_size*2

        output = output.view(batch_size * output_len, -1)
        output = torch.tanh(self.linear_out(output))
        output = output.view(batch_size, output_len, -1)
        return output, attn


class Decoder(nn.Module):
    def __init__(self, vocab_size, embed_size, enc_hidden_size, dec_hidden_size, dropout=0.2):
        super(Decoder, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.attention = Attention(enc_hidden_size, dec_hidden_size)
        self.rnn = nn.GRU(embed_size, hidden_size, batch_first=True)
        self.out = nn.Linear(dec_hidden_size, vocab_size)
        self.dropout = nn.Dropout(dropout)

    def create_mask(self, x_len, y_len):
        # a mask of shape x_len * y_len
        device = x_len.device
        max_x_len = x_len.max()
        max_y_len = y_len.max()
        x_mask = torch.arange(max_x_len, device=x_len.device)[None, :] < x_len[:, None]
        y_mask = torch.arange(max_y_len, device=x_len.device)[None, :] < y_len[:, None]
        #mask = (1 - x_mask[:, :, None] * y_mask[:, None, :]).byte()
        mask = (~ x_mask[:, :, None] * y_mask[:, None, :]).byte()

        return mask

    def forward(self, ctx, ctx_lengths, y, y_lengths, hid):
        sorted_len, sorted_idx = y_lengths.sort(0, descending=True)
        y_sorted = y[sorted_idx.long()]
        hid = hid[:, sorted_idx.long()]

        y_sorted = self.dropout(self.embed(y_sorted))  # batch_size, output_length, embed_size

        packed_seq = nn.utils.rnn.pack_padded_sequence(y_sorted, sorted_len.long().cpu().data.numpy(), batch_first=True)
        out, hid = self.rnn(packed_seq, hid)
        unpacked, _ = nn.utils.rnn.pad_packed_sequence(out, batch_first=True)
        _, original_idx = sorted_idx.sort(0, descending=False)
        output_seq = unpacked[original_idx.long()].contiguous()
        hid = hid[:, original_idx.long()].contiguous()

        mask = self.create_mask(y_lengths, ctx_lengths)

        output, attn = self.attention(output_seq, ctx, mask)
        output = F.log_softmax(self.out(output), -1)

        return output, hid, attn

class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super(Seq2Seq, self).__init__()
        self.encoder = encoder
        self.decoder = decoder

    def forward(self, x, x_lengths, y, y_lengths):
        encoder_out, hid = self.encoder(x, x_lengths)
        output, hid, attn = self.decoder(ctx=encoder_out,
                                         ctx_lengths=x_lengths,
                                         y=y,
                                         y_lengths=y_lengths,
                                         hid=hid)
        return output, attn

    def translate(self, x, x_lengths, y, max_length=100):
        encoder_out, hid = self.encoder(x, x_lengths)
        preds = []
        batch_size = x.shape[0]
        attns = []
        for i in range(max_length):
            output, hid, attn = self.decoder(ctx=encoder_out,
                                             ctx_lengths=x_lengths,
                                             y=y,
                                             y_lengths=torch.ones(batch_size).long().to(y.device),
                                             hid=hid)
            y = output.max(2)[1].view(batch_size, 1)
            preds.append(y)
            attns.append(attn)
        return torch.cat(preds, 1), torch.cat(attns, 1)

def convert_string_bos(string):
    line = string.strip().split("\t")
    en = []
    data = list(jieba.cut(string, HMM=False))

    en.append(["BOS"] + data + ["EOS"])
    return en

def encode(en_sentences, en_dict, sort_by_len=True):
    '''
        Encode the sequences.
    '''
    length = len(en_sentences)
    out_en_sentences = [[en_dict.get(w, 0) for w in sent] for sent in en_sentences]

    # sort sentences by english lengths
    def len_argsort(seq):
        return sorted(range(len(seq)), key=lambda x: len(seq[x]))

    # 把中文和英文按照同样的顺序排序
    if sort_by_len:
        sorted_index = len_argsort(out_en_sentences)
        out_en_sentences = [out_en_sentences[i] for i in sorted_index]

    return out_en_sentences


class AttentionChat():

    def __init__(self):
        """
        初始化模型
        :return:
        """
        encoder = Encoder(vocab_size=en_total_words,
                          embed_size=embed_size,
                          enc_hidden_size=hidden_size,
                          dec_hidden_size=hidden_size,
                          dropout=dropout)
        decoder = Decoder(vocab_size=cn_total_words,
                          embed_size=embed_size,
                          enc_hidden_size=hidden_size,
                          dec_hidden_size=hidden_size,
                          dropout=dropout)

        model = Seq2Seq(encoder, decoder)
        model = model.to(device)
        save_path = path + "save_model/atten.model"
        checkpoint = torch.load(save_path, map_location=torch.device('cpu'))
        model.load_state_dict(checkpoint["model_state_dict"], strict=False)

        self.model = model

    def process(self, msg):
        """
        model process msg
        如果调用QA置信度大于阈值则采用QA否则则采用Seq2Seq的回答
        :param msg:
        :return:
        """
        """
            根据模型得到（回答和置信度）
            :param input:
            :return:
            """
        #model = initModel()
        model = self.model
        string = msg
        dev_en = convert_string_bos(string)

        dev_en = encode(dev_en, en_dict)

        mb_x = torch.from_numpy(np.array(dev_en[0]).reshape(1, -1)).long().to(device)
        mb_x_len = torch.from_numpy(np.array([len(dev_en[0])])).long().to(device)
        bos = torch.Tensor([[cn_dict["BOS"]]]).long().to(device)

        translation, attn = model.translate(mb_x, mb_x_len, bos)
        translation = [inv_cn_dict[i] for i in translation.data.cpu().numpy().reshape(-1)]
        trans = []
        for word in translation:
            if word != "EOS":
                trans.append(word)
            else:
                break
        return trans




