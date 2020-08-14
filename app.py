from flask import Flask
from flask import request
import json
import config
import SimpleChatProcessor
from atten_model import AttentionChat
import socket
#processor = SimpleChatProcessor.SimpleChatProcessor()
processor = AttentionChat()

import socket
processor = SimpleChatProcessor.SimpleChatProcessor()
app = Flask(__name__)


@app.route('/chat')
def chat():
    msg = request.args["msg"]
    if msg is None:
        return makeReq(None, "No have args")
    rep = processor.process(msg)
    return makeReq(rep, None)


def makeReq(msg, errorMsg):
    res = dict()
    if errorMsg is not None:
        res["errorMsg"] = errorMsg
    else:
        res["reply"] = msg
    return json.dumps(res)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=9997
    )
