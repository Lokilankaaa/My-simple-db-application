import pymysql
from books import Books
from cards import Cards
from record import Record


class LibraryDB():
    def __init__(self, params):
        self.db = pymysql.connect(params['host'], user=params['user'], passwd=params['passwd'], db=params['db'])
        self.cursor = self.db.cursor()
        self.books = Books(self.cursor, self.db)
        self.cards = Cards(self.cursor, self.db)
        self.records = Record(self.cursor, self.db)

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
                    oneLine = [i.strip(' ') for i in line.strip('\n').split(',')]
                    bookInfo = dict(zip(tt, oneLine))
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
        print("------------------------------------------------------------------------------------------------")
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

    def borrowBook(self):
        card_id = input("Please enter your 7 digits borrowing card id(if you don't have one, type register): ")
        if card_id == 'register':
            card_id = self.cards.cardManage('1')
        if card_id:
            bid = input("Please enter the book id which you want to borrow: ")
            if self.records.checkBorrow(card_id, bid):
                print("You have borrowed the book!")
                return
            res = self.books.borrow(bid)
            if res:
                tmp = self.records.addBorrowRecord(card_id, bid)
                if tmp:
                    print("Here you are")
                else:
                    print("Sorry!")
            else:
                print("Sorry!")
            print("------------------------------------------------------------------------------------------------")
            print("                                                                                                ")
            print("                                                                                                ")
        else:
            return

    def returnBook(self):
        cid = input("Please enter your 7 digits card id: ")
        bid = input("Please enter the id of your book you want return: ")
        ret_res = self.records.returnRecord(cid, bid)
        if ret_res:
            if self.books.returnBook(bid):
                print("Successfully returned!")
        else:
            print("You didn't borrow the book.")
        print("------------------------------------------------------------------------------------------------")
        print("                                                                                                ")
        print("                                                                                                ")

    def showBorrowed(self):
        cid = input("Please enter your card id: ")
        res = self.records.showBorrowed(cid)
        if res:
            print("------------------------------------------------------------------------------------------------")
            for one in res:
                print("Card_id:{0} Book_id:{1} borrow_date:{2} Return_date:{3}".format(one[0], one[1], one[2], one[3]))
        else:
            print("You didn't borrow any books")

        print("------------------------------------------------------------------------------------------------")
        print("                                                                                                ")
        print("                                                                                                ")

    def cardManage(self):
        choice = input("You can register typing 1.\n"
                       "You can remove a card typing 2\n"
                       "You can modify a card typing 3\n")
        res = self.cards.cardManage(choice)
        if res:
            print("Successfully done!")
        else:
            print("Failed for unknown reason!")
        print("------------------------------------------------------------------------------------------------")
        print("                                                                                                ")
        print("                                                                                                ")