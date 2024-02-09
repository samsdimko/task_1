# Task 1 database application
This is a small application for processing student database. 

## Purpose:

This project provides a command-line interface for interacting with a MySQL database containing student and room data. It offers two main functionalities:

**Data Import**: Allows importing room and student data from JSON files into the database.
**Data Export**: Enables exporting various reports based on the database content to a JSON file.

**Installation**: Ensure Python and mysql-connector-python are installed.
**Configuration**: In ```config.py```, set your MySQL connection details.

### **Import**:
* ```python main.py import [rooms_path] [students_path]```
* ```rooms_path (optional)```: Path to JSON file containing room data (default: rooms.json).
* ```students_path (optional)```: Path to JSON file containing student data (default: students.json).

### **Export**:
* ```python main.py export [export_type] [export_path]```
* ```export_type```: Type of report to export (default: all).
* * ```all```: Export all reports in separate sections within a single JSON file.
* * ```count```: Export rooms with the number of students.
* * ```avg```: Export 5 rooms with the minimum average student age.
* * ```dif```: Export 5 rooms with the maximum difference in student ages.
* * ```sex```: Export rooms with both male and female students.
* ```export_path (optional)```: Path to save the exported data (default: format.json).

## Additional Notes:

Use ```python main.py --help``` for detailed usage information.
Modify ```config.py``` to adjust database connection settings.