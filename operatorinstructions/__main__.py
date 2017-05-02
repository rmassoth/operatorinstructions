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
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
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
        rpi_configured = False
        while not rpi_configured:
            rpi_config = database_handler.get_rpi_config(
                hostname=socket.gethostname())
            if rpi_config:
                rpi = RPI(unit_id=rpi_config[0],
                          hostname=rpi_config[1],
                          ipaddress=rpi_config[2],
                          description=rpi_config[3],
                          active=rpi_config[4],
                          linenumber_id=rpi_config[5])
                rpi_configured = True
            else:
                logger.warning("No config found for this unit ({}) in the "
                            "database. Pausing for 30 seconds..."
                            .format(socket.gethostname()))
                sleep(30)

        while(True):
            # Main loop
            recipe = database_handler.get_current_running_recipe(
                rpi.linenumber_id)
            # Get urls from the database
            files = database_handler.get_all_files(rpi.unit_id, recipe)

            # Change main slideshow if recipe changed
            if bool(files) and files != soffice.files:
                # Set the new files
                soffice.files = files
                current_presentation = 0
                last_presentation = None
                if bool(soffice.presentations):
                    soffice.end_slideshow()
                    soffice.close_files()
                # Load the new files from the network
                soffice.load_files_from_network()
                sleep(5)
            # Set the unconfigured path if no files are configured
            # in the database
            if not bool(files) and soffice.files != [ UNCONFIGURED ]:
                logger.warning("No files setup in database, setting "
                               "unconfigured.")
                soffice.files = [ UNCONFIGURED ]
                soffice.load_files_from_network()
                current_presentation = 0
                last_presentation = None
                sleep(5)

            # Restart soffice if it died for some reason
            if soffice.sub.poll() is not None:
                # logger.debug("Soffice died. Poll: {}".format(
                    # soffice.sub.poll()))
                #soffice.kill_soffice() # gets stuck for some reason
                soffice.start_soffice()
                soffice.connect()
            else:
                num_presentations = len(soffice.presentations)

                # Reset presentation count if greater than or equal
                # to the number of presentations
                if current_presentation >= num_presentations:
                    current_presentation = 0

                # Show current presentation if it isn't None
                if soffice.presentations[current_presentation]:
                    if current_presentation != last_presentation:
                        soffice.end_slideshow()
                        soffice.show_slideshow(current_presentation)
                last_presentation = current_presentation
                current_presentation += 1
            sleep(10)
        soffice.kill_soffice()
    except Exception as error:
        logger.error(error)
        raise

if __name__ == "__main__":
    main()
