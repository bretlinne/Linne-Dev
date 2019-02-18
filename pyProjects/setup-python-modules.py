from __future__ import print_function
import sys
import os
import platform
from time import sleep
import subprocess#, CalledProcessError, check_output

class col:
    RED='\033[0;31m'
    LT_RED='\033[1;31m'
    LT_GREEN='\033[1;32m'
    YELLOW='\033[1;33m'
    LT_BLUE='\033[1;36m'
    NC='\033[0m' # NO COLOR

aIter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
'n','o','p','q','r','s','t','u','v','w','x','y','z']


defOutputColor = col.LT_GREEN 
  
def ConOutput(msg, delayTrue=False, color=None):
    if color is None:
        color = defOutputColor
    print( color + " => " + msg, end='')
    if delayTrue is True:
        DotDelay()
    else:
        sys.stdout.flush()
        print('\n')
    
def DotDelay(count=None, length=None):
    if count is None:
        count = 3
    if length is None:
        length = 0.25
    sys.stdout.flush()
    for i in range(0, count):
        print('.', end='')
        sleep(length)
        sys.stdout.flush()
    sleep(length)
    print('\n')

def CheckInstallPip():
    # first estalblish if pip is installed
    pipInstalled = False
    try:
        import pip
        pipInstalled = True
    except ImportError:
        print(col.LT_RED + " Pip not present...")
    
    # if so, skip the remainder
    if pipInstalled is True:
        ConOutput("PIP installed", False, col.LT_BLUE)
    # if not, detect OS and install PIP
    else:
        ConOutput("Installing PIP", True)
        
        OSType = platform.linux_distribution()
        print(col.LT_BLUE)
        cmd = "echo {0}{1}".format('OS Detected: ',OSType[0])
        
        os.system(cmd)
        if OSType[0] == "Ubuntu":
            pass
            os.system('sudo apt install python-pip')
            os.system('sudo apt install python3-pip')
        else:
            pass
            os.system('yum install epel-release')
            os.system('yum install python-pip')
            os.system('yum install python3-pip')
        print('\n'+col.NC)
            
def installAllModules(ml):
    if 'pip' in sys.modules:
        if ml:
            print("exists")
        pass
    else:
        print(col.YELLOW + "\n Python modules are hard to install without PIP.")
        sleep(0.5)
        print(" Do that first Rookie.")

class InputSwitch:
    def __init__(self, ml=None, tl=None):
        self.ml = ml
        self.tl = tl
        
    def switch(self, input):
        inputString = str(input).lower()
        return getattr(self, 'case_' + inputString, lambda: self.default())()
    
    def default(self):
        print(col.LT_RED + " Make a valid selection.\n")
        sleep(0.5)
        return True
        
    def case_a(self):
        CheckInstallPip()
        return True
    
    def case_b(self):
        installAllModules(self.ml)
        return True
        
    def case_installModule(self, moduleToInstall):
        cmd = 'pip install ' + moduleToInstall
        #os.system(cmd)
        try:
            import Pillow
            print(col.LT_BLUE + " Pillow present...")
        except ImportError:
            print(col.LT_RED + " Pillow not present...")
        
        return True
        
    def case_choose_module(self, libraryType):
        self.input = libraryType
        if (self.input == 'data'):
            prompt = "\n SQL & Data Analysis Libraries:"
        elif (self.input == 'game_dev'):
            prompt = "\n Game Development Libraries:"
        elif (self.input == 'graphics'):
            prompt = "\n Graphics and GUI Libraries:"
        elif (self.input == 'math'):
            prompt = "\n Math and Scientific Libraries:"
        elif (self.input == 'networking'):
            prompt = "\n Networking Libraries:"
        elif (self.input == 'util'):
            prompt = "\n Utility Libraries:"
        print(prompt)
        
        # get size of the console window for output checking below
        rows, columns = os.popen('stty size', 'r').read().split()
        
        validChoices = {}
        looping = True
        while looping is True:
            iterator = 0;
            for i in range(0, len(self.ml)):
                
                #only display the choices for the chosen category
                if self.ml[i].type == self.input:
                    
                    #setup a dictionary of valid choices using userInput letter choices as key
                    validChoices[aIter[iterator]] = self.ml[i].name
                    
                    #setup output spacing
                    if len(self.ml[i].name) > 12:
                        tab = '\t'
                    elif len(self.ml[i].name) < 5:
                        tab = '\t\t\t'
                    else:
                        tab = '\t\t'
                    pad = ' '
                    
                    if len(self.ml[i].desc) > rows:
                        print("{: >20} {: >20} {: >20}".format(*row))
                    print(self.ml[i].color + "\t"+ aIter[iterator] + ")" + pad + 
                    self.ml[i].name + tab +
                    self.ml[i].iString + "\n\t  --" +
                    self.ml[i].desc)
                    iterator+=1
                    
            print(col.LT_GREEN + "\t" + "z)" + pad +
            "<< GO BACK")
            print("Make a choice:")
            
            # get user input
            userInput = raw_input()
            
            # go back if user enters z/Z
            if userInput.lower() == 'z':
                looping = False
            else:
                #look through dictionary for key matching userInput
                moduleToInstall = validChoices.get(userInput.lower(), 'unknown')
                if moduleToInstall == "unknown":
                    print("Make a valid selection")
                else:
                    # pass the module name to the install case
                    self.case_installModule(moduleToInstall)
                    for i in range(0, len(self.ml)):
                        self.ml[i].updateModuleColors()
        return True
    
    # break out of program        
    def case_x(self):
        return False

