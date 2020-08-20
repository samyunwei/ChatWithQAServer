import sqlite3


class ChatLog:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def insert(self, serialnum, id, seq, role, meesage, chat_type) -> (bool, sqlite3.Error):
        cursor = self.conn.cursor()
        sql = "insert into chat(serialnum, id, seq, role, message,type) values (%d,'%s',%d,%d,'%s',%d)" % (
            serialnum, id, seq, role, meesage, chat_type)
        try:
            cursor.execute(sql)
            self.conn.commit()
            return True, None
        except sqlite3.Error as e:
            print(e)
            return False, e
        finally:
            cursor.close()
