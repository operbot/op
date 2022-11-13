# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"timer"


## import


import unittest


from op import Timer


## define


def test():
    pass


3# class


class TestTimer(unittest.TestCase):

    def testcontructor(self):
        timer = Timer(60, test)
        self.assertEqual(type(timer), Timer)
