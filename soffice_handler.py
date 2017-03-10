"""

Module that wraps starting, killing, and showing a libreoffice connection into
an easy to use object with method calls.
"""
import subprocess
from subprocess import TimeoutExpired
import os
import sys
import pathlib
from time import sleep

# add necessary environment variable for pyuno if it doesn't already exist
sys.path.append('/usr/lib/libreoffice/program')
if getattr(os.environ, 'URE_BOOTSTRAP', None) is None:
    os.environ['URE_BOOTSTRAP'] = ("vnd.sun.star.pathname:/usr/lib/"
                                   "libreoffice/program/fundamentalrc")
import pyuno
import uno
from com.sun.star.beans import PropertyValue, UnknownPropertyException
from com.sun.star.uno import (RuntimeException)
from com.sun.star.connection import NoConnectException

class SofficeHandler():
    """Class to handle all libreoffice(soffice) related functions."""

    def __init__(self):
        # pointer to the soffice subprocess
        self.sub = None
        # get the uno component context from the PyUNO runtime
        self.local_context = uno.getComponentContext()
        # create the UnoUrlResolver
        self.resolver = (
            self.local_context.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", self.local_context))
        self.remote_context = None
        self.smgr = None
        self.desktop = None
        self.files = []
        self.main_frame = None
        self.presentation = None

    def __del__(self):
        """Clean up after killing the object."""
        #self.kill_soffice()

    def start_soffice(self):
        """Start a new soffice process and listen on port 2002."""
        self.sub = subprocess.Popen(
            args=[
                "/usr/bin/soffice",
                "--impress",
                "--accept=socket,host=localhost,"
                "port=2002;urp;StarOffice.ServiceManager",
                "--norestore",
                "--nolockcheck"])
        return self.sub.pid

    def kill_soffice(self):
        """Terminate the soffice process."""
        try:
            self.sub.terminate()
            while not self.sub.wait(timeout=10):
                pass
        except TimeoutExpired:
            self.sub.kill()

    def connect(self):
        """Connect to the soffice process listening on port 2002."""
        tries = 0
        while tries < 10:
            try:
                # connect to the running office
                self.remote_context = self.resolver.resolve(
                    "uno:socket,host=localhost,port=2002;"
                    "urp;StarOffice.ComponentContext")
                break
            except NoConnectException:
                pass
            tries += 1
            # pause if no connection was made
            sleep(1)
        if tries >= 10:
            raise NoConnectException
        self.smgr = self.remote_context.ServiceManager
        # get the central desktop object
        self.desktop = self.smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.remote_context)

    def load_main_file(self):
        """Load the file from the first position in the files list."""
        # get file in current directory
        url = pathlib.Path(os.getcwd(), self.files[0]).as_uri()
        self.main_frame = self.desktop.loadComponentFromURL(
            url, "_default", 0, ())
        self.presentation = self.main_frame.getPresentation()

    def show_main_slideshow(self):
        """Start the main slideshow."""
        self.presentation.start()

    def end_main_slideshow(self):
        """End the main slideshow."""
        self.presentation.end()
