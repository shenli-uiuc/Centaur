import TwitterData
import pickle

class SimpleDataStore:
    filename = None
    pickleData = None
    fHandle = None

    def __init__(self, filename):
        self.filename = filename
        if overwrite:
            self.fHandle = open(filename, 'w')
        else:
            self.fHandle = open()
