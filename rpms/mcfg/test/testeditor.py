import datetime
import filecmp
import os
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

class TestEditor(unittest.TestCase):

  def setUp(self):
    # make this independent of the cwd, always relative to our code
    self.testFilesDir = os.path.join( here , "files" )

  def test_invokeEditor(self):
    # lets just reuse the files from TestEdfuncs.test_replaceSucessful
    # we could also use a mock object for edfuncs, but the real one
    # seems to be reasonably simple so we don't
    iFileName = os.path.join( self.testFilesDir , "replace1.in" )
    oFileName = os.path.join( self.testFilesDir , "editor.out-"
                                        + datetime.datetime.now().isoformat())

    edi = editor.Editor( "replace" , 10 , ( "toBeReplaced" , "replacement" ))
    edi.run_it( iFileName , oFileName )

    oFileNameExpected = os.path.join( self.testFilesDir , "replace1.out.expected" )
    result = filecmp.cmp( oFileName , oFileNameExpected )
    if result:
      os.unlink(oFileName)
    else:
      print >>sys.stderr , "\nUnexpected result in" , oFileName
    self.assertTrue( result )

  def test_backup(self):
    e = editor.Editor("replace", 10, ("toBeReplaced", "replacement"))
    self.assertTrue(e.backup())
    e = editor.Editor("copy_file", 10, ("location", "foo"))
    self.assertFalse(e.backup())

if __name__ == '__main__':
  unittest.main()
