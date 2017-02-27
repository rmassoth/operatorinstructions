import pytest
from soffice_handler import SofficeHandler


def test_soffice_started():
    soffice = SofficeHandler()
    assert soffice.start_soffice() > 0