# This file is placed in the Public Domain.


"runtime"


import inspect
import os
import queue
import threading
import traceback
import time


from .cls import Class
from .dft import Default
from .obj import Object, register
from .fnc import edit, name
from .thr import launch


Cfg = Default()


def handle(evt):
    evt.parse()
    func = Command.get(evt.cmd)
    if func:
        func(evt)
        evt.show()
    evt.ready()


class Bus(Object):

    objs = []

    @staticmethod
    def add(obj):
        if repr(obj) not in [repr(x) for x in Bus.objs]:
            Bus.objs.append(obj)

    @staticmethod
    def byorig(orig):
        res = None
        for obj in Bus.objs:
            if repr(obj) == orig:
                res = obj
                break
        return res


class Callbacks(Object):

    cbs = {}

    @staticmethod
    def register(typ, cbs):
        if typ not in Callbacks.cbs:
            Callbacks.cbs[typ] = cbs

    @staticmethod
    def callback(event):
        func = Callbacks.cbs.get(event.type)
        if not func:
            event.ready()
            return
        func(event)

    @staticmethod
    def dispatch(event):
        Callbacks.callback(event)

    @staticmethod
    def get(typ):
        return Callbacks.cbs.get(typ)


class Command(Object):

    cmd = {}

    @staticmethod
    def add(cmd):
        Command.cmd[cmd.__name__] = cmd

    @staticmethod
    def get(cmd):
        return Command.cmd.get(cmd)

    @staticmethod
    def remove(cmd):
        del Command.cmd[cmd]


class Event(Object):

    def __init__(self, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        self.__ready__ = threading.Event()
        self.args = []
        self.cmd = ""
        self.orig = ""
        self.result = []
        self.rest = ""
        self.sets = Default()
        self.txt = ""
        self.type = "event"

    def parse(self, txt=None):
        if txt:
            self.txt = txt
        splitted = self.txt.split()
        if splitted:
             self.cmd = splitted[0]
        if len(splitted) > 1:
             self.args = splitted[1:]
             self.rest = " ".join(self.args)
        for word in splitted[1:]:
            try:
                key, value = word.split("=")
                register(self.sets, key, value)
                continue
            except ValueError:
                pass

    def ready(self):
        self.__ready__.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            print(txt)

    def wait(self):
        self.__ready__.wait()


class Handler(Callbacks):

    cmd = Object()

    def __init__(self):
        Callbacks.__init__(self)
        self.queue = queue.Queue()
        self.register("event", handle)
        Bus.add(self)

    def add(self, cmd):
        setattr(self.cmd, cmd.__name__, cmd)
 
    def announce(self, txt):
        pass

    def handle(self, event):
        event.orig = repr(self)
        self.dispatch(event)

    def raw(self, txt):
        pass

    def loop(self):
        while 1:
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def raw(self, txt):
        print(txt)

    def start(self):
        launch(self.loop)

    def wait(self):
        while 1:
            time.sleep(1.0)


class Shell(Handler):

    def poll(self):
        event = Event()
        event.bot = self
        event.txt = input("> ")
        event.orig = repr(self)
        return event

    def raw(self, txt):
        pass

    def start(self):
        launch(self.loop)

    def wait(self):
        while 1:
            time.sleep(1.0)


def from_exception(exc, txt="", sep=" "):
    result = []
    for frm in traceback.extract_tb(exc.__traceback__):
        result.append("%s:%s" % (os.sep.join(frm.filename.split(os.sep)[-2:]), frm.lineno))
    return "%s %s: %s" % (" ".join(result), name(exc), exc, )


def scan(obj, mod):
    for _k, clz in inspect.getmembers(mod, inspect.isclass):
        Class.add(clz)
    for _k, cmd in inspect.getmembers(mod, inspect.isfunction):
        if "event" in cmd.__code__.co_varnames:
            obj.add(cmd)


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
