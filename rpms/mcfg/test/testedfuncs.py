import sys
import os

# we live in subdirectory test, so we need to import the code to be tested
# from the parent directory. I don't like this hack, please suggest something
# better
hackedPath = [ os.path.join( sys.path[0] , "..") ]
hackedPath.extend( sys.path )
sys.path = hackedPath

import edfuncs
import unittest

class TestEdfuncs(unittest.TestCase):

# def setUp(self):
#   self.seq = range(10)

  def test_replaceSuccessful(self):
    pass
#        self.assertEqual(self.seq, range(10))

#        self.assertRaises(TypeError, random.shuffle, (1,2,3))

  def test_replaceInputFileMissing(self):
    pass

  def test_copyFileSuccessFul(self):
    pass

  def test_CopyFileInputFileMissing(self):
    pass
 
  
if __name__ == '__main__':
  unittest.main()
