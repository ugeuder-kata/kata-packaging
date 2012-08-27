"""tests for the mcfg module"""
import datetime
import filecmp
import os
import shutil
import sys
import unittest

# we live in subdirectory test, so we need to import the code to be tested
# from the parent directory. I don't like this hack, please suggest something
# better (well, nose does it already, but maybe not everybody uses it)
here = os.path.split(__file__)[0]
if here == '' :
    here = os.getcwd()
above = os.path.split(here)[0]
hacked_path = [above]
hacked_path.extend(sys.path)
sys.path = hacked_path

import mcfg

class TestMcfg(unittest.TestCase):
    """test the mcfg class"""

    def setUp(self):
        """unittest.TestCase.setUp makes pylint cry"""
        # make this independent of the cwd, always relative to our code
        self.test_files_dir = os.path.join(here, "files")

    def test_parsevalue_good(self):
        """test a good value"""
        (incr, param) = mcfg.Mcfg.parsevalue("27 foo")
        self.assertEqual(27, incr)
        self.assertEqual("foo", param) 

    def test_parsevalue_no_space(self):
        """test a value that contains no space"""
        testvalue = "27foo"
        self.assertRaises(ValueError, mcfg.Mcfg.parsevalue, testvalue)
        # in Python 2.7 we could have used assertRaises as context manager,
        # in the first place, but we need to support Python 2.6
        # (of course this could be coded differently using try, but the
        # assertRaises conveys the idea what we are doing)
        try:
            mcfg.Mcfg.parsevalue(testvalue)
        except ValueError as exc:
            self.assertEqual( "Increment value must be separated from " 
                  "editor name by space: {0}".format(testvalue), str(exc))


    def test_parsevalue_no_int(self):
        """ test a value that has no valid integer before the space"""
        testvalue = "foo bar"
        self.assertRaises(ValueError, mcfg.Mcfg.parsevalue, testvalue)
        # see comment about Python 2.7 above
        try:
            mcfg.Mcfg.parsevalue(testvalue)
        except ValueError as exc:
            self.assertEqual( "Increment value must numeric: >>>foo<<< bar", 
                             str(exc))


    def test_init(self):
        """test that the constructor reads the ini files correctly"""
        templatefile = os.path.join(self.test_files_dir, "template1.ini")
        mcfgfile = os.path.join(self.test_files_dir, "master1.ini")
        mcfg.Mcfg(templatefile, mcfgfile)


if __name__ == '__main__':
    unittest.main()
