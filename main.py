from phonebook.console_interface import ConsoleInterface
from phonebook.text_db import JsonDB, CsvDB, DataAccessObject

if __name__ == "__main__":
    db: DataAccessObject = JsonDB()
    db.connect('database_json.txt')
    # db: DataAccessObject = CsvDB()
    # db.connect('database_csv.txt')
    console_interface: ConsoleInterface = ConsoleInterface(db)
    console_interface.run()

