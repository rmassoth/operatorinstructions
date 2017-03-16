"""

This is the main program to run the operator instructions program from.
It handles creating objects and swtiching between different presentations.
"""
from soffice_handler import SofficeHandler
from file_handler import FileHandler
from database_handler import DatabaseHandler

soffice_handler = SofficeHandler()
file_handler = FileHandler()
database_handler = DatabaseHandler(database='plantfloor')

try:
    soffice_handler.start_soffice()
except Exception as error:
    print(error)
