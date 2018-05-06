# tests
# Testing for the lifoid module
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis

"""
Testing for the lifoid module
"""

import unittest


class InitializationTest(unittest.TestCase):
    def test_import(self):
        """
        Can import lifoid
        """
        try:
            import lifoid
        except ImportError:
            self.fail("Unable to import the lifoid module!")

    def test_version(self):
        """
        Assert that the version function works
        """
        import lifoid.version
        lifoid.version.__version__ = {
            'major': 0,
            'minor': 1,
            'micro': 0,
            'releaselevel': 'alpha',
            'serial': 0,
        }
        self.assertEqual(lifoid.version.get_version(), '0.1a0')


if __name__ == '__main__':
    unittest.main()
