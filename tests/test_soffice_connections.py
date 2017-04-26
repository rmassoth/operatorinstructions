from time import sleep

import pytest

from operatorinstructions.soffice_handler import SofficeHandler
from com.sun.star.connection import NoConnectException




soffice = SofficeHandler()
soffice.files.append("")

def test_soffice_connection():
    soffice.start_soffice()
    soffice.connect()
    soffice.kill_soffice()
    # pausing after killing due to port still being open shortly after killing
    # if you try to connect again too soon it throws errors.
    sleep(3)

def test_load_main_file():
    soffice.start_soffice()
    soffice.files[0] = ("tests/Unconfigured.ppt")
    soffice.connect()
    soffice.load_main_file()
    soffice.kill_soffice()
    # pausing again
    sleep(3)

def test_load_main_file_from_network():
    soffice.start_soffice()
    soffice.files[0] = ("http://ah-plantfloor.marisabae.com/media/"
        "operatorinstructions/Unconfigured.pptx")
    soffice.connect()
    assert soffice.load_main_file_from_network()
    soffice.kill_soffice()
    # pausing again
    sleep(3)

def test_load_main_file_from_network_url_unencoded():
    soffice.start_soffice()
    soffice.files[0] = ("http://ah-plantfloor.marisabae.com/ahdocs/AUBURN "
        "HILLS PRODUCTION DOCUMENTS/484 - LINE/283362/01 Operator Instructions"
        "/(I-11100) 283362 Final Inspection.ppt")
    soffice.connect()
    assert soffice.load_main_file_from_network()
    soffice.kill_soffice()
    # pausing again
    sleep(3)

def test_load_main_file_from_network_url_encoded():
    soffice.start_soffice()
    soffice.files[0] = ("http://ah-plantfloor.marisabae.com/ahdocs/AUBURN%20H"
        "ILLS%20PRODUCTION%20DOCUMENTS/440%20A%20-%20LINE/2553526%20P552%20170"
        "3389XXX%20P558%20-%20ALT/01%20Operator%20Instructions/%28I-11450%29%2"
        "0P552%202553526%20P558%201703389XXX%20High%20Lock%20Sta%2001.ppt")
    soffice.connect()
    assert soffice.load_main_file_from_network()
    soffice.kill_soffice()
    # pausing again
    sleep(3)

def test_load_main_file_from_network_missing():
    soffice.start_soffice()
    soffice.files[0] = ("http://ah-plantfloor.marisabae.com/ahdocs/AUBURN%20H"
        "ILLS%20PRODUCTION%20DOCUMENTS/4%20A%20-%20LINE/2553526%20P552%20170"
        "3389XXX%20P558%20-%20ALT/01%20Operator%20Instructions/%28I-11450%29%2"
        "0P552%202553526%20P558%201703389XXX%20High%20Lock%20Sta%2001.ppt")
    soffice.connect()
    assert not soffice.load_main_file_from_network()
    soffice.kill_soffice()
    # pausing again
    sleep(3)

def test_load_all_files_from_network():
    soffice.start_soffice()
    soffice.files = [
        ("http://ah-plantfloor.marisabae.com/media/operatorinstructions/"
            "Unconfigured.pptx"),
        ("http://ah-plantfloor.marisabae.com/ahdocs/AUBURN%20HILLS%20PRODUCTIO"
            "N%20DOCUMENTS/440%20A%20-%20LINE/2553526%20P552%201703389XXX%20P5"
            "58%20-%20ALT/01%20Operator%20Instructions/%28I-11450%29%20P552%20"
            "2553526%20P558%201703389XXX%20High%20Lock%20Sta%2001.ppt")
    ]
    soffice.connect()
    assert soffice.load_files_from_network()
    soffice.kill_soffice()
    # pausing again
    sleep(3)

def test_multiple_slideshows():
    soffice.start_soffice()
    soffice.files = [
        ("http://ah-plantfloor.marisabae.com/media/operatorinstructions/"
            "Unconfigured.pptx"),
        ("http://ah-plantfloor.marisabae.com/ahdocs/AUBURN%20HILLS%20PRODUCTIO"
            "N%20DOCUMENTS/440%20A%20-%20LINE/2553526%20P552%201703389XXX%20P5"
            "58%20-%20ALT/01%20Operator%20Instructions/%28I-11450%29%20P552%20"
            "2553526%20P558%201703389XXX%20High%20Lock%20Sta%2001.ppt")
    ]
    soffice.connect()
    assert soffice.load_files_from_network()
    soffice.show_slideshow(0)
    soffice.end_slideshow()
    sleep(5)
    soffice.show_slideshow(1)
    soffice.end_slideshow()
    sleep(5)
    soffice.kill_soffice()
    # pausing again
    sleep(3)

def test_soffice_connection_failure():
    with pytest.raises(NoConnectException):
        soffice.connect()
