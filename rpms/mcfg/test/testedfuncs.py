import sys
import os
import inspect
import filecmp
import datetime

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

    # originally we used os.tempnam() here but it clutters up the test output
    # with a disturbing security warning.
    oFileName = os.path.join( self.testFilesDir , "replaceSuccessful.out-" 
                                        + datetime.datetime.now().isoformat())

    # we could call the editor function in a easier way here, but let's
    # simulate it once the way it will be done when the name comes from a 
    # text file
    func = getattr( edfuncs.edfuncs , "replace" )
    func( iFileName , oFileName , 'toBeReplaced' , 'replacement' )

    oFileNameExpected = os.path.join( self.testFilesDir , "replace1.out.expected" )
    result = filecmp.cmp( oFileName , oFileNameExpected )
    if result:
      os.unlink( oFileName )
    else:
      print >>sys.stderr , "\nUnexpected result in" , oFileName  
    self.assertTrue( result )


  def test_replaceInputFileMissing(self):
    self.assertRaises(IOError, edfuncs.edfuncs.replace, "foo", "bar", "1", "2")


  def test_copyFileSuccessful(self):
    iFileName = os.path.join( self.testFilesDir , "replace1.in" )
    oFileName = os.path.join( self.testFilesDir , "copyFileSuccessful.out-" 
                                        + datetime.datetime.now().isoformat())
    edfuncs.edfuncs.copyFile( "dummy" , oFileName , "location" , iFileName )
    result = filecmp.cmp( iFileName , oFileName )
    os.unlink( oFileName )
    self.assertTrue( result )


  def test_CopyFileInputFileMissing(self):
    raise NotImplementedError

  def test_CopyFileWrongParameter(self):
    self.assertRaises( ValueError , edfuncs.edfuncs.copyFile , 
                                   "dummy" , "dummy" , "wrong" , "dummy" )


if __name__ == '__main__':
  unittest.main()
