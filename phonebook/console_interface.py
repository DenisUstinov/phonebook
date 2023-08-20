from typing import List, Dict
from phonebook.text_db import DataAccessObject


class ConsoleInterface:
    """
    Класс ConsoleInterface предоставляет консольный интерфейс для взаимодействия с базой данных.
    """

    def __init__(self, db_instance: DataAccessObject):
        """
        Инициализация объекта для взаимодействия с базой данных.

        :param db_instance: Экземпляр класса для взаимодействия с базой данных.
        """
        self.db: DataAccessObject = db_instance

    def run(self) -> None:
        """
        Запуск консольного интерфейса для взаимодействия с базой данных.
        """
        print("Добро пожаловать в консольный интерфейс телефонного справочника!")
        while True:
            print("\nВыберите действие:")
            print("1. Вывод постранично записей из справочника на экран")
            print("2. Добавление новой записи в справочник")
            print("3. Возможность редактирования записей в справочнике")
            print("4. Поиск записей по одной или нескольким характеристикам")
            print("5. Выход")

            choice: str = input("Введите номер действия: ")

            if choice == '1':
                self.show_records()
            elif choice == '2':
                self.add_record()
            elif choice == '3':
                self.edit_record()
            elif choice == '4':
                self.search_records()
            elif choice == '5':
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите действие из списка.")

    def display_records(self, records: List[Dict[str, str]], current_page: int, records_per_page: int) -> None:
        """
        Выводит список записей на экран.

        :param records: Список записей для отображения.
        :param current_page: Текущая страница.
        :param records_per_page: Количество записей на странице.
        """
        print("\nСписок записей:")
        for index, record in enumerate(records, start=(current_page - 1) * records_per_page + 1):
            print(f"\nЗапись {index}:")
            for key, value in record.items():
                print(f"{key}: {value}")

    def show_records(self) -> None:
        """
        Организует вывод записей постранично.
        """
        records_per_page: int = 10
        current_page: int = 1

        num_records: int = self.db.get_records_count()
        all_pages: int = (num_records + records_per_page - 1) // records_per_page

        while True:
            records = self.db.get_records(
                num_records_start=(current_page - 1) * records_per_page,
                num_records=records_per_page
            )

            if records:
                self.display_records(records, current_page, records_per_page)
                print(f"\nСтраница {current_page} из {all_pages}")
                if current_page < all_pages:
                    print("1. Следующая страница")
                if current_page > 1:
                    print("2. Предыдущая страница")
            else:
                print("В справочнике нет записей!")
            print("3. Вернуться в меню")

            while True:
                choice: str = input("Выберите действие: ")
                if choice == '1' and current_page < all_pages:
                    current_page += 1
                    break
                elif choice == '2' and current_page > 1:
                    current_page -= 1
                    break
                elif choice == '3':
                    return
                else:
                    print("Неверный выбор. Пожалуйста, выберите действие из списка.")

    def add_record(self) -> None:
        """
        Добавляет новую запись в базу данных.
        """
        record = {
            'id': str(self.db.get_records_count() + 1),
            'last_name': input("Фамилия: "),
            'first_name': input("Имя: "),
            'middle_name': input("Отчество: "),
            'organization': input("Название организации: "),
            'work_phone': self.get_valid_phone("Рабочий телефон: "),
            'personal_phone': self.get_valid_phone("Личный телефон: ")
        }
        self.db.add_record(record)
        print("Запись добавлена успешно!")

    def edit_record(self) -> None:
        """
        Редактирует выбранную запись в базе данных.
        """
        record_number_input: str = input("Введите id записи для редактирования: ")

        if not record_number_input.isdigit():
            print("Некорректный ввод. Введите число.")
            return

        record_number: int = int(record_number_input) - 1

        if not (0 <= record_number <= self.db.get_records_count()):
            print("Некорректный номер записи.")
            return

        new_record = {
            'id': str(record_number_input),
            'last_name': input("Новая фамилия: "),
            'first_name': input("Новое имя: "),
            'middle_name': input("Новое отчество: "),
            'organization': input("Новое название организации: "),
            'work_phone': self.get_valid_phone("Новый рабочий телефон: "),
            'personal_phone': self.get_valid_phone("Новый личный телефон: ")
        }

        self.db.edit_record(record_number, new_record)
        print("Запись отредактирована успешно!")

    def search_records(self) -> None:
        """
        Поиск записей в базе данных по заданным характеристикам.
        """
        print("Поиск записей:")
        print("Введите данные для поиска в формате: фильтр=значение, если параметр не один, через запятую")
        print("Поддерживаемые фильтры: id, last_name, first_name, middle_name, organization, work_phone, personal_phone")
        search_data: str = input("Введите данные для поиска: ")

        search_filters = {}
        search_params = search_data.split(',')
        for param in search_params:
            key, value = param.strip().split('=')
            search_filters[key] = value

        records = self.db.get_records_by_filters(filters=search_filters)

        if records:
            print("\nРезультаты поиска:")
            for index, record in enumerate(records, start=1):
                print(f"\nЗапись {index}")
                for key, value in record.items():
                    print(f"{key}: {value}")
        else:
            print("Записи с заданными параметрами не найдены.")

    def get_valid_phone(self, prompt: str) -> str:
        """
        Получает от пользователя действительный телефонный номер.

        :param prompt: Подсказка для ввода.
        :return: Действительный телефонный номер.
        """
        while True:
            phone: str = input(prompt)
            if phone.isdigit() and len(phone) >= 7:
                return phone
            else:
                print("Некорректный номер. Введите только цифры, минимум 7 символов.")
