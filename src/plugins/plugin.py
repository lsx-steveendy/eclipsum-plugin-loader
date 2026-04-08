import os


class Plugin:
    def __init__(self, abspath: str):
        @property
        def path(self):
            return abspath
        
        @property
        def filename(self):
            return os.path.basename(abspath)
        

