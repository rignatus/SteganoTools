#!/usr/bin/env python
from PIL import Image, ImageMath, ImageColor
import sys, optparse

def encrypt(original, watermark, output):
    if original.endswith('.png') and watermark.endswith('.png'):
        watermark = Image.open(watermark)
        original = Image.open(original)
        watermark = watermark.resize(original.size)

        red, green, blue, alpha = original.split()
        wred, wgreen, wblue, walpha = watermark.split()

        red2 = ImageMath.eval("convert(a&0xFE|b&0x1, 'L')", a = red, b = wred)
        green2 = ImageMath.eval("convert(a&0xFE|b&0x1, 'L')", a = green, b = wgreen)
        blue2 = ImageMath.eval("convert(a&0xFE|b&0x1, 'L')", a = blue, b = wblue)

        out = Image.merge("RGB", (red2, green2, blue2))
        out.save(output)
        print "Completed"
    else:
        print "Incorrect image format"

def decrypt(water, output):
    if water.endswith('.png'):
        colorNames = ['red', 'green', 'blue']
        water = Image.open(water)
        outputs = []
        for colName, color in zip(colorNames, water.split()):
            #print color
            watermark = ImageMath.eval("(a&0x1)*255", a = color)
            watermark = watermark.convert("L")
            outputs.append(watermark)
            #watermark.save(colName + output)
    
        out = Image.merge("RGB", (outputs[0], outputs[1], outputs[2]))
        out.save(output)
        print "Completed"
    else:
        print "Incorrect image format"

def Main():
    parser = optparse.OptionParser('usage %prog : \n' + \
            'To encrypt : -e <evil file> -t <target file> -o <output file>\n' + \
            'To decrypt : -d <target file> -o <output file>')
    parser.add_option('-e', dest='evil', type='string', \
            help='the evil file to be hidden')
    parser.add_option('-t', dest='target', type='string', \
            help='the destination of the hidden image')
    parser.add_option('-o', dest='out', type='string', \
            help='the output file')
    parser.add_option('-d', dest='final', type='string', \
            help='the file to decrypt')

    (options, args) = parser.parse_args()
    if options.evil != None:
        encrypt(options.target, options.evil, options.out)
    elif options.final != None:
        decrypt(options.final, options.out)
    else:
        print parser.usage
        exit(0)

if __name__ == '__main__':
    Main()
