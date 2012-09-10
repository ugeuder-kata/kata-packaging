"""This file contains the Editor class"""

import logging

import edfuncs

class Editor:
    """A very thin wrapper class to store a reference to an editor function
    and its parameters
    """
# an editor does not store information about its target. Target : editor
# is a 1 : n relationship, so the details belong to the target. A reverse
# pointer is not needed for our purpose.

# although currently edfuncs take always 4 paramaters we just store a list
# here. It doesn't make the code more complicated and allows to introduce
# edfuncs with more parameters later

# all naming with the semantics of the replace edfunc in mind  

    def __init__(self, ed_func , incr, par_list):
        """constructor just stores all paramters"""
        self.func = getattr(edfuncs.Edfuncs, ed_func)
        self.name = ed_func     # we don't really need the name, but keep it
                                # for potential error messages and debugging
        self.incr = incr
        self.par_list = par_list


    def run_it(self, from_file, to_file):
        """run the editor function in this instance
        does not take the increment into accout, needs to be done by the caller
        """
        logging.debug("Editor.run_it %s(%s, %s, %s)", self.name, from_file,
                       to_file, str(self.par_list))
        self.func(from_file, to_file, *self.par_list)


    def backup(self):
        """return the backup policy as given by the underlying editor function
        """
        return self.func.backup


    def __int__(self):
        """Magic function __int__ returns the increment the editor belongs to"""
        # This might not be a least-surprise choice, but it makes it easy
        # to filter lists of editors during incremental execution
        return self.incr
