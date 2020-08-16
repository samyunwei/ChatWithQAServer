import sqlite3


class DbConnector(object):
    def __init__(self):
        self.conn = sqlite3.connect("chat.db")

    def executeSql(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()

    def test(self):
        self.executeSql('create table user(id varchar(20) primary key,name varchar(20))')
        # 插入一条记录：
        self.executeSql('insert into user (id, name) values (\'1\', \'Michael\')')

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    db = DbConnector()
    db.test()
