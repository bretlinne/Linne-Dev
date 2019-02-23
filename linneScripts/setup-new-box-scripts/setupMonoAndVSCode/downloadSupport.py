import os               # used to direct where to save downloaded file
import requests         # used in IsDownloadable()
import subprocess       # used to derive filepath of CLI arg
from linneXtermColors import col
import re               # used to find dpkg status and fix half-installed issues if they occur

def IsDownloadable(url):
    """
    Check of the link passed in is a downloadable file. Used to shortcut the 
    processing so that it doesn't attempt to download a URL that isn't 
    downloadable.  Returns True or False.
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    contentType = header.get('content-type')
    if 'text' in contentType.lower():
        return False
    if 'html' in contentType.lower():
        return False
    return True

def CheckDownloadSuccess(outputName):
    # used in subprocess calls to suppress stdout or stderr
    pipeToDevNull = open(os.devnull, 'w')

    try:
        subprocess.check_call("ls " + outputName, stdout=pipeToDevNull, stderr=pipeToDevNull, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def CheckDpkgStatus():
    """
    uses dpkg-query shell command to check if code is installed at all,
    and to check if the dpkg status is 'installed OK' or 'half-installed'
    """
    command = 'dpkg-query'
    flag = '--status'
    package =  'code'
    
    ps = subprocess.Popen(('ps', '-A'), stdout=subprocess.PIPE)
    output = subprocess.check_output((command, flag, package), stdin=ps.stdout)
    ps.wait()    
    
    output = output.decode('utf-8')
    
    patternHalfInstalled = r'\bStatus: install reinstreq half-installed\b'
    patternOk = r'\bStatus: install ok installed\b'
    ok = 'Status: install ok installed'
    
    if output is not None:
        # ----------------------------------------
        # search for ok
        # ----------------------------------------
        try:
            result = re.findall(patternOk, output)
        except AttributeError:
            result = None
     
        matchValue = ""
        if result:
            for item in result:
                matchValue = item
            if matchValue == "Status: install ok installed":
                print(col.LT_GREEN + 'Microsoft Visual Studio Code installed with status:\n' + col.LT_BLUE + ok  + col.NC)
    
        # ----------------------------------------
        # search for half-installed
        # ----------------------------------------
        try:
            result = re.finall(patternHalfInstalled, output)
        except AttributeError:
            result = None
        
        if result:
            for item in result:
                matchValue = item
            if matchValue == ok:
                command = 'sudo dpkg --force-remove-reinstreq --remove code'
                subprocess.call(command, shell=True)
                print(col.LT_BLUE+ 'Partially installed package removed, VSCode uninstalled.')
                print('Re-run this script to re-install.'  + col.NC)
    else:
        print(col.YELLOW + 'Code is not installed.' + col.NC)

def CheckIfCodeInstalled():
    try:
        ps = subprocess.Popen(('ps', '-A'), stdout=subprocess.PIPE)
        codeLocation = subprocess.check_output(('which', 'code'), stdin=ps.stdout)
        ps.wait()
        return codeLocation
        
    # this means Code is not installed
    except subprocess.CalledProcessError:
        return False
