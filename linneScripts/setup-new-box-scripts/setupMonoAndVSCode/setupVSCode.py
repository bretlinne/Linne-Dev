"""
Python 3 script
Downloads the latest .deb package for installing VSCode, and installs it 
"""
import os               # used to direct where to save downloaded file
import subprocess       # used to derive filepath of CLI arg
import requests         # py3 only
from urllib.request import urlopen, ContentTooShortError, urlretrieve # py3 version of 'import urllib2'

HOME = os.path.expanduser('~')
filePath = HOME + "/Downloads"
fileName = 'vs_code_most_recent_amd64.deb'
outputName = os.path.join(filePath, fileName)
alreadyDownloaded = False
    
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
    #blockSize = 8192
    blockSize = 16384
    
    while True:
        buffer = u.read(blockSize)
        if not buffer:
            break
        fileSizeDL += len(buffer)
        f.write(buffer)
        status = r"%10d Bytes [%3.2f%%]" % (fileSizeDL, fileSizeDL * 100. / fileSize)
        status = status + chr(8)*(len(status)+1)
        print("Downloading: {0}".format(status), end="\r", flush=True)
    print("Downloading: {0}".format(status))
    print("Downloaded: {0}".format(fileName))
    f.close()


def CheckDownloadSuccess():
    pipeToDevNull = open(os.devnull, 'w')
    try:
        subprocess.check_call("ls " + outputName, stdout=pipeToDevNull, stderr=pipeToDevNull, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def UnpackAndInstall():
    pass
    
        
def main():
    # i think this link is a constant link which MS keeps updated to whatever is the current
    # version of VSCode.  I found a site which had, at the time it was made, current links
    # to the latest versions.  They use the exact same LinkID=760868 portion, even though that 
    # website hosted links to VSCode from several releases back
    url = 'https://go.microsoft.com/fwlink/?LinkID=760868'
    
    alreadyDownloaded = CheckDownloadSuccess()
    
    if alreadyDownloaded is False:
        if IsDownloadable(url):
            DownloadVSCodePkg(url)            
            # check if the download succeeded, if file doesn't already exist.
            if CheckDownloadSuccess():
                print("Download Successful!\nFile location => " + outputName)
            else:
                print("Download Failed...")
     
        else:
            print('Link broken: need to update the package resource link.')
    else:
        print("File already exists.")
    
if __name__ == "__main__":
    main()
