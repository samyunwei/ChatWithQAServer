from ChatController import ChatController
import csv

if __name__ == '__main__':
    controller = ChatController()
    f = csv.reader(open("data/dict.csv", 'r', encoding='utf-8'))
    for row in f:
        print("insert dict key:%s value:%s" % (row[1], row[2]))
        controller.ChatDictCtrl("insert", row[1], row[2])
