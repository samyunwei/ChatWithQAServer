import sqlite3
import zhon.hanzi
import re
import string
import chardet


class ChatDict:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def select(self) -> (dict, sqlite3.Error):
        ret = {}
        cursor = self.conn.cursor()
        sql = "select key,value from dict"
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for each in rows:
                key = cleanPunctuation(each[0])
                value = each[1]
                if ret.__contains__(each[0]):
                    ret[key].append(value)
                else:
                    ret[key] = [value]
            return ret

        except sqlite3.Error as e:
            print(e)
            return ret, e
        finally:
            cursor.close()

    def insert(self, key, value, chat_type) -> (bool, sqlite3.Error):
        cursor = self.conn.cursor()
        sql = "insert into dict(key, value,type) values ('%s','%s',%d)" % (key, value, chat_type)
        try:
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return True, None
        except sqlite3.Error as e:
            print(e)
            return False, e

    def update(self, key, value, chat_type) -> (bool, sqlite3.Error):
        cursor = self.conn.cursor()
        sql = "update dict set type = %d  where key = '%s' and value = '%s'" % (chat_type, key, value,)
        try:
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return True, None
        except sqlite3.Error as e:
            print(e)
            return False, e

    def delete(self, key, value) -> (bool, sqlite3.Error):
        cursor = self.conn.cursor()
        sql = "delete from dict where key = '%s' and value = '%s'" % (key, value)
        try:
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return True, None
        except sqlite3.Error as e:
            print(e)
            return False, e


def cleanPunctuation(text):
    text = re.sub(r'[{}]+'.format(string.punctuation), '', text)
    text = re.sub(r'[{}]+'.format(zhon.hanzi.punctuation), '', text)
    return text


def unicodeToUTF8(text):
    # text = text.encode("utf-8")
    return text
