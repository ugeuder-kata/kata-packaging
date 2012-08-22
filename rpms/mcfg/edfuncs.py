import os
import os.path

class edfuncs:

  @staticmethod
  def replace( fromfile, tofile, fromstr, tostr ):
    f = open( fromfile , "r" )
    t = open( tofile , "w")
    fromstr = "%%" + fromstr.upper() + "%%"
    for line in f:
      line.replce( fromstr, tostr )
      print >> t , tostr
    t.close()
    f.close()

  @staticmethod
  def replace_check( file , fromstr, tostr):
    pass

  @staticmethod
  def copyFile( fromFileDummy, toFile, parDummy, copyFrom )
    os.system( "cp " + copyFrom + " " + toFile )

  @staticmethod
  def copyFile_check( fileDummy, parameter, copyFrom )
    if paramater.lower() != "location" :
      raise ValueError , "Unknown parameter: " + location
    if not os.path.exists( copyFrom )
      raise IOError , "Input file " + copyFrom + " missing

 
    
