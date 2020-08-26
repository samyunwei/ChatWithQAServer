import json

from flask import Flask, Response
from flask import request
from flask_cors import CORS

import SimpleChatProcessor
from ChatController import ChatController
from atten_model import AttentionChat

controller = ChatController()
processor = SimpleChatProcessor.SimpleChatProcessor()
app = Flask(__name__)

CORS(app)


@app.route('/chat')
def chat():
    chat_type = -1
    msg = request.args["msg"]
    if msg is None:
        return makeReq(None, "No have args")
    id = "anonymous"
    if request.args.__contains__("id"):
        id = request.args["id"]
    seq = controller.addUserSeq(id)
    controller.logMessage(id, seq, 1, msg, chat_type)
    chat_type = 0
    rep = controller.getAsk(msg)
    if rep is None:
        rep, chat_type = processor.process(msg, chat_type)
    seq = controller.addUserSeq(id)
    controller.logMessage(id, seq, 2, rep, chat_type)
    return makeReq(rep, seq, "")


@app.route("/dict/<method>")
def ChatDictCtrl(method):
    res = {}
    succ = False
    if method != "reload":
        key = request.args["key"]
        value = request.args["value"]
        succ, err = controller.ChatDictCtrl(method, key, value)
        if succ is False:
            res["errMsg"] = str(err)
    else:
        succ, dict = controller.reloadDict()
        res["dict"] = dict
    res["succ"] = succ
    return Response(json.dumps(res, ensure_ascii=False), mimetype='application/json;charset=utf-8')


def makeReq(msg, seq, errorMsg):
    res = dict()
    if len(errorMsg) is not 0:
        res["errorMsg"] = errorMsg
    else:
        res["reply"] = msg
    res["seq"] = seq
    rep = Response(json.dumps(res, ensure_ascii=False), mimetype='application/json;charset=utf-8')
    return rep


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(
        host='0.0.0.0',
        port=9997
    )
