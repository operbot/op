README
######

**NAME**

| ``op`` - object programming
|

**SYNOPSIS**


The ``op`` package provides an Object class, that allows for save/load to/from
json files on disk. Objects can be searched with database functions and uses
read-only files to improve persistence and a type in filename for
reconstruction. Methods are factored out into functions to have a clean
namespace to read JSON data into.

``op`` stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence. Paths carry the
type in the path name what makes reconstruction from filename easier then
reading type from the object.

|

**INSTALL**

| ``pip3 install op --upgrade --force-reinstall``
|

**PROGRAMMING**

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

|

**AUTHOR**

| Bart Thate - operbot100@gmail.com
|

**COPYRIGHT**

| ``op`` is placed in the Public Domain. No Copyright, No License.
|
