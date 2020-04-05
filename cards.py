class Cards:
    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    def createCard(self, name, department, type):
        query_sql = "select * from card"
        self.cursor.execute(query_sql)
        num = len(self.cursor.fetchall())
        id = (1000000 + num).__str__()
        sql = "insert into card (cno, name, department, type) values ('{0}', '{1}', '{2}', '{3}');".format(id, name,
                                                                                                           department,
                                                                                                           type)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Registered successfully! "
                  "Remember that your id is {0}. "
                  "You can borrow now".format(id))
            return id
        except:
            self.db.rollback()
            print("Failed to register!")
            return None


