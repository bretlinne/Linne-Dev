"""
Detect OS
USAGE:
    in another python script:
    "from DetectOS.py import WINDOWS, MSYS, OSX, LINUX"
    
    run through python to print out OS info:
    python linneDetectOS.py -v
    
    IMPORTABLE VALUES:
    ------------------
    WINDOWS, MSYS, OS, LINUX, ARMBIAN   --bool values
    ENVPATH_SEPARATOR                   --either set to ';' for Win, or ':' for else
    LINUX_DISTRO                        --set to name of OS distribution
	PROCESSOR							--set to architecture type (x86_64, ARM)
"""

import os
import platform
import sys

# name value to be printed out, not exported
outputOS = 'UNDEFINED'

WINDOWS = False
#check if system is Windows via os.name or os.getenv
if os.name == 'nt' or (os.getenv('SYSTEMROOT') != None and 'windows' in os.getenv('SYSTEMROOT').lower()) or (os.getenv('COMSPEC') != None and 'windows' in os.getenv('COMSPEC').lower()):
    WINDOWS = True
    outputOS = 'Windows'
    ENVPATH_SEPARATOR = ';'

#check for MinGW and MSYS 
MSYS = False
if os.getenv('MSYSTEM'):
  MSYS = True
  outputOS = 'MSYS'
  if os.getenv('MSYSTEM') != 'MSYS' and os.getenv('MSYSTEM') != 'MINGW64':
    print('Warning: MSYSTEM environment variable is present, and is set to "' + os.getenv('MSYSTEM') + '". This shell has not been tested with emsdk and may not work.') # https://stackoverflow.com/questions/37460073/msys-vs-mingw-internal-environment-variables

#check for OSX
OSX = False
if platform.mac_ver()[0] != '':
    OSX = True
    outputOS = 'Apple OSX'
    ENVPATH_SEPARATOR = ':'
    
#check for Linux
LINUX = False
if not OSX and platform.system() == 'Linux' or os.name() == 'posix':
    outputOS = 'Linux'
    LINUX = True
    ENVPATH_SEPARATOR = ':'

#find which type of linux
if LINUX:
    #LINUX_DISTRO = platform.platform()
    LINUX_DISTRO = platform.linux_distribution()[0]
    #LINUX_DISTRO  = 'Linux-3.4.113-sun8i-armv7l-with-Ubuntu-16.04-xenial'
    
    #target behavior: python -mplatform | grep -qi Ubuntu && sudo apt-get update || sudo yum update
    # -qi flags in the grep statement tell it to not print output to console (q for quiet)
    # and the -i is for ignore.  It  ignores case in the pattern and input files
    
    #check if we're running 'ARMBIAN' example output:     line = "Linux-3.4.113-sun8i-armv7l-with-Ubuntu-16.04-xenial"
    # this could return true if we're only parsing for 'ubuntu' but not tell us that it's 
    # an arm architecture.  A further check for 'ARMBIAN' is needed by finding if the resulting
    # platform string contains the word 'arm'.  
    ARMBIAN = False
    PROCESSOR = platform.processor()
    
    """
    #check ubuntu
    #if LINUX_DISTRO.lower() == 'ubuntu':
    if LINUX_DISTRO.lower().find('arm') != -1:
        ARMBIAN = True
    
    
    #check CentOS
    elif (LINUX_DISTRO.lower().find('centos')) != -1:
        LINUX_DISTRO = 'CentOS'
        
    # Check ARCH linux
    # Example output for platform.platform():
    # 'Linux-4.12.6-1-ARCH-86_64-with-arch'
    #elif (LINUX_DISTRO.lower().find('arch')) != -1:
    elif (LINUX_DISTRO.lower() == 'arch'):
        LINUX_DISTRO = 'Arch Linux'
    else:
        LINUX_DISTRO = 'UNDETERMINABLE'
    
    # check if a file argument was passed in from the  command line
	"""
	
def outputResults():
    print('OS:\t\t' + outputOS)
    print('Processor Type:\t' + PROCESSOR)
    print('Distro:\t\t' + LINUX_DISTRO)
    
if (sys.argv[-1] == '-v') or (sys.argv[-1] == '--verbos'):
    outputResults()
    sys.exit(0)

    
