from phonebook.console_interface import ConsoleInterface
from phonebook.text_db import TextDB, DataAccessObject

if __name__ == "__main__":
    db: DataAccessObject = TextDB()
    db.connect('database.txt')
    console_interface: ConsoleInterface = ConsoleInterface(db)
    console_interface.run()

