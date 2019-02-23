"""
Better detect OS methods
Clean up later.
"""
POWERSHELL = bool(os.getenv('EMSDK_POWERSHELL'))

WINDOWS = False
if os.name == 'nt' or (os.getenv('SYSTEMROOT') != None and 'windows' in os.getenv('SYSTEMROOT').lower()) or (os.getenv('COMSPEC') != None and 'windows' in os.getenv('COMSPEC').lower()):
  WINDOWS = True
  ENVPATH_SEPARATOR = ';'

MSYS = False
if os.getenv('MSYSTEM'):
  MSYS = True
  if os.getenv('MSYSTEM') != 'MSYS' and os.getenv('MSYSTEM') != 'MINGW64':
    print('Warning: MSYSTEM environment variable is present, and is set to "' + os.getenv('MSYSTEM') + '". This shell has not been tested with emsdk and may not work.') # https://stackoverflow.com/questions/37460073/msys-vs-mingw-internal-environment-variables

OSX = False
if platform.mac_ver()[0] != '':
  OSX = True
  ENVPATH_SEPARATOR = ':'

LINUX = False
if not OSX and (platform.system() == 'Linux' or os.name == 'posix'):
  LINUX = True
  ENVPATH_SEPARATOR = ':'
