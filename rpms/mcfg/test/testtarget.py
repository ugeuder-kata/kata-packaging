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

import editor
import target

class TestTarget(unittest.TestCase):

    def setUp(self):
        # make this independent of the cwd, always relative to our code
        self.test_files_dir = os.path.join(here, "files")

    def test_empty_edlist(self):
        samplefile = os.path.join(self.test_files_dir, "replace1.in" )
        targetfile = os.path.join(self.test_files_dir, "emptyEdlist.out-"
                                        + datetime.datetime.now().isoformat())
        shutil.copy(samplefile, targetfile)
        tgt = target.Target()
        tgt.targetfile = targetfile
        tgt.run_editors(77)
        self.assertTrue(filecmp.cmp(samplefile, targetfile))
        os.unlink(targetfile)

    def test_contradicting_backup(self):
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
            self.assertEqual( "Editors with incompatible backup policy in " \
                             "contradictive", str(exc))


if __name__ == '__main__':
    unittest.main()
