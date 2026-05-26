import pickle as pi
from file_directories import *
from Miscellaneous import *


class savedata(object):
    def __init__(self, filename):
        self.fn = filename
        self.dic = dict()

    def exists(self, what):
        return what in self.dic

    def add(self, item, value):
        self.dic[item] = value

    def read(self, item):
        if self.exists(item) == False:
            return
        else:
            return self.dic[item]

    def readn(self, item):
        if self.exists(item) == False:
            return
        else:
            return int(self.dic[item])
    def readf(self, item):
        if self.exists(item) == False:
            return
        else:
            return float(self.dic[item])


    def save(self):
        pd = pi.dumps(self.dic)
        file_put_contents(self.fn, pd, "wb")

    def load(self):
        if file_exists(self.fn) == False:
            return ""
        try:
            self.dic = pi.loads(file_get_contents(self.fn, "rb"))
        except:
            return ""
 