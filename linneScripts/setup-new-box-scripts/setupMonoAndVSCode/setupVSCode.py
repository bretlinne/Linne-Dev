"""
Python 3 script
Downloads the latest .deb package for installing VSCode, and installs it 
"""
import sys              # used in calls to get CLI args
import subprocess       # used to derive filepath of CLI arg
import requests         # py3 only
from urllib.request import urlopen, ContentTooShortError, urlretrieve # py3 version of 'import urllib2'
from urllib.parse import urlparse
import re
import cgi
#import html.parser        # py3 ver of 'from HTMLParser import HTMLParser'
from html.parser import HTMLParser

from os import path



#from ftplib import FTP

class MyHtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        p = re.compile("https://go.microsoft.com/fwlink/(.*)")
        
        #from 760868
        #code_1.31.1-1549938243_amd64.deb               # Debian/Ubuntu
        #from 760 867
        #code-1.31.1-1549938372.el7.x86_64.rpm          # Fedora, Redhat, SUSE
        
        #only parse the 'anchor' tag
        if tag == 'a':
            """
            #for the indirect link
            for data in attrs:
                if data[0] == 'href':
                    #print(data[1])
                    foo = p.findall(data[1])
                    
                    for result in foo:
                        if result is not None:
                            print(result)
            """
            #check the list of defined attrs
            
            for name, value in attrs:
                #if href is defined, print it
                if name == 'href':
                    print(name + ' = ' + value)
            
                
    """
    def handle_endtag(self, tag):
        print('encountered an end tag:' + tag)
    def handle_data(self, data):
        print('encountered data: ' + data)
    """
    
def IsDownloadable(url):
    """
    Does URL contain a downloadable file?
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
    """
    fileName = url.split('/')[-1]
    u = urlopen(url)
    f = open(fileName, 'wb')
    meta = u.info()
    
    # NOTE: THIS USES GET_ALL AND INITIALLY GETHEADERS() WAS RECOMMENDED FROM THE TUTORIAL
    # GETHEADERS IS OLD AND ONLY IN PY2.7.  GET_ALL DOES THE JOB THOUGH
    fileSize = int(meta.get_all("Content-Length")[0])
    print("Downloading: {0} Bytes: {1}".format(fileName, fileSize))

    """
    fileSizeDL = 0
    blockSize = 8192
    while True:
        buffer = u.read(blockSize)
        if not buffer:
            break
        fileSizeDL += len(buffer)
        f.write(buffer)
        status = r"%10d [%3.2f%%]" % (fileSizeDL, fileSizeDL * 100. / fileSize)
        status = status + chr(8)*(len(status)+1)
        print(status)
    """
    f.close()
    
        
def main():
    #DownloadVSCodePkg()
    
    url = 'https://go.microsoft.com/fwlink/?LinkID=760868'
    #url='https://code.visualstudio.com/docs/?dv=linux64_deb'
    #url='https://code.visualstudio.com/docs/setup/linux'    
    #url='https://code.visualstudio.com/Download'
    #url='https://code.visualstudio.com/docs/?dv=linux64_deb'    #.deb       debian
    #url='https://code.visualstudio.com/docs/?dv=linux64_rpm'   #.rpm       redhat
    #url='https://code.visualstudio.com/docs/?dv=linux64'       #.tar.gz    source code which would need to be compiled
    
    
    if IsDownloadable(url):
        DownloadVSCodePkg(url)
    else:
        print('need to update the package resource link.')

    #openSite = urlopen(url)
    #html = openSite.read()
    
    #p = MyHtmlParser()
    #p.feed(html.decode('utf-8'))
    
    #h = HTMLParser()
    """
    website = urlopen(url)
    html = website.read()
    files = re.findall('href="(.*tgz|.*tar.gz)"', html)
    print(sorted(x for x in (files)))
    """
    
if __name__ == "__main__":
    main()
