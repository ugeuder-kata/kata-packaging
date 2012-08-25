import datetime
import filecmp
import os
import shutil
import sys
import unittest

# we live in subdirectory test, so we need to import the code to be tested
# from the parent directory. I don't like this hack, please suggest something
# better (well, nose does it already, but maybe not everybody uses it)
here=os.path.split( __file__ )[0]
if here == '' :
  here = os.getcwd()
above=os.path.split( here )[0]
hackedPath = [ above ]
hackedPath.extend( sys.path )
sys.path = hackedPath

import editor
import target

class TestTarget(unittest.TestCase):

  def setUp(self):
    # make this independent of the cwd, always relative to our code
    self.testFilesDir = os.path.join(here, "files")

  def test_emptyEdlist(self):
    sampleFile = os.path.join(self.testFilesDir, "replace1.in" )
    targetfile = os.path.join(self.testFilesDir, "emptyEdlist.out-"
                                        + datetime.datetime.now().isoformat())
    shutil.copy(sampleFile, targetfile)
    t = target.Target()
    t.targetfile = targetfile
    t.run_editors(77)
    self.assertTrue(filecmp.cmp(sampleFile, targetfile))
    os.unlink(targetfile)

  def test_contradictingBackup(self):
    t = target.Target()
    t.targetfile = "contradictive"
    t.edlist.append(editor.Editor("replace", 10, ("foo", "bar")))
    t.edlist.append(editor.Editor("copy_file", 10, ("location", "inputFile")))
    self.assertRaises(ValueError, t.backup)
    # in Python 2.7 we could have used assertRaises as context manager,
    # in the first place, but we need to support Python 2.6
    # (of course this could be coded differently using try, but the
    # assertRaises conveys the idea what we are doing)
    try:
      t.backup()
    except ValueError as e:
      self.assertEqual( "Editors with incompatible backup policy in " \
                        "contradictive", str(e))


if __name__ == '__main__':
  unittest.main()
