"""
FROM setupVSCode.py
"""
#from urllib.parse import urlparse
#import re
#import cgi

#import html.parser        # py3 ver of 'from HTMLParser import HTMLParser'
#from html.parser import HTMLParser


    # DELETE LATER
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
    
    
    # DELETE LATER
    # i think these are unimportant.  
    #url='https://code.visualstudio.com/docs/?dv=linux64_deb'
    #url='https://code.visualstudio.com/docs/setup/linux'    
    #url='https://code.visualstudio.com/Download'
    #url='https://code.visualstudio.com/docs/?dv=linux64_deb'    #.deb       debian
    #url='https://code.visualstudio.com/docs/?dv=linux64_rpm'   #.rpm       redhat
    #url='https://code.visualstudio.com/docs/?dv=linux64'       #.tar.gz    source code which would need to be compiled
    
    

#from ftplib import FTP

# THIS WHOLE CLASS MAY BE SUPERFLUOUS
# DELETE LATER OR MOVE ElSEWHERE

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
    
