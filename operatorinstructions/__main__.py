#!/usr/bin/python
"""

This is the main program to run the operator instructions program from.
It handles creating objects and swiching between different presentations.
Created by Ryan Massoth
"""
import socket
from time import sleep
import logging
import logging.handlers
from urllib.request import Request
from operatorinstructions.soffice_handler import SofficeHandler
from operatorinstructions.file_handler import FileHandler
from operatorinstructions.database_handler import DatabaseHandler

soffice = SofficeHandler()
file_handler = FileHandler()
database_handler = DatabaseHandler(database="plantfloor")
UNCONFIGURED = ("http://ah-plantfloor.marisabae.com/media/operatorinstructions"
               "/Unconfigured.pptx")
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# log_handler = logging.handlers.RotatingFileHandler(
#     "operatorinstructions.log",
#     maxBytes=500000,
#     backupCount=2)
# log_format = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
# log_handler.setFormatter(log_format)
# logger.addHandler(log_handler)

class RPI():
    """

    Class for holding information about the current unit.
    """

    def __init__(self, unit_id=0, hostname="Unknown", ipaddress="",
                 description="", active=False, linenumber_id=""):

        self.unit_id = unit_id
        self.hostname = hostname
        self.ipaddress = ipaddress
        self.description = description
        self.active = active
        self.linenumber_id = linenumber_id

def copy_new_version():
    """

    Gets the new version of this program and replaces itself and
    restarts.
    """
    pass

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
            rpi = RPI(unit_id=rpi_config[0],
                      hostname=rpi_config[1],
                      ipaddress=rpi_config[2],
                      description=rpi_config[3],
                      active=rpi_config[4],
                      linenumber_id=rpi_config[5])

            recipe = database_handler.get_current_running_recipe(
                rpi.linenumber_id)
            files = database_handler.get_all_files(rpi.unit_id, recipe)
            if bool(files):
                soffice.files = files
            else:
                soffice.files.append(UNCONFIGURED)
            if soffice.load_main_file_from_network():
                soffice.show_main_slideshow()
            else:
                soffice.files[0] = (UNCONFIGURED)
                if soffice.load_main_file_from_network():
                    soffice.show_main_slideshow()
            logger.debug("Setup complete, entering main loop...")

        while(True):
            # Main loop
            recipe = database_handler.get_current_running_recipe(
                rpi.linenumber_id)
            files = database_handler.get_all_files(rpi.unit_id, recipe)
            # Change main slideshow if recipe changed
            if bool(files) and files != soffice.files:
                soffice.files = files
                soffice.end_main_slideshow()
                soffice.load_main_file_from_network()
                soffice.show_main_slideshow()
            else:
                soffice.files.append(UNCONFIGURED)

            # Restart soffice if it died for some reason
            if soffice.sub.poll() is not None:
                logger.debug("Soffice died. Poll: {}".format(
                    soffice.sub.poll()))
                #soffice.kill_soffice() # gets stuck for some reason
                soffice.start_soffice()
                soffice.connect()
                soffice.load_main_file_from_network()
                soffice.show_main_slideshow()
            sleep(30)
        soffice.kill_soffice()
    except Exception as error:
        logger.error(error)
        raise

if __name__ == "__main__":
    main()
