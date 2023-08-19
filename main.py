from phonebook.console_interface import ConsoleInterface
from phonebook.text_db import TextDB


if __name__ == "__main__":
    db = TextDB()
    db.connect('database.txt')
    console_interface = ConsoleInterface(db)
    console_interface.run()
