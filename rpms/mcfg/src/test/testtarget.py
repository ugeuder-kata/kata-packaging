"""tests for the target module"""
import datetime
import filecmp
import mock
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

import editor
import target

class TestTarget(unittest.TestCase):
    """test the target class"""

    def setUp(self):
        """unittest.TestCase.setUp makes pylint cry"""
        # make this independent of the cwd, always relative to our code
        self.test_files_dir = os.path.join(here, "files")

    def test_empty_edlist(self):
        """empty edlist is the trivial case"""
        samplefile = os.path.join(self.test_files_dir, "replace1.in" )
        targetfile = os.path.join(self.test_files_dir, "emptyEdlist.out-"
                                        + datetime.datetime.now().isoformat())
        shutil.copy(samplefile, targetfile)
        tgt = target.Target()
        tgt.targetfile = targetfile
        incr = mock.Mock()
        incr.is_current.return_value = True
        tgt.run_editors(incr)
        self.assertTrue(filecmp.cmp(samplefile, targetfile))
        os.unlink(targetfile)

    def test_contradicting_backup(self):
        """Exception must be raised if editor with contradicting backup
        policy on same target
        """
        tgt = target.Target()
        tgt.targetfile = "contradictive"
        tgt.edlist.append(editor.Editor("replace", 10, ("foo", "bar")))
        tgt.edlist.append(editor.Editor("copy_file", 10,
                                        ("location", "inputFile")))
        self.assertRaises(ValueError, tgt.backup)
        # in Python 2.7 we could have used assertRaises as context manager,
        # in the first place, but we need to support Python 2.6
        # (of course this could be coded differently using try, but the
        # assertRaises conveys the idea what we are doing)
        try:
            tgt.backup()
        except ValueError as exc:
            self.assertEqual( "Editors with incompatible backup policy for " \
                             "contradictive", str(exc))

    def test_one_replacement(self):
        """Test a target with a single replacement editor
        Before the test execution we copy the target file from a sample each
        time. Target will be removed on successful test execution. On
        failure it will be kept for debugging and overwritten on next test
        execution (no checks)
        """
        sample = os.path.join(self.test_files_dir, "one_replacement.sample")
        targetfile = os.path.join(self.test_files_dir, "one_replacement.conf")
        expected = os.path.join(self.test_files_dir,
                                "one_replacement.expected")
        thisincr = 10
        backupfile = "{0}.backup.{1}".format(targetfile, thisincr)
        shutil.copy(sample, targetfile)
        tgt = target.Target()
        tgt.targetfile = targetfile
        tgt.edlist.append(editor.Editor("replace", 10,
                                        ("email", "admin@here.org")))
        thisincr = mock.Mock()
        thisincr.is_current.return_value = True
        thisincr.__int__ = mock.Mock()
        thisincr.__int__.return_value = 10
        tgt.run_editors(thisincr)
        result = filecmp.cmp(targetfile, expected)
        self.assertTrue(result)
        if not result:
            print >> sys.stderr, "Failed result in {}".format(targetfile)
        else:
            os.unlink(targetfile)
        self.assertTrue(filecmp.cmp(backupfile, sample))
        os.unlink(backupfile)


    def test_two_replacements(self):
        """Test a target with a two replacement editors
        Basically copied from test_one_replacement, did not bother to factor
        out common code.
        """
        sample = os.path.join(self.test_files_dir, "two_replacements.sample")
        targetfile = os.path.join(self.test_files_dir, "two_replacements.conf")
        expected = os.path.join(self.test_files_dir,
                                "two_replacements.expected")
        thisincr = mock.Mock()
        thisincr.is_current.return_value = True
        thisincr.__int__ = mock.Mock()
        thisincr.__int__.return_value = 22
        backupfile = "{0}.backup.{1}".format(targetfile, int(thisincr))
        shutil.copy(sample, targetfile)
        tgt = target.Target()
        tgt.targetfile = targetfile
        tgt.edlist.append(editor.Editor("replace", 22,
                                        ("email", "postmaster@here.org")))
        tgt.edlist.append(editor.Editor("replace", 22,
                                        ("myip", "1.2.3.4")))
        tgt.run_editors(thisincr)
        result = filecmp.cmp(targetfile, expected)
        self.assertTrue(result)
        if not result:
            print >> sys.stderr, "Failed result in {}".format(targetfile)
        else:
            os.unlink(targetfile)
        self.assertTrue(filecmp.cmp(backupfile, sample))
        os.unlink(backupfile)


    def test_copy_file_exists(self):
        """Make sure and editor with backup = False fails if the target
        file exists already before.
        """
        # Just reuse some files from before.
        infile = os.path.join(self.test_files_dir, "two_replacements.sample")
        targetfile = os.path.join(self.test_files_dir,
                                  "two_replacements.expected")
        thisincr = mock.Mock()
        tgt = target.Target()
        tgt.targetfile = targetfile
        tgt.edlist.append(editor.Editor("copy_file", thisincr,
                                                      ("location", infile)))
        self.assertRaises(IOError, tgt.run_editors, thisincr)
        # see comment about Python 2.7 above
        try:
            tgt.run_editors(thisincr)
        except IOError as exc:
            self.assertEqual("Target file {0} already "
                              "exists".format(targetfile), str(exc))

    def test_replacement_input_missing(self):
        """Call a replacement editor without the target existing"""
        targetfile = os.path.join(self.test_files_dir, "one_replacement.conf")
        thisincr = mock.Mock()
        tgt = target.Target()
        tgt.targetfile = targetfile
        tgt.edlist.append(editor.Editor("replace", 10,
                                        ("email", "admin@here.org")))
        self.assertRaises(IOError, tgt.run_editors, thisincr)
        # see comment about Python 2.7 above
        try:
            tgt.run_editors(thisincr)
        except IOError as exc:
            self.assertEqual("Target file {0} does not exist or is not "
                              "a regular file".format(targetfile), str(exc))

    def test_no_targetfile(self):
        """Make sure exception is raised when targetfile not set"""
        thisincr = 10
        tgt = target.Target()
        self.assertRaises(ValueError, tgt.run_editors, thisincr)
        # see comment about Python 2.7 above
        try:
            tgt.run_editors(thisincr)
        except ValueError as exc:
            self.assertEqual("template error: no mcfg_filename", str(exc))


if __name__ == '__main__':
    unittest.main()
