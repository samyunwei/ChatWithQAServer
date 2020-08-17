import sqlite3


class User:

    def __init__(self, conn: sqlite3.Connection):
        """
        :param conn:
        """
        self.conn = conn
        self.id = None
        self.name = None
        self.age = None

    def select(self) -> (bool, sqlite3.Error):
        try:

            cursor = self.conn.cursor()
            cursor.execute("SELECT id,name,age FROM user where id = '%s'" % self.id)
            row = cursor.fetchall()
            if len(row) == 0:
                cursor.close()
                return False
            else:
                self.name = row[0]["name"]
                self.age = row[0]["age"]
                self.name = row[0]["name"]
                cursor.close()
                return True
        except sqlite3.Error as e:
            print(e)
            return False, e


    def update(self) -> (bool, sqlite3.Error):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE user set name = '%s' and age = %d where id = '%s' " % (self.name, self.age, self.id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False, e

    def insert(self) -> (bool, sqlite3.Error):
        try:
            cursor = self.conn.cursor()
            cursor.execute("insert into user(id,name,age) values('%s','%s',%d)" % (self.id, self.name, self.age))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False, e

    def delete(self) -> (bool, sqlite3.Error):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE from user where  id = '%s'" % self.id)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False, e
