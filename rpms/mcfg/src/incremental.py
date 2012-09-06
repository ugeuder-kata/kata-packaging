"""This module contains the Incremental class"""

import os
import pwd

class Incremental:
    """Idea: call the same command repetitively to work through a list of
    actions. The whole list gets completed incrementally.
    Each action has numerical attribute, that shows in which increment
    the action needs to be performed.
    Increment numbers don't need to be match exactly, they are treated
    as intervals.

    Example:
        list: [(a1, 5), (a2, 10), (a3, 20)]

        (This list is used only to show the concept. No such data structure
        exists in the class.)

    Invocation example 1:

        command(10)  # will invoke actions a1 and a2
        command(25)  # will invoke action a3

    Invocation example 2:

         command(7)  # will invoke action a1
         command(9)  # will not invoke any action
         command(50) # will inoke actions a2 and a3
    """

    def __init__(self, incr):
        """Constructor, each invocation of the constructor designates
        the execution of the increment. This is not idempotent, the 2nd
        instance with the same parameter will actually reset the whole
        sequence!!!
 
               incr: the current increment (increment numbers are
                     non-negative integers)
        """
        self.incr = incr
        # the previously executed increment will be read from
        # a file and the current increment stored to the same
        # file. The file is in /tmp and user specific. (This has
        # security implications in a multi user system, but we
        # don't address them because our only system is a server
        # with only friendly users having access to /tmp).
        # Additionally it means that one user can only have one
        # "active" increments sequence at a time, but again that
        # is enough for our use.
        statusfile = self.get_stat_file_name()
        try:
            stat = open(statusfile, "r")
        except IOError:
            self.lastincr = -1
        else:
            line = stat.read()
            stat.close()
            self.lastincr = int(line)  # if this goes wrong, something is
                                       # really wrong, just throw the exception
        if self.lastincr >= self.incr:
            self.lastincr = -1         # must be leftover from last sequence
                                       # supports also border-case where
                                       # whole sequence is executed always
                                       # at once
        stat = open(statusfile, "w")
        stat.write(str(self.incr))
        stat.close()

    @staticmethod
    def get_stat_file_name():
        """Returns name of the file used to the store the last increment"""
        # this method can be called by unitttests to manipulate the status
        return "/tmp/{0}-incremental".format(
            pwd.getpwuid(os.getuid()).pw_name)

    def __int__(self):
        """Magic function convert to integer.
        Returns the current increment.
        """
        return self.incr

    def is_current(self, some_incr):
        """is_current tests wether a step with value some_incr needs to be
        executed in this increment

            some_incr: the increment value to be tested, does not need to
               an integer, but calling int() must succeed

        returns: True or False
        """
        some_incr = int(some_incr)
        result = some_incr > self.lastincr and some_incr <= self.incr
        return result
