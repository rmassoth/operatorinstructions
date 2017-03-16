import pytest
from soffice_handler import SofficeHandler
from time import sleep

from com.sun.star.connection import NoConnectException

soffice = SofficeHandler()

def test_soffice_connection():
    soffice.start_soffice()
    soffice.connect()
    soffice.kill_soffice()
    # pausing after killing due to port still being open shortly after killing
    # if you try to connect again too soon it throws errors.
    sleep(3)

def test_load_main_file():
    soffice.start_soffice()
    soffice.files.append("tests/Unconfigured.ppt")
    soffice.connect()
    soffice.load_main_file()
    soffice.show_main_slideshow()
    soffice.end_main_slideshow()
    soffice.kill_soffice()
    # pausing again
    sleep(3)

def test_soffice_connection_failure():
    with pytest.raises(NoConnectException):
        soffice.connect()
