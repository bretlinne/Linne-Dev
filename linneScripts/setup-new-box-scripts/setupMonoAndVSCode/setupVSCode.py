"""
Python 3 script
Downloads the latest .deb package for installing VSCode, and installs it 

I think this link is a constant link which MS keeps updated to whatever is the current
version of VSCode.  I found a site which had, at the time it was made, current links
to the latest versions.  They use the exact same LinkID=760868 portion, even though that 
website hosted links to VSCode from several releases back
    url = 'https://go.microsoft.com/fwlink/?LinkID=760868'

"""
import os               # used to direct where to save downloaded file
import sys              # used for dealing with CLI flags
import subprocess       # used to derive filepath of CLI arg
import requests         # py3 only
import platform         # used to detect the OS
from urllib.request import urlopen, ContentTooShortError, urlretrieve # py3 version of 'import urllib2'
import re               # used to find dpkg status and fix half-installed issues if they occur
from linneXtermColors import col
from setupVSCodeHelp import printHelp


HOME = os.path.expanduser('~')
filePath = os.path.join(HOME, "Downloads")
fileName = 'vs_code_most_recent_amd64.deb'
outputName = os.path.join(filePath, fileName)
alreadyDownloaded = False

# used in subprocess calls to suppress stdout or stderr
pipeToDevNull = open(os.devnull, 'w')
    
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
    
def DownloadVSCodePkg(url):
    """
    Downloads the file at the specified URL.  Currently works, but I don't think the file can
    be executed or installed.  Need to figure a way to get the proper title as the file name.
    PROPER FORMAT: 'code_1.31.1-1549938243_amd64.deb'
    
    UPDATE: I asked a professor--he says I'm thinking of this wrong.  I don't
    need to worry about the actual file name.  i can call it whatever I want.
    I'm trying to solve a problem that doesn't need solving.
    """
    u = urlopen(url)
    
    # the 'wb' is 'write' 'binary'.
    f = open(outputName, 'wb')
    meta = u.info()
    
    # NOTE: THIS USES GET_ALL AND INITIALLY GETHEADERS() WAS RECOMMENDED FROM THE TUTORIAL
    # GETHEADERS IS OLD AND ONLY IN PY2.7.  GET_ALL DOES THE JOB THOUGH
    fileSize = int(meta.get_all("Content-Length")[0])    
    
    fileSizeDL = 0
    blockSize = 16384 #8192
    
    while True:
        buffer = u.read(blockSize)
        if not buffer:
            break
        fileSizeDL += len(buffer)
        f.write(buffer)
        status = r"%10d Bytes [%3.2f%%]" % (fileSizeDL, fileSizeDL * 100. / fileSize)
        status = status + chr(8)*(len(status)+1)
        print(col.LT_BLUE + "Downloading: {0}".format(status), end="\r", flush=True)
    print("Downloading: {0}".format(status))
    print("Downloaded: {0}".format(fileName))
    print(col.NC)
    f.close()
    del f

