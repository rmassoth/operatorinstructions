import subprocess
import os
import sys
import pathlib
from subprocess import TimeoutExpired
from time import sleep

# add necessary environment variable for pyuno if it doesn't already exist
sys.path.append('/usr/lib/libreoffice/program')
if getattr(os.environ, 'URE_BOOTSTRAP', None) is None:
     os.environ['URE_BOOTSTRAP'] = "vnd.sun.star.pathname:/usr/lib/libreoffice/program/fundamentalrc"
import uno

class SofficeHandler():
    """Class to handle all libreoffice(soffice) related functions."""

    def __init__(self):
        self.sub = None         # subprocess of soffice
        self.local_context = uno.getComponentContext() # get the uno component context from the PyUNO runtime
        # create the UnoUrlResolver
        self.resolver = self.local_context.ServiceManager.createInstanceWithContext(
                            "com.sun.star.bridge.UnoUrlResolver", self.local_context )
        self.remote_context = None
        self.smgr = None
        self.desktop = None
        self.files = []
        self.main_frame = None
        self.presentation = None

    """Clean up after killing the object."""
    def __del__(self):
        try:
            self.kill_soffice()
        except Exception as e:
            print(e)

    """Start a new soffice process and listen on port 2002."""
    def start_soffice(self):
        try:
            self.sub = subprocess.Popen(args=["/usr/bin/soffice", "--impress", "--accept=socket,host=localhost,port=2002;urp;StarOffice.ServiceManager", "--norestore", "--nolockcheck"])
            return self.sub.pid
        except Exception as e:
            print(e)

    """Terminate the soffice process."""
    def kill_soffice(self):
        try:
            self.sub.terminate()
            while not self.sub.wait(timeout=10):
                pass
        except TimeoutExpired:
            try:
                self.sub.kill()
            except Exception as kill_exc:
                print(kill_exc)
        except Exception as e:
            print(e)

    """Connect to the soffice process listening on port 2002."""
    def connect(self):
        try:
            tries=0
            while tries<10:
                try:
                    # connect to the running office
                    self.remote_context = self.resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
                    break
                except Exception:
                    pass
                tries+=1
                sleep(1) # pause if no connection was made
            self.smgr = self.remote_context.ServiceManager
            # get the central desktop object
            self.desktop = self.smgr.createInstanceWithContext( "com.sun.star.frame.Desktop", self.remote_context)
        except Exception as e:
            print(e)

    """Load the file from the first position in the files list."""
    def load_main_file(self):
        try:
            url = pathlib.Path(os.getcwd(), self.files[0]).as_uri() # get file in current directory, this could be better like an absolute path or a link on the website.
            self.main_frame = self.desktop.loadComponentFromURL(url, "_default", 0, ())
            self.presentation = self.main_frame.getPresentation()
        except Exception as e:
            print(e)

    """Start the main slideshow."""
    def show_main_slideshow(self):
        try:
            self.presentation.start()
        except Exception as e:
            print(e)

    """End the main slideshow."""
    def end_main_slideshow(self):
        try:
            self.presentation.end()
        except Exception as e:
            print(e)