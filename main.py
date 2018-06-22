#!/usr/bin/python

import code
import atexit
from alh import alh

#_____________________________________________________________________________
def quit_gracefully():
   print "Bye"

#_____________________________________________________________________________
def start_interactive():

   vars = globals()
   vars.update(locals())
   shell = code.InteractiveConsole(vars)
   shell.interact()

#_____________________________________________________________________________
if __name__ == "__main__":

   alh = alh()
   atexit.register(alh.quit)

   start_interactive()

