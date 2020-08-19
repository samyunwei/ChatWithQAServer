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
                return False, sqlite3.Error("not FOUND")
            else:
                self.name = row[0][1]
                self.age = row[0][2]
                cursor.close()
                return True, None
        except sqlite3.Error as e:
            print(e)
            return False, e

    def update(self) -> (bool, sqlite3.Error):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE user set name = '%s' and age = %d where id = '%s' " % (self.name, self.age, self.id))
            self.conn.commit()
            return True, None
        except sqlite3.Error as e:
            print(e)
            return False, e

    def insert(self) -> (bool, sqlite3.Error):
        try:
            cursor = self.conn.cursor()
            cursor.execute("insert into user(id,name,age) values('%s','%s',%d)" % (self.id, self.name, self.age))
            self.conn.commit()
            return True, None
        except sqlite3.Error as e:
            print(e)
            return False, e

    def delete(self) -> (bool, sqlite3.Error):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE from user where  id = '%s'" % self.id)
            self.conn.commit()
            return True, None
        except sqlite3.Error as e:
            print(e)
            return False, e


def loadUsers(conn):
    users = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id,name,age FROM user")
        row = cursor.fetchall()
        for eachrow in row:
            user = User(conn)
            user.id = eachrow[0]
            user.name = eachrow[1]
            user.age = eachrow[2]
            users.append(user)
        return users, None
    except sqlite3.Error as e:
        print(e)
        return users, e
