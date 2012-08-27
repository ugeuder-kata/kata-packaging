# not really a unittest, just some helper to read an ini file

import ConfigParser

config=ConfigParser.SafeConfigParser()

cfile="example.ini"
files=config.read(cfile)
if files != [ cfile ] :
  raise IOError , ( "%s not found" % cfile )

for s in config.sections():
  print s
  for i in config.items(s) :
    print i

try:
  config.get("wrong_section", "foo")
except ConfigParser.NoSectionError as exc:
  print exc

try:
  config.get("ckan.ini", "foo")
except ConfigParser.NoOptionError as exc:
  print exc

