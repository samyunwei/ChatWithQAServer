import sqlite3


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
                ret[each[0]] = each[1]
            return ret

        except sqlite3.Error as e:
            print(e)
            return ret, e
        finally:
            cursor.close()

    def insert(self, key, value) -> (bool, sqlite3.Error):
        cursor = self.conn.cursor()
        sql = "insert into dict(key, value) values ('%s','%s')" % (key, value)
        try:
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            print(e)
            return False, e
