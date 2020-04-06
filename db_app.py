from librarydb import LibraryDB

if __name__ == "__main__":
    params = {'host':'', 'user':'', 'passwd':'', 'db':''}
    with open("myhost.txt") as f:
        lines = f.readlines()
        for line in lines:
            tmp = line.split('=')
            params[tmp[0]] = tmp[1].strip('\n')
    myDB = LibraryDB(params)
    while True:
        command = input('-----------------------------------------------------\n'
                        'Welcome to the library.\n'
                        '-----------------------------------------------------\n'
                        'You can store one book typing 1.\n'
                        'You can store batch of books typing 2.\n'
                        'You can query books typing 3.\n'
                        'You can borrow a book typing 4.\n'
                        'You can get details about what you borrowed typing 5.\n'
                        'You can return a book typing 6.\n'
                        'You can manage cards typing 7.\n'
                        'You can quit typing q.\n')
        if command == '1':
            myDB.storeBooks()
        elif command == '2':
            myDB.storeBooks(batch=True)
        elif command == '3':
            myDB.queryBooks()
        elif command == '4':
            myDB.borrowBook()
        elif command == '5':
            myDB.showBorrowed()
        elif command == '6':
            myDB.returnBook()
        elif command == '7':
            myDB.cardManage()
        elif command == 'q':
            print("Bye!")
            break
        else:
            print("Unknown command! Please try again.")
            print("------------------------------------------------------------------------------------------------")
            print("                                                                                                ")
            print("                                                                                                ")
