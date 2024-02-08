import sys

EXPORT_OPTIONS = {'all', 'dif', 'avg', 'count', 'sex'}


def start_message():
    """
    This function is used at the start of script

    It describes possible usage for different scenarios of database usage
    for import/export

    """
    if len(sys.argv) == 1:
        print('Write python main.py --help to get usage information')
        sys.exit(0)
    if sys.argv[1] == '--help' or sys.argv[1] == '-h' or sys.argv[1] == 'help':
        print('Usage: python main.py <action> [export_type] [file1_path] [file2_path] [export_file]')
        print('Actions:')
        print('  * help, --help, h: Get help usage message')
        print('  * import: Import data from files')
        print('  * export: Export data to a file')
        print('Optional arguments:')
        print('  * import: ')
        print('    * file1_path: path to file with rooms (import only)')
        print('    * file2_path: path to file with students (import only)')
        print('  * export: ')
        print('    * export_type: report to export (export only)')
        print('      * all: export all types in single json')
        print('      * count: export rooms with count of students')
        print('      * avg: export 5 rooms with minimum average age of students')
        print('      * dif: export 5 rooms with maximum difference in ages')
        print('      * sex: export rooms with both sexes in them')
        print('    * export_file: path to file to export data (export only)')
        sys.exit(0)

    if len(sys.argv) > 4:
        print('Usage: python main.py <action> [export_type] [file1_path] [file2_path] [export_file]')
        print('  write python main.py --help to get more details')
        sys.exit(0)

    elif sys.argv[1] == 'import':
        if len(sys.argv) == 2:
            return {'action': 'import', 'rooms_path': 'rooms.json', 'students_path': 'students.json'}
        elif len(sys.argv) == 3:
            return {'action': 'import', 'rooms_path': sys.argv[2], 'students_path': 'students.json'}
        elif len(sys.argv) == 4:
            return {'action': 'import', 'rooms_path': sys.argv[2], 'students_path': sys.argv[3]}

    elif sys.argv[1] == 'export':
        if len(sys.argv) == 2:
            return {'action': 'export', 'export_type': 'all', 'export_path': 'format.json'}
        elif sys.argv[2] not in EXPORT_OPTIONS:
            print('Invalid export type')
            sys.exit(0)
        elif len(sys.argv) == 3:
            return {'action': 'export', 'export_type': sys.argv[2], 'export_path': 'format.json'}
        elif len(sys.argv) == 4:
            return {'action': 'export', 'export_type': sys.argv[2], 'export_path': sys.argv[3]}

    else:
        print('Invalid action type')
        sys.exit(0)