moduleData = {
'Requests': {'name': 'Requests', 'type':'networking', 'desc': 'Famous http library by kenneth reitz.  Must have for every python developer'},
'Scapy': {'name': 'Scapy', 'type':'networking', 'desc': 'A packet sniffer and analyzer for python made in python.'},
'Scrapy': {'name': 'Scrapy', 'type':'networking', 'desc': 'Webscraping library.'},
'Twisted': {'name': 'Twisted', 'type':'networking', 'desc': 'Important tool for any network application developer. Beautiful api.'},

'Pillow': {'name': 'Pillow', 'type':'graphics', 'desc': 'A user-friendly fork of PIL (Python Imaging Library).'},
'pyQT': {'name': 'pyQT', 'type':'graphics', 'desc': 'A GUI toolkit for python. 2nd to wxpython for developing GUI\'s.'},
'pyGtk': {'name': 'pyGtk', 'type':'graphics', 'desc': 'Another python GUI library. Bittorrent client was created with this.'},
'wxPython': {'name': 'wxPython', 'type':'graphics', 'desc': 'A gui toolkit for python. similar to tkinter.'},

'NumPy': {'name': 'NumPy', 'type':'math', 'desc': 'Provides advanced math functionalities to python'},
'SciPy': {'name': 'SciPy', 'type':'math', 'desc': 'Useful with NumPy. Algorithms & math tools for scientific work.'},
'SymPy': {'name': 'SymPy', 'type':'math', 'desc': 'Algebraic evaluation library: differentiation, expansion, complex \n\t    numbers, etc. Contained in a pure Python distribution.'},
    
'matplotlib': {'name': 'matplotlib', 'type':'data', 'desc': 'A numerical plotting library. For Data scientist & analysis.'},
'SQLAlchemy': {'name': 'SQLAlchemy', 'type':'data', 'desc': 'A database library. Some love it others hate it.'},

'BeautifulSoup': {'name': 'BeautifulSoup','type':'util', 'desc': 'Xml and html parsing library. Useful for beginners.'},
'IPython': {'name': 'IPython', 'type':'util', 'desc': 'python prompt on steroids. It has completion, history, shell \n\t    capabilities, and a lot more.'},
'nose': {'name': 'nose', 'type':'util', 'desc': 'A testing framework for python. For test driven development.'},
'nltk': {'name': 'nltk', 'type':'util', 'desc': 'Natural Language Toolkit. Useful for string manipulation. '},
'pywin32': {'name': 'pywin32', 'type':'util', 'desc': 'Provides methods and classes for interacting with windows.'},

'Pygame': {'name': 'Pygame', 'type':'game_dev', 'desc': '2d game development library.'},
'Pyglet': {'name': 'Pyglet', 'type':'game_dev', 'desc': 'A 3d animation and game creation engine. Python port of minecraft \n\t    was made with this.'},
}

class Module:
    def __init__(self, moduleName):
        self.name = moduleData[moduleName]['name']
        self.desc = moduleData[moduleName]['desc']
        self.type = moduleData[moduleName]['type']
        self.updateModuleColors()
    
    def updateModuleColors(self):
        if self.name in sys.modules:
            self.installed = True
            self.iString = '(Installed)'
            self.color = col.LT_BLUE
        else:
            self.installed = False
            self.iString = '(NOT Installed)'
            self.color = col.LT_RED

def Menu():
    os.system('clear')
    looping = True
    
    # ml for moduleList
    ml = []
    # tl for type list
    tl= ['data', 'game_dev', 'graphics', 'math', 'networking', 'util']
        
    #load module list
    for module in moduleData:
     #   print(module)
        temp = Module(module)
        ml.append(temp)

    ml.sort(cmp = lambda x, y: cmp(x.name, y.name))
    
    s = InputSwitch(ml, tl)
    #updateSwitch(modules)
    while looping is True:
        print(col.LT_BLUE + " Setup Python Modules")
        print(col.LT_BLUE + " Menu")
        print(col.LT_BLUE + " *********************************************")
        print(col.LT_GREEN + " a) Install PIP")
        print(col.LT_GREEN + " b) Install ALL!")
        print(col.LT_GREEN + " Choose package category:")
        for j in range(0, len(tl)):
            print("\t" + str(j+1) + ") " + tl[j])
        
        print(col.LT_RED + " x) Exit")
        print(col.LT_GREEN + "\n Please make a selection: ", end='')
        
        userInput = raw_input()
        
        #check to see if user entered a number, swap the value for the switch-case
        if not userInput.isalpha() and (int(userInput) < len(tl)+1 and int(userInput) > 0 ):
            userInput = tl[int(userInput)-1]
            looping = s.case_choose_module(userInput)
        else:                
            sys.stdout.flush()
            looping = s.switch(userInput)
        #looping = False
    
        
#os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
#os.system('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080')
#Better yet, you can use subprocess's call, it is safer:

#from subprocess import call
#call('ls')

def main():
    #CheckInstallPip()
    Menu()

if __name__ == "__main__":
    main()
