import sys
import os
import inspect

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
    iFile = open( iFileName , "r" )
    print >> sys.stderr , "\n%s:%d: tempnam risk neglected, please suggest improvement" % ( __file__ , inspect.currentframe().f_lineno )
    oFileName = os.tempnam( )
    oFile = open( oFileName , "w" )
    # we could call the editor function in a easier way here, but let's
    # simulate it once the way it will be done when the name comes from a 
    # text file
    func = getattr( edfuncs.edfuncs , "replace" )
    func( iFile , oFile , 'toBeReplaced' , 'replacement' )
    oFile.close()
    iFile.close()
    # maybe by using difflib instead of filecmp we could replace tempnam
    # by tmpfile???
    self.assertTrue( filecmp.cmp( iFileName , oFileName ))
    os.unlink( oFileName )


  def test_replaceInputFileMissing(self):
    pass
#        self.assertRaises(TypeError, random.shuffle, (1,2,3))


  def test_copyFileSuccessFul(self):
    pass

  def test_CopyFileInputFileMissing(self):
    pass


if __name__ == '__main__':
  unittest.main()