def CheckDownloadSuccess():
    try:
        subprocess.check_call("ls " + outputName, stdout=pipeToDevNull, stderr=pipeToDevNull, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def UnpackAndInstall():
    # Detect OS
    linuxDistro = platform.linux_distribution()
    OSType = linuxDistro[0]
    
    # check which OS
    if OSType == 'Ubuntu':
        from apt.debfile import DebPackage
        pkg = DebPackage(outputName)
        command = 'sudo dpkg -i ' + outputName
        
        #The thing that attempts to unpack:
        try:
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError:
            print(col.LT_RED + "Install Failed."  + col.NC)
        """
        THERE'S AN ISSUE THAT CAN OCCUR IF THE PACKAGE DOESN'T INSTALL PROPERLY OR GETS 
        INTERRUPTED.  IN THE DIRECTORY: "/var/lib/dpkg/status"  THE FILE "status" HOLDS A 
        LOG OF ALL PACKAGES INSTALLED ON THE SYSTEM AND WHETHER THEY WERE SUCCESSFUL.  
        MOST WILL CITE "Status: install ok installed".  WHEN SOMETHING FAILS TO INSTALL
        CORRECTLY, IT WILL HAVE "Status: install reinstreq half-installed"
        THAT'S HOW I FOUND WHERE THE ISSUE WAS.
        
        AFTER FAILING TO INSTALL THE CONSOLE RETURNS AN ERROR JUST TRYING TO INVOKE THE
        "DebPackage()" METHOD.  IT LOOKS LIKE THIS:
            Traceback (most recent call last):
              File "setupVSCode.py", line 123, in <module>
                main()
              File "setupVSCode.py", line 120, in main
                UnpackAndInstall()
              File "setupVSCode.py", line 86, in UnpackAndInstall
                pkg = DebPackage(outputName)
              File "/usr/lib/python3/dist-packages/apt/debfile.py", line 51, in __init__
                cache = apt.Cache()
              File "/usr/lib/python3/dist-packages/apt/cache.py", line 113, in __init__
                self.open(progress)
              File "/usr/lib/python3/dist-packages/apt/cache.py", line 165, in open
                self._depcache = apt_pkg.DepCache(self._cache)
            apt_pkg.Error: E:The package code needs to be reinstalled, but I can't find an archive for it.
        
        THIS ABOVE ERROR IS DUE TO THIS ENTRY IN THE status FILE:
        Package: code
        Status: install reinstreq half-installed
        Priority: optional
        Section: devel
        Architecture: amd64
        Version: 1.31.1-1549938243
        
        TO ELIMINATE IT, USE:
        sudo leafpad /var/lib/dpkg/status
        
        SEARCH FOR "half-installed" AND LOOK FOR THE PACKAGE CALLED "code"
        DELETE THE ENTRY, FROM PACKAGE NAME DOWN TO VERSION.
        
        THEN THE SCRIPT CAN BE RE-RUN.
        
        *****   AUTOMATE THIS IN THE CASE OF THIS FAILURE *****
        Steps:
        1. open the file
        2. search for Package: code
        3. verify 'Status: install reinstreq half-installed'
        4. run 'sudo dpkg --force-remove-reinstreq --remove <package_name here>' or
               'sudo dpkg --force-remove-reinstreq --remove code'
                
                if this is effective, output should be: 
                    dpkg: warning: overriding problem because --force enabled:
                    dpkg: warning: package is in a very bad inconsistent state; you should
                     reinstall it before attempting a removal
                    (Reading database ... 179472 files and directories currently installed.)
                    Removing code (1.31.1-1549938243) ...
                
                another possible output is something like this:
                    (Reading database ... 181165 files and directories currently installed.)
                    Removing code (1.31.1-1549938243) ...
                    Processing triggers for desktop-file-utils (0.23-1ubuntu3.17.10.1) ...
                
                if it fails, or the package is not in the 'reinstreq' state, output is:
                    dpkg: warning: ignoring request to remove code which isn't installed

        5. how do we detect if the damn thing has this problem?
        """

def CheckIfCodeInstalled():
    try:
        ps = subprocess.Popen(('ps', '-A'), stdout=subprocess.PIPE)
        codeLocation = subprocess.check_output(('which', 'code'), stdin=ps.stdout)
        ps.wait()
        return codeLocation
        
    # this means Code is not installed
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
    #subprocess.call((command + ' ' + flag + ' ' + package), shell=True)
    
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

def main():
    repairFlag = False
    if (len(sys.argv) > 2):
        printHelp()
        sys.exit(0)
    else:
        if ((sys.argv[-1] == '--repair') or (sys.argv[-1] == '-r')):
            repairFlag = True
        elif ((sys.argv[-1] == '--help') or (sys.argv[-1] == '-h')):
            printHelp()
            sys.exit(0)
    
    codeLocation = CheckIfCodeInstalled()
    if codeLocation is False:
        url = 'https://go.microsoft.com/fwlink/?LinkID=760868'

        alreadyDownloaded = CheckDownloadSuccess()
        
        if alreadyDownloaded is False:
            if IsDownloadable(url):
                DownloadVSCodePkg(url)            
                # check if the download succeeded, if file doesn't already exist.
                if CheckDownloadSuccess():
                    print(col.LT_GREEN + "Download Successful!\nFile location => " + outputName + col.NC)
                else:
                    print(col.LT_RED + "Download Failed..." + col.NC)
            else:
                print(col.LT_RED +'Link broken: need to update the package resource link.' + col.NC)
        else:
            print(col.LT_GREEN + 'File already exists.' + col.NC)
            
        # call unpack and install
        UnpackAndInstall()

        codeLocation = CheckIfCodeInstalled()
        
        if codeLocation is not None and codeLocation is not False:
            print(col.LT_GREEN + 'Microsoft Visual Studio Code is installed:\n' + codeLocation.decode() + col.NC)
            print('Type "code" at the CLI to run the program')
        else:
            print(col.LT_RED + 'Failed to install...  Try invoking with -h flag for possible fixes.' + col.NC)
    else:
        print(col.LT_GREEN + 'Microsoft Visual Studio Code already installed:\n' + codeLocation.decode() + col.NC)
        print('Type "code" at the CLI to run the program')
    
    if repairFlag is True:
        CheckDpkgStatus()
    
if __name__ == "__main__":
    main()
