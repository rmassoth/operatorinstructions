import os
import glob
from urllib.request import Request, urlopen
import urllib.parse

class FileHandler():

    def __init__(self):
        pass
        
    def check_for_local_file(self, filename=None):
        try:
            files = glob.glob(filename)
            if files != []:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def get_file_from_network(self, url, filename):
        encoded_url = urllib.parse.quote(url, safe='/:')
        req = Request(encoded_url)
        response = urlopen(req)
        with open(filename, 'wb') as return_file:
            return_file.write(response.read())

    def receive_file_from_socket(self):
        pass