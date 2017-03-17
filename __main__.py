"""

This is the main program to run the operator instructions program from.
It handles creating objects and swtiching between different presentations.
"""
import socket
from time import sleep
from soffice_handler import SofficeHandler
from file_handler import FileHandler
from database_handler import DatabaseHandler

soffice = SofficeHandler()
file_handler = FileHandler()
database_handler = DatabaseHandler(database='plantfloor')

class RPI():
    """

    Class for holding information about the current unit.
    """

    def __init__(self, unit_id=0, hostname="Unknown", ipaddress="",
                 description="", active=False, linenumber_id=''):

        self.unit_id = unit_id
        self.hostname = hostname
        self.ipaddress = ipaddress
        self.description = description
        self.active = active
        self.linenumber_id = linenumber_id

def main():
    """

    Main routine for managing the operator instructions
    """

    try:
        soffice.start_soffice()
        soffice.connect()
        rpi_config = database_handler.get_rpi_config(
            hostname=socket.gethostname())
        if rpi_config:
            rpi = RPI(rpi_config[0],
                      rpi_config[1],
                      rpi_config[2],
                      rpi_config[3],
                      rpi_config[4],
                      rpi_config[5])

            recipe = database_handler.get_current_running_recipe(
                rpi.linenumber_id)
            file = database_handler.get_current_recipe_filename(rpi.unit_id,
                                                                recipe)
            if file:
                soffice.files.append(file)
                soffice.load_main_file_from_network()
                soffice.show_main_slideshow()
                sleep(10)
                soffice.end_main_slideshow()
            else:
                print("No file")
        while(True):
            sleep(10)
        soffice.kill_soffice()
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()
