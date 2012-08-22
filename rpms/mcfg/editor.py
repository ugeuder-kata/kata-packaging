import edfuncs

class editor:

  def __init__(self, name, toFile, incr, fromStr, toStr):
    self.edfunc = edfuncs.getmeth
    self.incr = incr
    self.toFile = toFile
    self.fromStr = fromStr
    self.toStr = toStr

  def invoke( self, 
