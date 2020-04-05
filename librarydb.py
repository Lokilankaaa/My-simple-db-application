import pymysql
from books import Books
from cards import Cards


class LibraryDB():
    def __init__(self):
        self.db = pymysql.connect('lokilanka.cn', user="test2", passwd="password", db="lab5")
        self.cursor = self.db.cursor()
        self.books = Books(self.cursor, self.db)
        self.cards = Cards(self.cursor, self.db)

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def storeBooks(self, batch=False):
        bookInfo = {}
        tt = ['book_id', 'category', 'title', 'press', 'year', 'author', 'price', 'num']
        if not batch:
            for t in tt:
                if t != 'num':
                    bookInfo[t] = input('Please enter ' + t + ':')
                else:
                    bookInfo[t] = '1'
            self.books.store(bookInfo)
        else:
            path = input('Please enter file path：')
            with open(path) as f:
                for line in f.readlines():
                    oneLine = line.split(',')
                    bookInfo = zip(tt, oneLine)
                    self.books.store(bookInfo)

    def queryBooks(self):
        tt = ['category', 'title', 'press', 'year', 'author', 'price']
        queryInfo = {}
        for t in tt:
            print('Please enter the ' + t + ' of the book which you want to query.'
                  + 'If you don\'t know the detail, just pass it by enter')
            if t == 'year' or t == 'price':
                print('You should input in the following format:\n'
                      + 'xxx to xxx(where xxx is the number of ' + t + ' )')
            queryInfo[t] = input()
        results = self.books.query(queryInfo)
        if results:
            for one in results:
                print(
                    "book_id:{0} category:{1} title:{2} press:{3} year:{4} author:{5} price:{6} total:{7} stock:{8}".format(
                        one[0], one[1], one[2], one[3], one[4], one[5], one[6], one[7], one[8]))
        else:
            print("Sorry! No book you want here.")
        print("------------------------------------------------------------------------------------------------")
        print("                                                                                                ")
        print("                                                                                                ")

    def createCard(self):
        pass
