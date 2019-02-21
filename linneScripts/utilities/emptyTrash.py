"""
Python 3 script
Empties the trash in ~/.local/share/Trash.  At first I thought it was necessary
to empty the trash/recycle bin on a linux machine. I was constantly downloading
and rm-ing a large file and worried I was filling up the recycle bin.  Part-way
through writing this script I learned it's not necessary as POSIX-based systems
don't really have a Recycle/Trash bin that fills up like in Windows machines.

I finished it anyway as a learning exercise.  Apparently the KDE linux desktop
uses a recycle/trash bin like this and this will work there.  

NEED TO TEST IN KDE ENVIRONMENT

USAGE:  python emptyTrash.py
        python3 emptyTrash.py   -- if you have specified Python 3.x as such
"""
import subprocess           # invoke a shell sub process
from time import sleep      # create a slight delay for UX
import random               # generate random steps for incr of UX
import os                   # for checking if there's trash via os.listdir()

command = "rm -rf "

HOME = os.path.expanduser('~')

filePath = HOME + "/.local/share/Trash/*"

def progress():
    """
    just fluff to make it seem like it's doing something
    """
    step = random.randrange(1,6,2)
    for i in range (0, 101, step):
        step = random.randrange(3,8,2)
        if i > 100:
            i = 100
        else:
            status = r"[%3.1f%%]" % (i)
        sleep(0.008)
        print("Emptying Trash from {0}: {1}".format(filePath, status), end="\r", flush=True)
    print("Emptying Trash from {0}: {1}".format(filePath, "[100.0%]"), end="\r", flush=True)
    print()    
    print("Trash Emptied")

try:
    # check if there's trash to empty
    if os.listdir(filePath[:-1]) != []:
        subprocess.check_call(command + filePath, stderr=subprocess.STDOUT, shell=True)
        progress()
    # if not, reply that there's no need.
    else:
        print(filePath[:-1] + " is already empty!")
        
except subprocess.CalledProcessError:
    print("There was an error.")
