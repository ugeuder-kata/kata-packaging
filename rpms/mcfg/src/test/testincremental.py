"""Unit test the incremental task, no other classes used"""

import mock
import os
import sys
import unittest

# we live in subdirectory test, so we need to import the code to be tested
# from the parent directory. I don't like this hack, please suggest something
# better (well, nose does it already, but maybe not everybody uses it)
here = os.path.split( __file__ )[0]
if here == '' :
    here = os.getcwd()
above = os.path.split( here )[0]
hackedPath = [ above ]
hackedPath.extend( sys.path )
sys.path = hackedPath

import incremental

class TestIncremental(unittest.TestCase):
    """Unit test the incremental task, no other classes used"""

    def test_construct_and_convert(self):
        """Just construct it and convert to int"""
        inc = incremental.Incremental(7)
        self.assertEqual(7, int(inc))
        os.unlink(incremental.Incremental.get_stat_file_name())

    def test_status_file(self):
        """Test that the last increment is kept correctly
        black box testing as far as file contents is concerned
        """
        filename = incremental.Incremental.get_stat_file_name()
        try:
            os.unlink(filename)
        except OSError:
            pass
        inc = incremental.Incremental(7)
        self.assertEqual(-1, inc.lastincr)
        inc = incremental.Incremental(8)
        self.assertEqual(7, inc.lastincr)
        inc = incremental.Incremental(8)
        # twice the same is not an increment!
        self.assertEqual(-1, inc.lastincr)
        os.unlink(filename)

    def test_is_current(self):
        """Test the is_current method. Depends on correct status file
        operation.
        """
        filename = incremental.Incremental.get_stat_file_name()
        try:
            os.unlink(filename)
        except OSError:
            pass
        inc = incremental.Incremental(7)
        self.assertTrue(inc.is_current(0))
        self.assertTrue(inc.is_current(6))
        self.assertTrue(inc.is_current(7))
        self.assertFalse(inc.is_current(8))
        inc = incremental.Incremental(10)
        self.assertFalse(inc.is_current(7))
        self.assertTrue(inc.is_current(8))
        self.assertTrue(inc.is_current(9))
        self.assertTrue(inc.is_current(10))
        self.assertFalse(inc.is_current(11))

        # also test a non-integer
        action = mock.Mock()
        action.__int__ = mock.Mock()         # magic method needs to be
                                             # explicitly assigned
        action.__int__.return_value = 10
        self.assertTrue(inc.is_current(action))
        action.__int__.return_value = 11
        self.assertFalse(inc.is_current(action))
        os.unlink(filename)


if __name__ == '__main__':
    unittest.main()
