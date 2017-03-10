import pytest
import os
from file_handler import FileHandler
from urllib.error import HTTPError, URLError

file_handler = FileHandler()
filename = "temp_file"

def setup_function():
    with open(filename, 'w') as f:
        pass

def teardown_function():
    os.remove(filename)

def test_local_file_check():
    with pytest.raises(TypeError):
        file_handler.check_for_local_file()

def test_local_file_check_file_exists(tmpdir):
    assert file_handler.check_for_local_file(filename)

def test_local_file_check_missing_file():
    assert not file_handler.check_for_local_file('Nothing')

def test_network_file_getter():
    url = "http://ah-plantfloor.marisabae.com/ahdocs/AUBURN HILLS PRODUCTION DOCUMENTS/484 - LINE/283362/01 Operator Instructions/(I-11100) 283362 Final Inspection.ppt"
    file_handler.get_file_from_network(url, "temp.ppt")

def test_network_file_missing():
    url = 'http://ah-plantfloor.marisabae.com/doesntexist/'
    with pytest.raises(HTTPError) as HTTPError_info:
        file_handler.get_file_from_network(url, "temp.ppt")

def test_network_file_bad_url():
    url = 'http://doesntexist.marisabae.com/doesntexist/'
    with pytest.raises(URLError) as URLError_info:
        file_handler.get_file_from_network(url, "temp.ppt")

def test_receive_file():
    file_handler.receive_file_from_socket()