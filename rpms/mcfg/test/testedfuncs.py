import sys
import os
import inspect
import filecmp

# we live in subdirectory test, so we need to import the code to be tested
# from the parent directory. I don't like this hack, please suggest something
# better
hackedPath = [ os.path.join( sys.path[0] , "..") ]
hackedPath.extend( sys.path )
sys.path = hackedPath

import edfuncs
import unittest

class TestEdfuncs(unittest.TestCase):

  def setUp(self):
    here = sys.path[1]
    self.testFilesDir = os.path.join( here , "files" )

  def test_replaceSuccessful(self):
    iFileName = os.path.join( self.testFilesDir , "replace1.in" )
    print >> sys.stderr , "\n%s:%d: tempnam risk neglected, please suggest improvement" % ( __file__ , inspect.currentframe().f_lineno )
    oFileName = os.tempnam( )
    # we could call the editor function in a easier way here, but let's
    # simulate it once the way it will be done when the name comes from a 
    # text file
    func = getattr( edfuncs.edfuncs , "replace" )
    func( iFileName , oFileName , 'toBeReplaced' , 'replacement' )
    # maybe by using difflib instead of filecmp we could replace tempnam
    # by tmpfile???
    oFileNameExpected = os.path.join( self.testFilesDir , "replace1.out.expected" )
    result = filecmp.cmp( oFileName , oFileNameExpected )
    if result:
      os.unlink( oFileName )
    else:
      print >>sys.stderr , "\nUnexpected result in" , oFileName  
    self.assertTrue( result )


  def test_replaceInputFileMissing(self):
    pass
#        self.assertRaises(TypeError, random.shuffle, (1,2,3))


  def test_copyFileSuccessFul(self):
    pass

  def test_CopyFileInputFileMissing(self):
    pass


if __name__ == '__main__':
  unittest.main()
