import mysql.connector
from config import CONNECTION_SETTINGS, EXPORT_TYPES
import json
import queries


class Database:
    """
    Class which is used as implementation for database usage
    """
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**CONNECTION_SETTINGS)
        except mysql.connector.Error as e:
            raise ConnectionError from e
        self.connection.close()

    def import_data(self, path: str, import_table: str):
        """
        Method to import data into database

        :param path: path to import file
        :param import_table: table to import
        """
        self.connection.connect()
        with open(path, 'r') as f:
            data = json.load(f)
        query = self.get_import_query(import_table, data)
        cursor = self.connection.cursor()
        cursor.execute(query)
        cursor.close()
        self.connection.commit()
        self.connection.close()

    def get_import_query(self, query_type: str, query_data: dict) -> str:
        query_builders = {
            'rooms': self.get_import_query_rooms,
            'students': self.get_import_query_students
        }
        return query_builders[query_type](query_data)

    @staticmethod
    def get_import_query_students(student_data: dict) -> str:
        base_query = 'INSERT INTO student_classes.students (id, birthday, name, roomId, sex) VALUES \n'
        values_query = ''
        for student in student_data:
            values_query += (f',\n({student['id']}, \'{student['birthday']}\', \'{student['name']}\', '
                             f'{student['room']}, \'{student['sex']}\')')

        query = base_query + values_query[1:]
        return query

    @staticmethod
    def get_import_query_rooms(room_data: dict) -> str:
        base_query = 'INSERT INTO student_classes.rooms (id, name) VALUES \n'
        values_query = ''
        for room in room_data:
            values_query += f',\n({room['id']}, \'{room['name']}\')'

        query = base_query + values_query[1:]
        return query

    def export_data(self, path: str, export_report: str):
        """
        Method to import data into database

        :param path: path to export file
        :param export_report: type of report to export
        """
        export_data_dict = dict()
        if export_report == 'all':
            for export_type in EXPORT_TYPES:
                export_data_dict[export_type] = self.get_data_for_export(self.get_export_query(export_type))
        else:
            export_data_dict[export_report] = self.get_data_for_export(self.get_export_query(export_report))

        with open(path, 'w') as f:
            json.dump(export_data_dict, f)

        self.connection.close()

    def get_data_for_export(self, query: str) -> list[dict]:
        self.connection.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    @staticmethod
    def get_export_query(export_type: str) -> str:
        if export_type == 'count':
            return queries.get_count_query()
        elif export_type == 'average':
            return queries.get_avg_query()
        elif export_type == 'difference':
            return queries.get_dif_query()
        elif export_type == 'sex':
            return queries.get_sex_query()
