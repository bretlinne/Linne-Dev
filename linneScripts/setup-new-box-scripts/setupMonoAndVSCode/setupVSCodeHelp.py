"""
Helper function to display help text if user doesn't know how to use the 
script, or enters a help flag of --help, or -h, --repair, or -r
    USAGE:
        help invoked by user calling script 2+ args, or 
        adding one of the help flags above
        
        getch: Faster UX feature.  Is used to get single character input
        without echoing to stdout or needing the user to press enter.  
""" 
from linneXtermColors import col
import sys

def printHelp():
    showRest = False
    print("""\n\
    {0}SETUP VS CODE HELP
    ************************************************************************
    {2}Usage: python setupVSCode.py <command>
    
    Commands:
        -h|--help       Call help page.  You figured it out.
        -r|--repair     Fix 'install reinstreq half-installed' status. 
                        Invokes: 
                        'sudo dpkg --force-remove-reinstreq --remove code'
        
    This script downloads the most recent version of Microsoft Visual 
    Studio Code places it in the Downloads directory, then invokes dpkg 
    through a shell subprocess call to install it.  If the package 
    installation is interrupted and has a status of 'install reinstreq half-
    installed', there is a method to correct it.
    """.format(col.LT_BLUE, col.LT_GREEN, col.NC))
