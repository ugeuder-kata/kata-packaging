"""Usage: mcfg.py <operation> <template.ini> <master.ini> [<increment>]
       - operation can be either verify or run
       - increment is mandatory for run, optional (and ignored if present)
         for verify
"""

import ConfigParser
import logging
import os
import sys

import editor
import incremental
import target

RUN = 1
VERIFY = 2

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

    @staticmethod
    def run_from_cmd(args):
        """Parse the command line (see module __doc__)
           return 2 on syntax error
           Python will return 1 if some exception occurs. So we don't
           do anything else but basic syntax checking here, the rest of the
           code will throw an exception if the the parameters are not good.
        """
        # TODO: in order to be testable this should really be it's own
        # module so we can use a mock Mcfg
        Mcfg.set_log_level()
        usage = globals()["__doc__"]
        result = 0
        if not len(args) in (4, 5) :
            result = 2
        elif "run".startswith(args[1]):
            operation = RUN
            if len(args) != 5:
                result = 2
            else:
                try:
                    run_incr = int(args[4])
                except ValueError:
                    result = 2
        elif "verify".startswith(args[1]):
            operation = VERIFY
        else:
            result = 2
        if result != 2:
            if operation == RUN:
                master = Mcfg( args[2] , args[3])
                incr = incremental.Incremental(run_incr)
                master.run_editors(incr)
            else:
                raise NotImplementedError, "verify"
        else:
            print >> sys.stderr, usage
        return result

    @staticmethod
    def set_log_level():
        """Get the log level from environment and set it to logging module"""
        level = os.getenv("MCFG_LOG", "warning")
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % level)
        logging.basicConfig(level=numeric_level)

if __name__ == "__main__":
    status = Mcfg.run_from_cmd(sys.argv)
    sys.exit(status)
