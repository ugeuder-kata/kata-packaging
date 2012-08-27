"""The mcfg main module"""

import ConfigParser
import sys

import target
import editor

class Mcfg:
    """All functionality related to ini files and overall flow control
    goes here.
    """
    SPECIAL_FILENAME = "mcfg_filename"

    def __init__(self, templatefile, mcfgfile):
        self.targetlist = []
        template_ini = ConfigParser.SafeConfigParser()
        files = template_ini.read(templatefile)
        if files != [templatefile]:
            # in theory there could also be more than one, but let's keep 
            # the error message simple
            raise IOError, "Template {0} not found".format(templatefile)
        master_ini = ConfigParser.SafeConfigParser()
        files = master_ini.read(mcfgfile)
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
                                        (name, master_ini.get(sec, name)))
                    tgt.edlist.append(edi)
            self.targetlist.append(tgt)


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
        param = text[blankpos+1:]
        try:
            incr = int(text[:blankpos])
        except ValueError:
            raise ValueError, "Increment value must numeric: " \
                 ">>>{0}<<< {1}".format(text[:blankpos],param)
        return (incr, param)

    def run_editors(self, incr):
        """Run editors on all targets for current increment"""
        for tgt in self.targetlist:
            tgt.run_editors(incr)

if __name__ == "__main__":
    print "TODO"
