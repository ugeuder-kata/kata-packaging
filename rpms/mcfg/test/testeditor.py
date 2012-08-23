import sys
import os
import filecmp
import datetime

# we live in subdirectory test, so we need to import the code to be tested
# from the parent directory. I don't like this hack, please suggest something
# better
hackedPath = [ os.path.join( sys.path[0] , "..") ]
hackedPath.extend( sys.path )
sys.path = hackedPath

import editor
import unittest

class TestEditor(unittest.TestCase):

  def setUp(self):
    here = sys.path[1]
    self.testFilesDir = os.path.join( here , "files" )

  def test_invokeEditor(self):
    # lets just reuse the files from TestEdfuncs.test_replaceSucessful
    # we could also use a mock object for edfuncs, but the real one
    # seems to be reasonably simple so we don't
    iFileName = os.path.join( self.testFilesDir , "replace1.in" )
    oFileName = os.path.join( self.testFilesDir , "editor.out-" 
                                        + datetime.datetime.now().isoformat())

    e = editor.editor( "replace" , 10 , ( "toBeReplaced" , "replacement" )) 
    e.runIt( iFileName , oFileName )

    oFileNameExpected = os.path.join( self.testFilesDir , "replace1.out.expected" )
    result = filecmp.cmp( oFileName , oFileNameExpected )
    if result:
      os.unlink( oFileName )
    else:
      print >>sys.stderr , "\nUnexpected result in" , oFileName  
    self.assertTrue( result )


if __name__ == '__main__':
  unittest.main()
