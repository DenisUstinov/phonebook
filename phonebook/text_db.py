import json
import csv
from dataclasses import dataclass, fields
from typing import List, Dict, Union


class DataAccessObject:
    def connect(self, connection_info: str) -> None:
        """
        Инициализирует соединение с базой данных.

        :param connection_info: Информация о соединении, может быть путем к файлу или деталями подключения.
        """
        pass

    def add_record(self, record: Dict[str, Union[str, int]]) -> None:
        """
        Добавляет новую запись в базу данных.

        :param record: Словарь с данными записи.
        """
        pass

    def get_records_by_filters(self, filters: Dict[str, Union[str, int]]) -> List[Dict[str, Union[str, int]]]:
        """
        Возвращает список записей, соответствующих заданным фильтрам.

        :param filters: Словарь с фильтрами для поиска записей.
        :return: Список словарей с данными записей.
        """
        pass

    def get_records(self, num_records_start: int, num_records: int) -> List[Dict[str, Union[str, int]]]:
        """
        Получает определенное количество записей из базы данных.

        :param num_records_start: Номер записи, с которой начать выборку.
        :param num_records: Количество записей для выборки.
        :return: Список словарей с данными записей.
        """
        pass

    def edit_record(self, record_number: int, new_record: Dict[str, Union[str, int]]) -> None:
        """
        Редактирует существующую запись в базе данных.

        :param record_number: Номер записи для редактирования.
        :param new_record: Словарь с новыми данными для записи.
        """
        pass

    def get_records_count(self) -> int:
        """
        Возвращает общее количество записей в базе данных.

        :return: Общее количество записей.
        """
        pass


class JsonDB(DataAccessObject):
    def __init__(self):
        self.file_path: str = ''

    def connect(self, file_path: str) -> None:
        """
        Устанавливает путь к файлу базы данных.

        :param file_path: Путь к файлу базы данных.
        """
        self.file_path = file_path

    def add_record(self, record: Dict[str, Union[str, int]]) -> None:
        """
        Добавляет запись в конец файла.

        :param record: Словарь с данными записи.
        """
        with open(self.file_path, 'a') as file:
            json.dump(record, file)
            file.write('\n')

    def get_records_by_filters(self, filters: Dict[str, Union[str, int]]) -> List[Dict[str, Union[str, int]]]:
        """
        Получает записи из файла, соответствующие заданным фильтрам.

        :param filters: Словарь с фильтрами вида {key1: value1, key2: value2}.
        :return: Список словарей с данными записей.
        """
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        records = [json.loads(line) for line in lines]

        for key, value in filters.items():
            records = [record for record in records if record.get(key) == value]

        return records

    def get_records(self, num_records_start: int, num_records: int) -> List[Dict[str, Union[str, int]]]:
        """
        Получает записи из файла, начиная с заданной строки и возвращая заданное количество записей.

        :param num_records_start: Начальная строка для выборки записей.
        :param num_records: Количество записей для выборки.
        :return: Список словарей с данными записей.
        """
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        records = [json.loads(line) for line in lines[num_records_start:num_records_start + num_records]]

        return records

    def edit_record(self, record_number: int, new_record: Dict[str, Union[str, int]]) -> None:
        """
        Редактирует запись в файле.

        :param record_number: Номер строки записи для редактирования.
        :param new_record: Словарь с новыми данными для записи.
        """
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        if 0 <= record_number < len(lines):
            lines[record_number] = json.dumps(new_record) + '\n'

        with open(self.file_path, 'w') as file:
            file.writelines(lines)

    def get_records_count(self) -> int:
        """
        Возвращает общее количество записей в базе данных.

        :return: Общее количество записей.
        """
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        return len(lines)


@dataclass
class Record:
    id: int
    last_name: str
    first_name: str
    middle_name: str
    organization: str
    work_phone: str
    personal_phone: str


class CsvDB(DataAccessObject):
    """
    Класс для работы с базой данных в формате CSV.
    """
    file_path: str = ''  # Путь к файлу базы данных
    field_names = [field.name for field in fields(Record)]  # Список названий полей записи

    def connect(self, file_path: str) -> None:
        """
        Устанавливает путь к файлу базы данных.

        :param file_path: Путь к файлу базы данных.
        """
        self.file_path = file_path

    def add_record(self, record: Dict[str, Union[str, int]]) -> None:
        """
        Добавляет запись в конец файла.

        :param record: Словарь с данными записи.
        """
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.field_names)
            writer.writerow(record)

    def get_records_by_filters(self, filters: Dict[str, Union[str, int]]) -> List[Dict[str, Union[str, int]]]:
        """
        Получает записи из файла, соответствующие заданным фильтрам.

        :param filters: Словарь с фильтрами вида {key1: value1, key2: value2}.
        :return: Список словарей с данными записей.
        """
        with open(self.file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            records = [record for record in reader if
                       all(record.get(key) == str(value) for key, value in filters.items())]
        return records

    def get_records(self, num_records_start: int, num_records: int) -> List[Dict[str, Union[str, int]]]:
        """
        Получает записи из файла, начиная с заданной строки и возвращая заданное количество записей.

        :param num_records_start: Начальная строка для выборки записей.
        :param num_records: Количество записей для выборки.
        :return: Список словарей с данными записей.
        """
        with open(self.file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            records = list(reader)[num_records_start:num_records_start + num_records]

        return records

    def edit_record(self, record_number: int, new_record: Dict[str, Union[str, int]]) -> None:
        """
        Редактирует запись в файле.

        :param record_number: Номер строки записи для редактирования.
        :param new_record: Словарь с новыми данными для записи.
        """
        records = []

        with open(self.file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for idx, record in enumerate(reader):
                if idx == record_number:
                    records.append(new_record)
                else:
                    records.append(record)

        with open(self.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.field_names)
            writer.writeheader()
            writer.writerows(records)

    def get_records_count(self) -> int:
        """
        Возвращает общее количество записей в базе данных.

        :return: Общее количество записей.
        """
        with open(self.file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            return len(list(reader)) - 1  # Вычитаем 1 для заголовочной строки


