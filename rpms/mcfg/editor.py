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
    self.edFunc = edFunc
    self.incr = incr
    self.parList = parList

  def runIt( self, fromFile, toFile) :
    # incr ignored for the time being
    func = getattr( edfuncs.edfuncs , self.edFunc )
    func( fromFile , toFile , *self.parList )

