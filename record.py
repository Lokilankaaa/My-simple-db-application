import time


class Record:
    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    def addBorrowRecord(self, cid, bid):
        now = time.strftime("%Y%m%d", time.localtime())
        then = 'null'
        insert_sql = "insert into borrow (cno, bno, borrow_date, return_date) values ('{0}', '{1}', '{2}', {3});".format(
            cid, bid, now, then)
        try:
            self.cursor.execute(insert_sql)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def checkBorrow(self, cid, bid):
        query_sql = "select * from borrow where cno='{0}' and bno='{1}' and return_date is null".format(cid, bid)
        try:
            self.cursor.execute(query_sql)
            res = self.cursor.fetchall()
            if res:
                return True
            else:
                return False
        except:
            return False

    def returnRecord(self, cid, bid):
        res = self.checkBorrow(cid, bid)
        now = time.strftime("%Y%m%d", time.localtime())
        update_sql = "update borrow set return_date='{0}' where cno='{1}' and bno='{2}';".format(now, cid, bid)
        if res:
            try:
                self.cursor.execute(update_sql)
                self.db.commit()
                return True
            except:
                self.db.rollback()
                return False
        else:
            return False

    def showBorrowed(self, cid):
        query_sql = "select * from borrow where cno='{0}'".format(cid)
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
