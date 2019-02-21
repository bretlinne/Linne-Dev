# Linne-Dev-WIP
Repo for my development works-in-progress.
Not meant for public release

## Reference to Scripts With Particular Python Functions
* emptyTrash.py
    - __os.path.expanduser('~')__<br />
        Get the value of $HOME on any particular machine to pre-pend to a path
    - __if os.listdir(path[:-1]) == []__<br />
        This checks if a dir is empty.  The [:-1] is to slice off the last char
        of the path string.
    - __subprocess.check_call(command + filePath, stderr=subprocess.STDOUT, shell=True)__<br />
        Call a arbitrary shell command.  Stderr goes to console output.
<br />
* setupVSCode.py
    - __IsDownloadable()__<br />
        uses __requests__ library to get the headers of a URL and checks content-type 
        for downloadability (currently just checks 'text' vs 'html')
    - __DownloadVSCodePkg(url)__<br />
        Downloads a file from a URL.  Opens it in the Downloads dir of the machine and
        uses the 'write binary' method.
    - __pipeToDevNull = open(os.devnull, 'w')__<br />
        USAGE: subprocess.check_call("ls " + outputName, stdout=pipeToDevNull, stderr=pipeToDevNull, shell=True)
    - __subprocess.check_call__<br />
        USAGE: 
        ```
        try:
            subprocess.check_call("ls " + outputName, stdout=pipeToDevNull, stderr=pipeToDevNull, shell=True)
            return True
        except subprocess.CalledProcessError:
            return False
        ```
