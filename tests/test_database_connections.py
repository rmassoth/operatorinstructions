import pytest
from database_handler import DatabaseHandler


db_handler = DatabaseHandler(database='plantfloor')
def test_get_current_recipe_filename():
    db_handler.get_current_recipe_filename(1, 1)


def test_get_current_running_recipe():
    db_handler.get_current_running_recipe(1)


def test_get_missing_rpi_config():
    assert db_handler.get_rpi_config('gir_test') == None

def test_get_known_rpi_config():
    assert db_handler.get_rpi_config('AH-GIRStation1') == (1, 'AH-GIRStation1', '172.17.198.1', 'GIR test unit', False, 1, )

def test_get_rpi_version():
    db_handler.get_rpi_version()