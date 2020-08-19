import sqlite3
from db.DB_ChatLog import ChatLog
from db.DB_User import User
from db.DB_ChatDict import ChatDict
from db.DB_User import loadUsers
import random
import threading


class ChatController:
    def __init__(self):
        self.conn = sqlite3.connect("chat.db", check_same_thread=False)
        self.chatLog = ChatLog(self.conn)
        self.users = loadUsers(self.conn)
        self.chatDict = ChatDict(self.conn)
        self.serialnum = random.randint(1, 1000000)
        self.dict = self.chatDict.select()
        self.user_count = {}
        self.lock = threading.Lock()

    def getAsk(self, quest):
        self.lock.acquire()
        ask = None
        if self.dict.__contains__(quest):
            ask = self.dict[quest]
        self.lock.release()
        return ask

    def logMessage(self, id, seq, role, msg):
        self.lock.acquire()
        ret = self.chatLog.insert(self.serialnum, id, seq, role, msg)
        self.lock.release()
        return ret

    def hasUser(self, id):
        for user in self.users:
            if user.id == id:
                return True
        return False

    def addUserSeq(self, id):
        self.lock.acquire()
        if self.user_count.__contains__(id):
            self.user_count[id] = self.user_count[id] + 1
        else:
            self.user_count[id] = 0
        self.lock.release()
        return self.user_count[id]

    def ChatDictCtrl(self, method, key, value) -> (bool, sqlite3.Error):
        succ = False
        err = None
        self.lock.acquire()
        if method == "insert":
            succ, err = self.chatDict.insert(key, value)
        elif method == "update":
            succ, err = self.chatDict.update(key, value)
        elif method == "delete":
            succ, err = self.chatDict.delete(key)
        else:
            succ, err = False, ValueError("UnSupport Method!")
        self.lock.release()
        return succ, err

    def reloadDict(self):
        self.lock.acquire()
        self.dict = self.chatDict.select()
        self.lock.release()
        return True, self.dict

    def close(self):
        self.conn.close()
