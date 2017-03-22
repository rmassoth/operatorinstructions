import pytest

from operatorinstructions.soffice_handler import SofficeHandler

soffice = SofficeHandler()
def test_start_soffice():
    soffice.start_soffice()

def test_kill_soffice():
    soffice.kill_soffice()