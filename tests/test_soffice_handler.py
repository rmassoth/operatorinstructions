import pytest
from soffice_handler import SofficeHandler

soffice = SofficeHandler()
def test_start_soffice():
    assert soffice.start_soffice() != False

def test_kill_soffice():
    assert soffice.kill_soffice() == True