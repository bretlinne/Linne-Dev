import binascii

#python imaging library
from PIL import Image
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

class Chunk:
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
	header=''
	Chunks=[]
	FileName=''
	data=''
	width=''
	height=''
	
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
		
	def __init__(self, file):
		self.FileName=file
		file=open(self.FileName, 'r')
		data=file.read()
		data=binascii.hexlify(data)
		vals=self.bytes(data)
		self.data=vals
		self.header=self.data[:8]
		self.header=''.join(self.header)
		self.Find_Chunks()
		file.close

#pix1=PNG('/home/bcuser/Git/Linne-Dev/pyProjects/pico_1pix.png')
pico8=PNG('/home/bcuser/Git/Linne-Dev/pyProjects/picoRGB_2.png')
#timg=PNG('/home/bcuser/Git/Linne-Dev/pyProjects/t-img.png')
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
	return '{:02x}{:02x}{:02x}'.format(r, g, b)
    
img = Image.open('/home/bcuser/Git/Linne-Dev/pyProjects/testAlex.png')
#rgb_img = img.convert('L')
pixels=list(img.convert('RGB').getdata())
print "\n"
byteString=""

for r, g, b, in pixels:
	byteString+=longHex[rgb2hex(r,g,b)]
#r, g, b = rgb_im.getpixel((0, 1))

print byteString

#print "foo:", longHex['f7ec2f']

img.close



#print "\n  chunk binary:\t", pico8.Chunks[foo-3].data
