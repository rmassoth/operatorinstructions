import pytest
from database_handler import DatabaseHandler


db_handler = DatabaseHandler(database='plantfloor')
def test_get_current_recipe_filename():
    assert isinstance(db_handler.get_current_recipe_filename(1, 61), str)

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