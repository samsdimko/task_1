import mysql.connector
from config import CONNECTION_SETTINGS, EXPORT_TYPES
import json
import queries


class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**CONNECTION_SETTINGS)
        except mysql.connector.Error as e:
            raise ConnectionError from e
        self.connection.close()

    def import_data(self, path: str, import_type: str):
        self.connection.connect()
        with open(path, 'r') as f:
            data = json.load(f)
        query = self.get_import_query(import_type, data)
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

    def export_data(self, path: str, export_type: str):
        export_dict = dict()
        if export_type == 'all':
            for etype in EXPORT_TYPES:
                export_dict[etype] = self.get_data_for_export(self.get_export_query(etype))
        else:
            export_dict[export_type] = self.get_data_for_export(self.get_export_query(export_type))

        with open(path, 'w') as f:
            json.dump(export_dict, f)

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
            return queries.ROOMS_WITH_COUNT_STUDENTS_QUERY
        elif export_type == 'average':
            return queries.ROOMS_WITH_MIN_AVERAGE_AGE_QUERY
        elif export_type == 'difference':
            return queries.ROOMS_WITH_MAXIMUM_DIFFERENCE_IN_AGE_QUERY
        elif export_type == 'sex':
            return queries.ROOMS_WITH_BOTH_SEXES_QUERY
