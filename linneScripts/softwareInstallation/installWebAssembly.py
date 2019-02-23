"""
Python 3 script
Clones the Web Assembly git repo and installs it.
Currently works on Ubuntu 
"""
import os               # path.join
import sys              # used to set arguments for executing a file during setup
import subprocess       # used to invoke git clone
import platform         # detect OS
import shutil           # move cloned repo; avoids issues of cloning into a non-empty ~/Git dir


from pprint import pprint
from subprocess import check_output


#This function should not run on Windows.
import os, shutil, glob, platform
def MoveAllFilesInDir(srcDir, dstDir):
    # detect windows
    if os.name == 'nt':
        osSlash = '\\'
    else:
        osSlash = '/'
    
    if os.path.isdir(srcDir) and os.path.isdir(dstDir):
        #first check if anything in the srcDir.  Only move if stuff in there
        if not os.listdir(srcDir) == []: 
            print('\nMoving Web Assembly repo from: ' + srcDir + ' =>')
            #iterate of all normal files in source dir
            for doc in glob.glob(srcDir + osSlash + '*'):
                print(' =>' + doc) 
                shutil.move(glob.glob(doc)[0], dstDir)
            
            #iterate through the hidden files and move them too
            for doc in glob.glob(srcDir + osSlash + '.*'):
                print(' =>' + doc) 
                shutil.move(glob.glob(doc)[0], dstDir)
        else: 
            print('Nothing to move from ' + srcDir)        
    else:
        print('srcDir & dstDir need to both be valid directories')
        
def ManageDirectories(gitDirPath, tempDir, gitDirEmpty):
    # check if ~/Git exists.  If not, mkdir
    if not (os.path.isdir(gitDirPath)):
        gitDirEmpty = True
        os.mkdir(gitDirPath, 0o0777)
        print('Creating ~/Git directory')
    
    # if ~/Git exists, check if empty
    else:
        print('~/Git dir exists.')
        if (os.listdir(gitDirEmpty) == []):
            gitDirEmpty = True
        else:
            gitDirEmpty = False
        
        #if not empty, we need a temp folder to clone to
        if not gitDirEmpty:
            # if the temp folder is there, blow it away, make new
            if os.path.isdir(tempDir):
                shutil.rmtree(tempDir)
                os.mkdir(tempDir, 0o0777)
                print('Trashing ' + tempDir + '; making new...')
            # if not there, make it
            else: 
                os.mkdir(tempDir, 0o0777)
                print('Creating ' + tempDir)
                
    return gitDirEmpty
            
def SetupDestDir(gitDestDir):
    """
    Create a destination directory in ~/Git if it doesn't exist
    """
    destEmpty = True
    # setup the gitDestDir in ~/Git if doesn't exist
    if not (os.path.isdir(gitDestDir)):
        os.mkdir(gitDestDir, 0o0777)
    # if it's there, check if it's empty
    else:
        if not os.listdir(gitDestDir) == []:
            destEmpty = False
            print(gitDestDir + ' is not empty!\n')
            answer = input('Do you want to delete it and create a new one? >')
            if answer.lower() == 'y' or answer.lower() == 'yes':
                shutil.rmtree(gitDestDir)
                os.mkdir(gitDestDir, 0o0777)
            else:
                exit();
    return destEmpty

def CleanUpTemp(tempDir):
    """
    Trash the temp folder if it was properly emptied
    """
    if not os.listdir(tempDir) == []:
        print('Something did not get moved properly from ' + tempDir)
        print('Aborting cleanup.  Do your own dirty work.')
    else:
        shutil.rmtree(tempDir)
    
