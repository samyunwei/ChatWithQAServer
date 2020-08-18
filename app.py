import json

from flask import Flask
from flask import request

import SimpleChatProcessor
from ChatController import ChatController
from atten_model import AttentionChat

# processor = SimpleChatProcessor.SimpleChatProcessor()
processor = AttentionChat()
controller = ChatController()

processor = SimpleChatProcessor.SimpleChatProcessor()
app = Flask(__name__)


@app.route('/chat')
def chat():
    msg = request.args["msg"]
    if msg is None:
        return makeReq(None, "No have args")
    id = "anonymous"
    if request.args.__contains__("id"):
        id = request.args["id"]
    seq = controller.addUserSeq(id)
    controller.logMessage(id, seq, 1, msg)
    rep = controller.getAsk(request.data)
    if rep is None:
        rep = processor.process(msg)
    seq = controller.addUserSeq(id)
    controller.logMessage(id, seq, 2, rep)
    return makeReq(rep, seq, None)


def makeReq(msg, seq, errorMsg):
    res = dict()
    if errorMsg is not None:
        res["errorMsg"] = errorMsg
    else:
        res["reply"] = msg
    res["seq"] = seq
    return json.dumps(res)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=9997
    )
