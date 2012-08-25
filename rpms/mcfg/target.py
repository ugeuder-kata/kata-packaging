import itertools
import os
import shutil

class Target:

  def __init__(self):
    # self.name = name     # don't think we need the name for any purpose
                           # except good error messages maybe
    self.targetFile = None
    self.edlist = []

  def runEditors(self, incr):
    backup = self.backup()
    for (ednum, e) in itertools.imap(None, itertools.count(1), self.edlist):
      inFile = None
      if backup :
        inFile = "{0}.backup.{1}".format(self.target, incr)
        if ednum > 1:
          inFile = "{0}.{1}".format(inFile, ednum)
        shutil.move(self.target, inFile)
      e.runIt(inFile, selt.target)
      if backup and ednum > 1:
        os.unlink(inFile)

  def backup(self):
    if len(self.edlist) == 0:
      result=False
    else:
      result=self.edlist[0].backup()
      for e in self.edlist:
        if result != e.backup():
          raise ValueError, "Editors with incompatible backup policy " \
                           "in {0}".format(self.targetFile)
    return result
