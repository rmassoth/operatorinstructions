import pytest
from soffice_handler import SofficeHandler
from time import sleep

soffice = SofficeHandler()

def test_soffice_connection():
    soffice.start_soffice()
    assert soffice.connect_to_soffice() == True
    soffice.kill_soffice()

def test_load_main_file():
    soffice.start_soffice()
    soffice.files.append(("Unconfigured.ppt"))
    soffice.connect_to_soffice()
    assert soffice.load_main_file() == True
    assert soffice.show_main_slideshow() == True
    assert soffice.end_main_slideshow() == True
    sleep(2)
    soffice.kill_soffice()