"""

This module provides a class to abstract managing the operator instruction
files themselves.
"""

import glob
from urllib.request import Request, urlopen
import urllib.parse

class FileHandler():
    """

    Handles checking if local files exists for the current running recipe.
    Also gets files from the network when they are updated or don't exist
    in the local directory.
    """

    def __init__(self):
        pass

    def check_for_local_file(self, filename=None):
        """

        Checks if a local file exists with the filename given.
        Returns True if it exists, False if not.
        """
        files = glob.glob(filename)
        return bool(files)

    def get_file_from_network(self, url, filename):
        """

        Gets the file from the url specified and saves it to the local
        directory with the filename given.
        """
        encoded_url = urllib.parse.quote(url, safe='/:')
        req = Request(encoded_url)
        response = urlopen(req)
        with open(filename, 'wb') as return_file:
            return_file.write(response.read())

    def receive_file_from_socket(self):
        """

        Receives a file over a socket connection and saves it to the local
        directory.
        """
        pass
