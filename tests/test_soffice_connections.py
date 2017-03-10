import pytest
from soffice_handler import SofficeHandler
from time import sleep

from com.sun.star.connection import NoConnectException

soffice = SofficeHandler()

def test_soffice_connection():
    soffice.start_soffice()
    soffice.connect()
    soffice.kill_soffice()

def test_load_main_file():
    soffice.start_soffice()
    soffice.files.append(("./tests/Unconfigured.ppt"))
    soffice.connect()
    soffice.load_main_file()
    soffice.show_main_slideshow()
    soffice.end_main_slideshow()
    sleep(2)
    soffice.kill_soffice()

def test_soffice_connection_failure():
    with pytest.raises(NoConnectException):
        soffice.connect()