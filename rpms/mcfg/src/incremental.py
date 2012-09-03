"""This module contains the Incremental class"""

class Incremental:
    """Idea: call a command repetitively to work through a list of actions.
    The whole list gets completed incrementally.
    Each action has numerical attribute, that shows in which increment
    the action needs to be performed.
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
        """Constructor
               incr: the current increment
        """
        raise NotImplementedError
        self.incr = incr

    def __int__(self):
        """Magic function convert to integer.
        Returns the current increment.
        """
        return self.incr

    def is_current(self, some_incr):
        """is_current tests wether a step with value some_incr needs to be
        executed in this increment
             
            some_incr: the increment value to be tested

        returns: True or False
        """
        raise NotImplementedError
        return True            
