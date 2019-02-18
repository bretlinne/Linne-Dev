""" Outputs a bunch of data about the PNG.   Not currently
used in the pico8-png-to-hex project.

May be useful later.
"""

def bar():
    # create a variable to store the test image path
    # pix1=PNG('/home/bcuser/Git/Linne-Dev/pyProjects/pico_1pix.png')
    pico8=PNG('/home/bcuser/Git/Linne-Dev-WIP/pyProjects/picoRGB_2.png')
    # timg=PNG('/home/bcuser/Git/Linne-Dev/pyProjects/t-img.png')
    '''
    print "pix1:\n", "  width:\t", pix1.width,
    print "\n  height:\t", pix1.height,
    print "\n  chunk count:\t", len(pix1.Chunks),
    foo = len(pix1.Chunks)
    for i in pix1.Chunks:
        print "\n  chunk binary:\t", i.data
    '''

    #i believe this is the color chunk
    #print "\n  chunk binary:\t", pix1.Chunks[foo-3].data
    foo = len(pico8.Chunks)
    for i in pico8.Chunks:
        print "\n  chunk type:\t", i.type, "\tbyte Length: ", i.Length,
        
        if i.type == 'IHDR':
            print "\n\tchunk data:\t", i.data,
            print "\n\tchunk data:\t", i.CRC,
    #pri
        
        if i.type == 'pHYs':
            print "\n\tchunk data:\t", i.data,
            print "\n\tchunk data:\t", i.CRC,
        if i.type == 'IDAT':
            print "\n\tchunk data:\t", i.data,
    #print "\n  chunk binary:\t", pico8.Chunks[foo-3].data
