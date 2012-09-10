import logging

import edfuncs

class Editor:

# an editor does not store information about its target. Target : editor
# is a 1 : n relationship, so the details belong to the target. A reverse
# pointer is not needed for our purpose.

# although currenently edfuncs take always 4 paramaters we just store a list
# here. It doesn't make the code more complicated and allows to introduce
# edfuncs with more parameters later

# all naming with the semantics of the replace edfunc in mind  

  def __init__(self, edFunc , incr, parList):
    self.func = getattr(edfuncs.Edfuncs, edFunc)
    self.name = edFunc      # we don't really need the name, but keep it
                            # for potential error messages and debugging
    self.incr = incr
    self.parList = parList


  def run_it(self, fromFile, toFile):
    """run the editor function in this instance"""
    logging.debug("Editor.run_it %s(%s, %s, %s)", self.name, fromFile,
                   toFile, str(self.parList))
    self.func(fromFile, toFile, *self.parList)

  def backup(self):
    return self.func.backup

  def __int__(self):
    """Magic function __int__ returns the increment the editor belongs to"""
    # This might not be a least-surprise choice, but it makes it easy
    # to filter lists of editors during incremental execution
    return self.incr
