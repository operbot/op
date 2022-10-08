# This file is placed in the Public Domain.


"runtime"


import inspect
import os
import threading
import traceback


from .cls import Class
from .obj import Object
from .fnc import name


class Event(Object):

    def __init__(self, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        self.__ready__ = threading.Event()
        self.args = []
        self.bot = None
        self.result = []
        self.rest = ""
        self.txt = ""

    def parse(self, txt=None):
        if txt:
            self.txt = txt
        splitted = self.txt.split()
        if splitted:
             self.cmd = splitted[0]
        if len(splitted) > 1:
             self.args = splitted[1:]
             self.rest = " ".join(self.args)

    def ready(self):
        self.__ready__.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            print(txt)

    def wait(self):
        self.__ready__.wait()


class Handler(Object):

    cmd = Object()

    @staticmethod
    def announce(txt):
        pass

    @staticmethod
    def handle(event):
        event.parse()
        try:
            func = getattr(Handler.cmd, event.cmd)
        except AttributeError:
            func = None
        if func:
            func(event)
            event.show()
        event.ready()

    @staticmethod
    def raw(txt):
        print(txt)

    @staticmethod
    def register(cmd):
        setattr(Handler.cmd, cmd.__name__, cmd)

    @staticmethod
    def scan(mod):
        for _k, clz in inspect.getmembers(mod, inspect.isclass):
            Class.add(clz)
        for _k, cmd in inspect.getmembers(mod, inspect.isfunction):
            if "event" in cmd.__code__.co_varnames:
                Handler.register(cmd)


def from_exception(exc, txt="", sep=" "):
    result = []
    for frm in traceback.extract_tb(exc.__traceback__):
        result.append("%s:%s" % (os.sep.join(frm.filename.split(os.sep)[-2:]), frm.lineno))
    return "%s %s: %s" % (" ".join(result), name(exc), exc, )


def scan(mod):
    for _k, clz in inspect.getmembers(mod, inspect.isclass):
        Class.add(clz)
    for _k, cmd in inspect.getmembers(mod, inspect.isfunction):
        if "event" in cmd.__code__.co_varnames:
            Handler.register(cmd)

def scandir(path, func):
    res = []
    if not os.path.exists(path):
        return res
    for _fn in os.listdir(path):
        if _fn.endswith("~") or _fn.startswith("__"):
            continue
        try:
            pname = _fn.split(os.sep)[-2]
        except IndexError:
            pname = path
        mname = _fn.split(os.sep)[-1][:-3]
        res.append(func(pname, mname))
    return res
