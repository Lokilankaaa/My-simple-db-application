import random

class Cards:
    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    def createCard(self, name, department, type):
        query_sql = "select * from card"
        self.cursor.execute(query_sql)
        num = len(self.cursor.fetchall()) + random.randint(0, 9999999)
        id = ((1000000 + num)%9999999).__str__()
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

    def cardManage(self, choice):
        if choice == '1':
            name = input("Please enter your name(no more than 10 letters): ")
            department = input("Please enter your department name(no more than 40 letters): ")
            type = input("Please enter your card type(T or S): ")
            id = self.createCard(name, department, type)
            return id
        elif choice == '2':
            cno = input("Please enter your card id: ")
            sql = "delete from card where cno='{0}'".format(cno)
            try:
                self.cursor.execute(sql)
                self.db.commit()
                return True
            except:
                self.db.rollback()
                return False
        elif choice == '3':
            cno = input("Please enter your card id: ")
            name = input("Please enter the name which you want to modify(If you don't want so, just pass it by enter): ")
            dep = input(
                "Please enter the department name which you want to modify(If you don't want so, just pass it by enter): ")
            type = input(
                "Please enter the type(T or S) which you want to modify(If you don't want so, just pass it by enter): ")
            sql = "update card set "
            info = {"name":name, "department":dep, "type":type}
            for key, value in info.items():
                if value:
                    sql += " {0}='{1}', ".format(key, value)
            sql += "cno='{0}' where cno='{0}'".format(cno)
            try:
                self.cursor.execute(sql)
                self.db.commit()
                return True
            except:
                self.db.rollback()
                return False