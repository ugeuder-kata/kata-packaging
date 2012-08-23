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
#
# fromFile and toFile are taken as fileNames and opened and closed by
# the editor function. Of course when several editors are called after each
# other this is somewhat inefficient compared to running each editor on the
# same buffer. However, with the data volume expected to be handled by 
# this tool we prefer the simple implementation.

import os
import os.path

class edfuncs:

  @staticmethod
  def replace( fromFile, toFile, fromStr, toStr ):
    f = open( fromFile , "r" )
    if os.path.exists( toFile ):
      raise IOError, "Output file " + toFile + " already exists"
    t = open( toFile , "w")
    fromStr = "%%" + fromStr.upper() + "%%"
    for line in f:
      line = line.replace( fromStr, toStr )
      t.write( line )
    t.close()
    f.close()

  @staticmethod
  def copyFile( fromFileDummy, toFile, parameter, copyFrom ):
    if parameter.lower() != "location" :
      raise ValueError , "Unknown parameter: " + parameter
    if not os.path.exists( copyFrom ):
      raise IOError , "Input file " + copyFrom + " missing"
    if os.path.exists( toFile ):
      raise IOError , "Target file " + toFile + " already exists"

    os.system( "cp " + copyFrom + " " + toFile )

# Python does not allow setting attributes on methods (see PEP232)
# so we do it aftetwards. Maybe we should get rid of the whole class
# it serves no purpose at the moment  
edfuncs.replace.backup = True
edfuncs.copyFile.backup = False


 
    
