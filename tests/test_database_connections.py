import pytest

from operatorinstructions.database_handler import DatabaseHandler


db_handler = DatabaseHandler(database='plantfloor')
def test_get_current_recipe_filename():
    assert isinstance(db_handler.get_current_recipe_filename(1, 61), str)

def test_get_all_filenames():
    files = db_handler.get_all_files(4, 42)
    print(files)
    assert type(files) == list
    assert len(files) == 3
    assert files == [
        ("http://ah-plantfloor.marisabae.com/ahdocs/AUBURN%20HILLS%20PRODUCTIO"
            "N%20DOCUMENTS/440%20A%20-%20LINE/2553526%20P552%201703389XXX%20P5"
            "58%20-%20ALT/01%20Operator%20Instructions/%28I-11450%29%20P552%20"
            "2553526%20P558%201703389XXX%20High%20Lock%20Sta%2001.ppt"),
        ("http://ah-plantfloor.marisabae.com/ahdocs/AUBURN%20HILLS%20PRODUCTIO"
            "N%20DOCUMENTS/440%20A%20-%20LINE/2553526%20P552%201703389XXX%20P5"
            "58%20-%20ALT/01%20Operator%20Instructions/%28I-11451%29%20P552%20"
            "2553526%20P558%201703389XXX%20High%20Lock%20Sta%2005.ppt"),
        ("http://ah-plantfloor.marisabae.com/ahdocs/AUBURN%20HILLS%20PRODUCTIO"
            "N%20DOCUMENTS/440%20A%20-%20LINE/2553526%20P552%201703389XXX%20P5"
            "58%20-%20ALT/01%20Operator%20Instructions/%28I-11452%29%20P552%20"
            "2553526%20P558%201703389XXX%20High%20Lock%20Sta%2015.ppt")
    ]

def test_get_missing_current_recipe_filename():
    assert db_handler.get_current_recipe_filename(1, 1) == None

def test_get_current_running_recipe():
    assert isinstance(db_handler.get_current_running_recipe(1), int)

def test_get_missing_current_running_recipe():
    assert db_handler.get_current_running_recipe(2) == None

def test_get_missing_rpi_config():
    assert db_handler.get_rpi_config('gir_test') == None

def test_get_known_rpi_config():
    assert db_handler.get_rpi_config('AH-GIRStation1') == (
        1,
        'AH-GIRStation1',
        '172.17.198.1',
        'GIR test unit',
        False, 1,)

def test_get_rpi_version():
    db_handler.get_rpi_version()