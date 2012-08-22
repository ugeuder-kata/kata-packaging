# Originally the idea was to have a special edit_check function for each
# editor function edit. However, this has been removed. Instead in the
# pre_installation check operation we call the real editor function on
# a dummy file. So any extra tests should just be added to the editor
# function proper.

# For administrator-friendly error messages we would need the location
# of the mcfg file the failing editor belongs to. Or maybe the caller
# should catch the exception and associate with a line in the mcfg file
# Well, maybe later...

# Each editor function takes 4 parameters:
# The basic concept is sed-like editing, more special editors might
# not need all of them, so they will just be dummies for those
# (Maybe we could also work with a variable amount of parameters, but
# at the moment we don't. Will probably come if an edit function really
# needs more parameters.)
#
# For the moment the 4 parameters are
#
#   fromFile: The file it is reading from (typically that could be
#     a temporary copy of the target file, because reading and
#     writing to the same file might not be a good idea).
#   toFile: This is really the target. The readily edited configuration file
#   fromString: the string to be replaced
#   toString: the replacement string    

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
  def copyFile( fromFileDummy, toFile, parDummy, copyFrom )
    if paramater.lower() != "location" :
      raise ValueError , "Unknown parameter: " + location
    if not os.path.exists( copyFrom )
      raise IOError , "Input file " + copyFrom + " missing

    os.system( "cp " + copyFrom + " " + toFile )

  @staticmethod
  def copyFile_check( fileDummy, parameter, copyFrom )
    if paramater.lower() != "location" :
      raise ValueError , "Unknown parameter: " + location
    if not os.path.exists( copyFrom )
      raise IOError , "Input file " + copyFrom + " missing

 
    
