# not really a unittest, just some helper to read an ini file

import ConfigParser

config=ConfigParser.SafeConfigParser()

cfile="template.ini"
files=config.read(cfile)
if files != [ cfile ] :
  raise IOError , ( "%s not found" % cfile )

for s in config.sections():
  print s
  for i in config.items(s) :
    print i

