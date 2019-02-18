"""Helper function to display help text if user doesn't know how to use the 
script, or enters a help flag of --help, -help, --h, or -h
    USAGE:
        help invoked either by user calling script with 0 or 2+ args, or 
        adding one of the help flags above
        
        getch: Faster UX feature.  Is used to get single character input
        without echoing to stdout or needing the user to press enter.  
""" 
from linneXtermColors import col
import sys
import getch

# USAGE: input = getch()
getch = getch.exportGetch

longHexHelpList = [
"000000",
"1c2b53",
"7f2454",
"008751",
"ab5236",
"60584f",
"c3c3c6",
"fff1e9",
"ed1b51",
"faa21b",
"f7ec2f",
"5dbb4d",
"51a6dc",
"83769c",
"f176a6",
"fcccab"
]

def printHelp():
    showRest = False
    print """\n\
    {0}PICO8-PNG-TO-HEX.PY HELP
    *******************************************************************************
    {2}This script requires one .png file input.  Include it in the command line as:
    Usage: {0}thisScript {1}<path and file>
    {2}
    If the path is in the same directory as the script it would be thus:
    {0}pico8-png-to-hex.py {1}./foo.png{2}
    
    TEST IT OUT:
    There is a file "p8Test.png" in this project folder.  Try that:
    {0}pico8-png-to-hex.py {1}./p8Test.png{2}
        Expected output: 0123456789abcdef
        
    LIMITATIONS:
    specifically constructed for the pico-8 palette.  Image can be drawn from 
    anywhere, but the values of the colors must correspond to these:
    """.format(col.LT_BLUE, col.LT_GREEN, col.NC)
    i=0
    for v in range(0, len(longHexHelpList)):
        i+=1
        c="#" + longHexHelpList[v];
        sys.stdout.write("    " + unichr(0x2588) + " " + longHexHelpList[v] + " - " + str(v) + "\t")
        if (i==4):
            print("")
            i=0
    
    sys.stdout.flush()
    
    print("\n    Press " + col.LT_GREEN + "[H]" + col.NC + " to expand \"Consumption by Pico-8\" Help.\n")
    
    userInput = getch()
    
    if userInput == 'h':
        showRest = True
        print """\
        {0}Consumption by Pico-8                        {1}NOTE: Pico-8 uses Lua-based script{0}
        *******************************************************************************
        {2}Copy the output string and paste into the pico-8 to be drawn to the game screen.\n
        {1}Example data structure usage in the Pico-8:{2}
        sprite={{
            test={{bytes={{"0123456789abcdef"}},
            inv=col.null,
            w=4}}
        }}
        where   bytes: is the hex string from this script
                inv: a color between 0 and f that will not be drawn
                w: width if the sprite in pixels
        """.format(col.LT_BLUE, col.LT_GREEN, col.NC)

    if showRest is True:
        print("\n    Press " + col.LT_GREEN + "[H]" + col.NC + " to expand \"Pico-8 Draw Function\" Example.")
        
        userInput = getch()
        
        if userInput == 'h':
            print """\n\
            {1}Example draw function in Pico-8:             
            *******************************************************************************{2}
            draw_sprite=function(self)
                local name = self.sprite_name
                local draw_x=self.x
                local draw_y=self.y
                local name=sprite[name]
                local inv=name.inv or 0
                local f=self.curr_frame

                for i=1,#name.bytes[f] do
                    --bound draw area by tile width
                    if (draw_x-self.x_orig)%self.w==0 then draw_y+=1 draw_x=self.x end

                    --get ea char of byte str
                    local byte=sub(name.bytes[f],i,i)

                    --check if hex val, convert
                    if tonum(byte)==nil then
                        local temp=unhex(byte,1) 
                        byte=temp[1]
                    end
                    if tonum(byte)~=inv or inv==col.null then
                        pset(draw_x,draw_y,byte)
                    end
                    draw_x+=1
                end --end for
            end --end draw function""".format(col.LT_BLUE, col.LT_GREEN, col.NC)
            showRest = False

#Linne's notes:
'''
this is the way the data is stored linearly in the pico.png img.  This is
very strange.  I don't get why it's oganized this way.  No particular way 
this makes sense.  I would have thought that it would be 0-f in a linear
order, since the image is constructed exactly that way:
0123
4567
89ab
cdef
000000 - 0
1c2b53 - 1
7f2454 - 2
008751 - 3
ab5236 - 4
60584f - 5
c3c3c6 - 6
fff1e9 - 7
ed1b51 - 8
faa21b - 9
f7ec2f - a(10)
5dbb4d - b(11)
51a6dc - c(12)
83769c - d(13)
f176a6 - e(14)
fcccab - f(15)
'''
