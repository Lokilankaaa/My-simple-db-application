class Books:
    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    def __update__(self, choice, bookInfo):
        sql = "update book\
               set "
        if choice == 1:
            for key, value in bookInfo.items():
                if key == 'book_id':
                    sql += "{0}='{1}'".format(key, value)
                else:
                    sql += ",{0}='{1}'".format(key, value)
        else:
            sql += "total=total+'{0}', stock=stock+'{1}'".format(bookInfo['num'], bookInfo['num'])
        sql += "where bno={0}".format(bookInfo['book_id'])
        return sql

    def store(self, bookInfo):
        test_sql = "select * from book where bno=" + "'" + bookInfo['book_id'] + "'"
        insert_sql = "insert into book (bno, category, title, press, year, author, price, total, stock) values " \
                     "('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}');".format(bookInfo["book_id"],
                                                                                               bookInfo["category"],
                                                                                               bookInfo["title"],
                                                                                               bookInfo["press"],
                                                                                               bookInfo["year"],
                                                                                               bookInfo["author"],
                                                                                               bookInfo["price"],
                                                                                               bookInfo["num"],
                                                                                               bookInfo["num"])
        self.cursor.execute(test_sql)
        results = self.cursor.fetchone()
        if not results:
            try:
                self.cursor.execute(insert_sql)
                self.db.commit()
                print("Successfully stored!")
            except:
                self.db.rollback()
                print("Fail to store for unknown reason!")
        else:
            print("The book has already been in storage.\n"
                  "You can modify the information or add it to storage")
            choice = input("Modify(typing 1) or Add to storage(typing 2): ")
            update_sql = self.__update__(choice, bookInfo)
            try:
                self.cursor.execute(update_sql)
                self.db.commit()
                print("Successfully modified!")
            except:
                self.db.rollback()
                print("Fail to modify for unknown reason!")

    def query(self, info):
        query_sql = "select * from book "
        i=0
        for key, value in info.items():
            if value != '':
                if not i:
                    query_sql += 'where '
                    i += 1
                elif i:
                    query_sql += 'and'
                if key == 'year' or key == 'value':
                    tmp = value.split(' ')
                    tmp.remove('to')
                    query_sql += " {0}='{1}' ".format(key, tmp[0]) if tmp[0] == tmp[1] else " '{0}'<={1}<='{2}' ".format(tmp[0],
                                                                                                                 key,
                                                                                                                 tmp[1])
                else:
                    query_sql += " {0}='{1}' ".format(key, value)

        try:
            self.cursor.execute(query_sql)
            self.db.commit()
            return self.cursor.fetchall()
        except:
            print("Query failed for unknown reason!")
            return None