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
import uno
from com.sun.star.connection import NoConnectException
from com.sun.star.lang import IllegalArgumentException

class SofficeHandler():
    """Class to handle all libreoffice(soffice) related functions."""
    # pointer to the soffice subprocess
    sub = None
    remote_context = None
    smgr = None
    desktop = None
    files = []
    main_frame = None
    presentation = None
    local_context = None
    resolver = None

    def __del__(self):
        """Clean up after killing the object."""
        try:
            if self.sub:
                output, errs = self.sub.communicate(timeout=1)
        except TimeoutExpired:
            self.kill_soffice()

    def start_soffice(self):
        """Start a new soffice process and listen on port 2002."""
        if self.sub:
            return_code = self.sub.poll()
            if return_code:
                self.sub.wait()
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
            #self.close_soffice()
            self.desktop = None
            self.smgr = None
            self.remote_context = None
            self.resolver = None
            self.local_context = None
            # kill the soffice process itself
            self.sub.terminate()
            while not self.sub.wait(timeout=10):
                pass
        except TimeoutExpired:
            self.sub.kill()

    def connect(self):
        """Connect to the soffice process listening on port 2002."""
        if self.sub:
            return_code = self.sub.poll()
            if return_code:
                self.sub.wait()
        tries = 0
        while tries < 10:
            try:
                 # get the uno component context from the PyUNO runtime
                self.local_context = uno.getComponentContext()
                # create the UnoUrlResolver
                self.resolver = (
                    self.local_context.ServiceManager.createInstanceWithContext
                    ("com.sun.star.bridge.UnoUrlResolver", self.local_context))
                # connect to the running office
                self.remote_context = self.resolver.resolve(
                    "uno:socket,host=localhost,port=2002;"
                    "urp;StarOffice.ComponentContext")
                break
            except NoConnectException:
                pass
            tries += 1
            # pause if no connection was made
            sleep(3)
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
        try:
            self.main_frame = self.desktop.loadComponentFromURL(
                url, "_default", 0, ())
            self.presentation = self.main_frame.getPresentation()
        except IllegalArgumentException:
            raise

    def load_main_file_from_network(self):
        """Load the file from the first position in the files list."""
        # get file in current directory
        url = self.files[0]
        try:
            self.main_frame = self.desktop.loadComponentFromURL(
                url, "_default", 0, ())
            self.presentation = self.main_frame.getPresentation()
            return True
        except IllegalArgumentException:
            return False

    def show_main_slideshow(self):
        """Start the main slideshow."""
        self.presentation.start()

    def end_main_slideshow(self):
        """End the main slideshow."""
        self.presentation.end()

    def close_soffice(self):
        """Close the frame and desktop but don't kill the process."""
        # close impress frame
        if self.main_frame:
            self.main_frame.close(True)
        # close desktop frame
        if self.desktop:
            self.desktop.terminate()

    def load_file(index):
        """Load the file from the index position in the files list."""
        # get file in current directory
        url = pathlib.Path(os.getcwd(), self.files[0]).as_uri()
        self.main_frame = self.desktop.loadComponentFromURL(
            url, "_default", 0, ())
        self.presentation = self.main_frame.getPresentation()

    def load_network_file(index):
        """Load the file from the index position in the files list."""
        # get file in current directory
        url = pathlib.Path(os.getcwd(), self.files[0]).as_uri()
        self.main_frame = self.desktop.loadComponentFromURL(
            url, "_default", 0, ())
        self.presentation = self.main_frame.getPresentation()