def CloneRepo(gitDirEmpty, gitCloneCommand, tempDir, gitDestDir):
    # if the ~/Git is empty, clone straight into it.
    if gitDirEmpty == True:
        # clone the git repo
        subprocess.call(gitCloneCommand, shell=True)
        print('Cloning the Web Assembly repo into:\n' + gitDirPath)
        
    # if not empty, things are more complicated.
    elif gitDirEmpty == False:            
        #clone the repo to the temp folder            
        subprocess.call('sudo ' + gitCloneCommand + ' ' + tempDir, shell=True)
        print('Cloning the Web Assembly repo into:\n' + tempDir)
            
        # move the repo folder to ~/Git
        MoveAllFilesInDir(tempDir, gitDestDir)
        
        CleanUpTemp(tempDir)
        
    # odd chance that girDirEmpty is still 'None'
    else:
        print('Cannot determine state of ~/Git dir.  Go fish.')
    
def main():
    linuxDistro = platform.linux_distribution()
    OSType = linuxDistro[0]
    
    if OSType == 'Ubuntu':
        # -------------------------------------------------
        # DECLARATIONS
        # -------------------------------------------------
        # construct git repo path
        command = 'git clone '
        repoSourcePath = 'https://github.com/juj/emsdk.git'
        gitCloneCommand = command + repoSourcePath
        
        # construct the path to the Git directory
        HOME = os.path.expanduser('~')
        gitDirPath = os.path.join(HOME, 'Git')
        
        gitDirEmpty = None
        
        # install directory
        emsdk = 'emsdk'
        installCmd = './emsdk install latest'
        activateCmd = './emsdk activate latest'
        
        # constuct temp folder
        tempDir = os.path.join(HOME, 'Downloads', emsdk)
        gitDestDir = os.path.join(HOME, 'Git', emsdk)
        
        # -------------------------------------------------
        # CALL REPO CLONE METHODS
        # -------------------------------------------------
        # handle setting up the directories for Git, & the temp if needed
#        gitDirEmpty = ManageDirectories(gitDirPath, tempDir, gitDirEmpty)
#        destEmpty = SetupDestDir(gitDestDir)
        
        #clone the repo, move it from temp to ~/Git/emsdk if necessary
#        CloneRepo(gitDirEmpty, gitCloneCommand, tempDir, gitDestDir)
                    
        # setup path for invoking install & activate commands
        emsdkRepoPath = os.path.join(gitDirPath, emsdk)
        
        # -------------------------------------------------
        # SETUP AND INSTALL
        # -------------------------------------------------
        # check if the repo installed correctly
        if (os.path.isdir(emsdkRepoPath)):
            
            # invoke the commands to install
            command = 'python '
            installerPath = os.path.join(emsdkRepoPath, emsdk)
            options = ' install latest'
            
            #subprocess.call(command + installerPath + options, shell=True)
            
            options = ' activate latest'
            #subprocess.call(command + installerPath + options, shell=True)
            
            emsdk_envFile = os.path.join(emsdkRepoPath, 'emsdk_env.sh')
            fooFile = os.path.join(emsdkRepoPath, 'foo.sh')
            options = ' --build=Release'
            command = 'source'

            foo = subprocess.Popen(["/bin/sh", emsdk_envFile, '--build=Release'])
            #subprocess.call(command + ' ' + emsdk_envFile + options, shell=True)            
#            subprocess.call('source /home/bcuser/Git/emsdk/emsdk_env.sh --build=Release', shell=True)
            #with open(emsdk_envFile) as f:
            #    code = compile(f.read(), emsdk_envFile, 'exec')
            #    exec(code, 'Release')
            #sys.argv = ['build', 'Release']
            #exec(open(emsdk_envFile).read(), globals())
            #exec(open(emsdk_envFile).read())

            """
            os.environ['a'] = 'a'*100
            # POSIX: name shall not contain '=', value doesn't contain '\0'
            output = check_output("source the_script.sh; env -0",   shell=True,
                                  executable="/bin/bash")
            # replace env
            os.environ.clear() 
            x=0
            for val in output:
                x+=1
                print(val)
            print('x: ' + str(x))
            #os.environ.update(line.partition('=')[::2] for line in output.split('\0'))
            #pprint(dict(os.environ)) #NOTE: only `export`ed envvars here
            """
        else:
            print('Web Assembly repo clone failed.')
    else:
        print('Other Operating Systems not implemented.')

        
if __name__ == "__main__":
    main()
