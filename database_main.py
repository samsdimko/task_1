import mysql.connector
from config import CONNECTION_SETTINGS, EXPORT_TYPES
import json
import queries
import pandas as pd


class Database(object):
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
        cursor = self.connection.cursor()
        chunks = pd.read_json(path, lines=True, chunksize=10000)
        for chunk in chunks: 
            query = self.get_import_query(import_table, chunk.to_dict('records'))
            cursor.execute(query)
        cursor.close()
        self.connection.commit()
        self.connection.close()

    def get_import_query(self, query_type: str, query_data: list[dict]) -> str:
        """
        Method to call query-creator for data import

        :param query_type: type of data import
        :param query_data: data to import
        """
        query_builders = {
            'rooms': self.get_import_query_rooms,
            'students': self.get_import_query_students
        }
        return query_builders[query_type](query_data)

    @staticmethod
    def get_import_query_students(student_data: list[dict]) -> str:
        """
        Method to create query to import student data into database

        :param student_data: student data for import
        """
        base_query = 'INSERT INTO student_classes.students (id, birthday, name, roomId, sex) VALUES \n'
        values_query = ''
        for student in student_data:
            values_query += (f",\n({student['id']}, \'{student['birthday']}\', \'{student['name']}\', "
                             f"{student['room']}, \'{student['sex']}\')")

        query = base_query + values_query[1:]
        return query

    @staticmethod
    def get_import_query_rooms(room_data: list[dict]) -> str:
        """
        Method to create query to import room data into database

        :param room_data: room data for import
        """
        base_query = 'INSERT INTO student_classes.rooms (id, name) VALUES \n'
        values_query = ''
        for room in room_data:
            values_query += f",\n({room['id']}, \'{room['name']}\')"

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
        """
        Method for data extraction for report
        """
        self.connection.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    @staticmethod
    def get_export_query(export_type: str) -> str:
        """
        Method to create data export query
        """
        query_selector = {
            'count': queries.get_count_query,
            'average': queries.get_avg_query,
            'difference': queries.get_dif_query,
            'sex': queries.get_sex_query
        }
        return query_selector[export_type]()
