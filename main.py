from phonebook.console_interface import ConsoleInterface
from phonebook.text_db import JsonDB, CsvDB, DataAccessObject

if __name__ == "__main__":
    def get_db_object(db_type):
        if db_type == "csv":
            return CsvDB()
        elif db_type == "json":
            return JsonDB()

    type_db = 'json'

    db: DataAccessObject = get_db_object(type_db)
    db.connect(f'database_{type_db}.txt')

    console_interface: ConsoleInterface = ConsoleInterface(db)
    console_interface.run()

