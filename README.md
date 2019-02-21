# Linne-Dev-WIP
Repo for my development works-in-progress.
Not meant for public release

## Reference to Scripts With Particular Python Functions
* emptyTrash.py
    - __os.path.expanduser('~')__
        Get the value of $HOME on any particular machine to pre-pend to a path
    - __if os.listdir(path[:-1]) == []__
        This checks if a dir is empty.  The [:-1] is to slice off the last char
        of the path string.
    - __subprocess.check_call(command + filePath, stderr=subprocess.STDOUT, shell=True)__
        Call a arbitrary shell command.  Stderr goes to console output.
