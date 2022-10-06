# This file is placed in the Public Domain.
# pylint: disable=R,C

"""object programming 


The ``op`` package provides an Object class, that mimics a dict while using
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction. Methods are
factored out into functions to have a clean namespace to read JSON data into.

basic usage is this::

>>> import op
>>> o = op.Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> from op import Object, load, save
>>> o = Object()
>>> o.key = "value"
>>> p = save(o)
>>> obj = Object()
>>> load(obj, p)
>>> obj.key
>>> 'value'

great for giving objects peristence by having their state stored in files::

 >>> from op import Object, save
 >>> o = Object()
 >>> save(o)
 'op.obj.Object/2021-08-31/15:31:05.717063'

"""


from .thr import Thread, launch
from .cls import Class
from .dbs import Db, allobj, find, fns, fntime, hook, last, locked
from .dft import Default
from .jsn import ObjectDecoder, ObjectEncoder, dump, dumps, load, loads, save
from .obj import *
from .utl import cdir, elapsed, spl
from .wdr import Wd


def __dir__():
    return (
            'Class',
            'Db',
            'Default',
            'Object',
            'ObjectDecoder',
            'ObjectEncoder',
            'Thread',
            'Wd',
            'allobj',
            'delete',
            'dump',
            'dumps',
            'edit',
            'find',
            'format',
            'get',
            'items',
            'keys',
            'launch',
            'last',
            'load',
            'loads',
            'locked',
            'name',
            'otype',
            'register',
            'save',
            'spl',
            'update',
            'values',
           )
