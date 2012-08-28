"""tests for the mcfg module"""
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
        # TODO, check that things went right, this would be best done
        # using mock target and editor

    def test_system_ok(self):
        """This is not really a unit test, but more a system test.
        Test a full example
        """
        templatefile = os.path.join(self.test_files_dir, "template2.ini")
        # targets are located in /tmp because we don't know anything
        # about the directory tree of the machine where this test is executed
        mcfgfile = os.path.join(self.test_files_dir, "master2.ini")
        target_ckan = "/tmp/mcfg-test-ckan.ini"
        target_haka = "/tmp/mcfg-test-haka.ini"
        target_cert = "/tmp/mcfg-test-cert.pem"
        testin_ckan = os.path.join(self.test_files_dir, "ckan1.ini")
        testin_haka = os.path.join(self.test_files_dir, "haka1.ini")
        testin_cert = os.path.join(self.test_files_dir, "cert1.pem")
        expected_ckan = os.path.join(self.test_files_dir, "ckan1.expected")
        expected_haka = os.path.join(self.test_files_dir, "haka1.expected")
        input_cert = "/tmp/input.pem"
        shutil.copy(testin_ckan, target_ckan)
        shutil.copy(testin_haka, target_haka)
        shutil.copy(testin_cert, input_cert)
        try:
            os.unlink(target_cert)
        except OSError:
            pass
        testmcfg = mcfg.Mcfg(templatefile, mcfgfile)
        thisincr = 10
        testmcfg.run_editors(thisincr)
        
        result = filecmp.cmp(expected_ckan, target_ckan)
        if result:
            os.unlink(target_ckan)
        else:
            print >> sys.stderr, "incorrect output {0}".format(target_ckan)
        self.assertTrue(result)
        
        backup = "{0}.backup.{1}".format(target_ckan, thisincr)
        result = filecmp.cmp(testin_ckan, backup)
        if result:
            os.unlink(backup)
        else:
            print >> sys.stderr, "incorrect output {0}".format(backup)
        self.assertTrue(result)
        
        result = filecmp.cmp(expected_haka, target_haka)
        if result:
            os.unlink(target_haka)
        else:
            print >> sys.stderr, "incorrect output {0}".format(target_haka)
        self.assertTrue(result)

        backup = "{0}.backup.{1}".format(target_haka, thisincr)
        result = filecmp.cmp(testin_haka, backup)
        if result:
            os.unlink(backup)
        else:
            print >> sys.stderr, "incorrect output {0}".format(backup)
        self.assertTrue(result)
        
        self.assertTrue(filecmp.cmp(testin_cert, target_cert))
        os.unlink(target_cert)
        os.unlink(input_cert)


        


if __name__ == '__main__':
    unittest.main()
