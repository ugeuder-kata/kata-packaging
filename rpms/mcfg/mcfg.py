"""The mcfg main module"""

import ConfigParser
import sys

import target
import editor

class Mcfg:
    """All functionality related to ini files and overall flow control
    goes here.
    """
    SPECIAL_FILENAME="mcfg_filename"

    def __init__(self, templatefile, mcfgfile):
        template_ini = ConfigParser.SafeConfigParser()
        files = template_ini.read(templatefile)
        if files != [templatefile]:
            # in theory there could also be more than one, but let's keep 
            # the error message simple
            raise IOError, "Template {0} not found".format(templatefile)
        self.master_ini = ConfigParser.SafeConfigParser()
        files = self.master_ini.read(mcfgfile)
        if files != [ mcfgfile ] :
            # as above
            raise IOError, "Master config file {0} not found".format(mcfgfile)
        for sec in template_ini.sections():
            tgt = target.Target()
            for (name, value) in template_ini.items(sec):
                if name == self.SPECIAL_FILENAME:
                    tgt.targetfile = value
                else:
                    incr, edname = self.parsevalue(value)
                    edi = editor.Editor(edname, incr, 
                                        self.getparlist(sec, name))

    def getparlist(self, sec, name):
        """get the parlist for an editor.
           - sec: the ini file section
           - name: the parameter name
        returns: parlist, list of parameters for the editor taken from
           master ini. Currently limited to 2 elements (name, value)
        """
        try:
          items = self.master_ini.items(sec)
        except Exception:
          raise
        try:
          print "\n***" , items
          value = items[name]
        except Exception:
          raise


    @staticmethod
    def parsevalue(text):
        """parse a valuestring: 
           - integer increment
           - blank separator
           - string parameter
        returns (incr, parameter)
        """
        blankpos = text.find(" ")
        if blankpos < 1:
            raise ValueError, "Increment value must be separated from " \
                             "editor name by space: {0}".format(text)
        param=text[blankpos+1:]
        try:
            incr=int(text[:blankpos])
        except ValueError:
            raise ValueError, "Increment value must numeric: " \
                 ">>>{0}<<< {1}".format(text[:blankpos],param)
        return (incr, param)


if __name__ == "__main__":
    print "TODO"
