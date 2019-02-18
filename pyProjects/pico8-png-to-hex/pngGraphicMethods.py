""" this file stores the graphical functions that are invoked from the main 
script to convert a png file's pixels to a string of hex digits
    USAGE:
        Chunk: class is a data struct for .png graphic data
        PNG: class invokes an instance of Chunk class as it parses through the file
        rgb2hex: method which takes in RB data; converts to a single 6 digit hex string
        longHex: a dictionary of 6 digit hex values as keys with single digit's 
            as values.  This is bcs only 16 colors in pico-8's palette.  
            The 6-digit hex values are the hard-coded color value of those 16 colors
"""

class Chunk:
    """Create data structure for chunks of pixel data read from .png"""
    Length=None
    type=None
    data=None
    CRC=None
    def height_width(self):
        if self.type=='IHDR':
            width=int(self.data[0:8], 16)
            height=int(self.data[8:16], 16)
            return [width, height]

class PNG:
    """create a data structure to parse data about the .png"""
    header=''
    Chunks=[]
    fileName=''
    data=''
    width=''
    height=''
    
    def __init__(self, file):
        self.fileName=file
        file=open(self.fileName, 'r')
        data=file.read()
        data=binascii.hexlify(data)
        vals=self.bytes(data)
        self.data=vals
        self.header=self.data[:8]
        self.header=''.join(self.header)
        self.Find_Chunks()
        file.close
        
    def bytes(self, data):
        vals=[]
        count=0
        step=2
        for i in range(0, len(data), 2):
            vals.append(data[i:step])
            step=step+2
        return vals
        
    def Find_Chunks(self):
        c=Chunk()
        total=0
        while c.type != 'IEND':
            c=Chunk()
            c.Length=int(''.join(self.data[8+total:12+total]),16)
            c.type=''.join(self.data[12+total:16+total]).decode('hex')            
            c.data=''.join(self.data[16+total:15+c.Length+total])
            c.CRC=''.join(self.data[16+c.Length+total:20+c.Length+total])
            w=c.height_width()
            if w:
                self.width=w[0]
                self.height=w[1]
            self.Chunks.append(c)
            
            total=total+c.Length+12

# dictionary for using a particular RGB color string from PNG as key to
# find a corresponding hex value consummable by the Pico-8
longHex={'000000':'0',
        '1c2b53':'1',
        '7f2454':'2',
        '008751':'3',
        'ab5236':'4',
        '60584f':'5',
        'c3c3c6':'6',
        'fff1e9':'7',
        'ed1b51':'8',
        'faa21b':'9',
        'f7ec2f':'a',
        '5dbb4d':'b',
        '51a6dc':'c',
        '83769c':'d',
        'f176a6':'e',
        'fcccab':'f'
}

def rgb2hex(r, g, b):
    """consume RGB data values for a pixel color and format as a 6-digit
    string of hexadecimal values"""
    return '{:02x}{:02x}{:02x}'.format(r, g, b)

