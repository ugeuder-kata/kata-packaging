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

import edfuncs

class TestEdfuncs(unittest.TestCase):

  def setUp(self):
    self.testFilesDir = os.path.join( here , "files" )

  def test_replaceSuccessful(self):
    # same files used by TestEditor.test_invokeEditor
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
    doesNotExist = "/tmp/seqwe/doesNotExist"
    args = ( "dummy", "dummy", "location",  doesNotExist )
    self.assertRaises( IOError , edfuncs.edfuncs.copyFile , *args ) 
    # in Python 2.7 we could have used assertRaises as context manager,
    # in the first place, but we need to support Python 2.6
    # (of course this could be coded differently using try, but the
    # assertRaises conveys the idea what we are doing)
    try:
      edfuncs.edfuncs.copyFile( *args )
    except IOError as e:
      self.assertEqual( "Input file " + doesNotExist + " missing" , str(e))


  def test_CopyFileTargetFileAlreadyThere(self):
    iFileName = os.path.join( self.testFilesDir , "replace1.in" )
    oFileName = os.path.join( self.testFilesDir , "replace1.out.expected" )
    args = ( "dummy", oFileName, "location",  iFileName )
    self.assertRaises( IOError , edfuncs.edfuncs.copyFile , *args )
    # see comment about assertRaises above
    try:
      edfuncs.edfuncs.copyFile( *args )
    except IOError as e:
      self.assertEqual( "Target file " + oFileName + " already exists" , str(e))


  def test_CopyFileWrongParameter(self):
    args = ( "dummy" , "dummy" , "wrong" , "dummy" )
    self.assertRaises( ValueError , edfuncs.edfuncs.copyFile, *args ) 
    # see comment about assertRaises above
    try:
      edfuncs.edfuncs.copyFile( *args )
    except ValueError as e:
      self.assertEqual( "Unknown parameter: wrong" , str(e))


if __name__ == '__main__':
  unittest.main()
