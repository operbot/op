# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"command tests"


import unittest


from op import Cfg, Command, Event, Handler, Object


events = []
skip = ["cfg",]


param = Object()
param.cmd = [""]
param.cfg = ["nick=bot", "server=localhost", "port=6699"]
param.fnd = ["log", "log txt==test", "config", "config name=bot", "config server==localhost"]
param.flt = ["0", ""]
param.log = ["test1", "test2"]
param.mre = [""]
param.thr = [""]


class CLI(Handler):

    def raw(self, txt):
        if Cfg.verbose:
            print(txt)


def getmain(name):
    main = __import__("__main__")
    return getattr(main, name, None)


def consume(evt):
    fixed = []
    for _e in evt:
        _e.wait()
        fixed.append(_e)
    for fix in fixed:
        try:
            evt.remove(fix)
        except ValueError:
            continue


class TestCommands(unittest.TestCase):

    def test_commands(self):
        cli = CLI()
        cmds = sorted(Command.cmd)
        for cmd in cmds:
            if cmd in skip:
                continue
            for ex in getattr(param, cmd, ""):
                evt = Event()
                evt.channel = "#bot"
                evt.orig = repr(cli)
                txt = cmd + " " + ex
                evt.txt = txt.strip()
                cli.handle(evt)
                events.append(evt)
        consume(events)
        self.assertTrue(not events)
