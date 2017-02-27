import subprocess
import os
import sys

# add necessary environment variable for pyuno if it doesn't already exist
sys.path.append('/usr/lib/libreoffice/program')
if getattr(os.environ, 'URE_BOOTSTRAP', None) is None:
     os.environ['URE_BOOTSTRAP'] = "vnd.sun.star.pathname:/usr/lib/libreoffice/program/fundamentalrc"
import uno

class SofficeHandler():
    """Class to handle all libreoffice(soffice) related functions."""

    def __init__(self):
        sub = None
        self.pid = None

    def __del__(self):
        sub.wait()


    def start_soffice(self):
        try:
            sub = subprocess.Popen(args=["/usr/bin/soffice", "--impress", "--accept=socket,host=localhost,port=2002;urp;StarOffice.ServiceManager", "--norestore", "--nolockcheck"])
            self.pid = sub.pid
            return self.pid
        except Exception as e:
            print(e)
            return 0
