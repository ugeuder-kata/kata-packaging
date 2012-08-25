import edfuncs

class editor:

# an editor does not store information about its target. Target : editor
# is 1 : n relation ship, so the details belong to the target. A reverse
# pointer is not needed for our purpose.

# although currenently edfuncs take always 4 paramaters we just store a list
# here. It doesn't make the code more complicated and allows to introduce
# edfuncs with more parameters later

# all naming with the semantics of the replace edfunc in mind  

  def __init__(self, edFunc , incr, parList):
    self.func = getattr(edfuncs.edfuncs, edFunc)
    self.name = edFunc      # we don't really need the name, but keep it
                            # for potential error messages and debugging
    self.incr = incr
    self.parList = parList


  def runIt(self, fromFile, toFile):
    # incr ignored for the time being
    self.func(fromFile, toFile, *self.parList)

  def backup(self):
    return self.func.backup
