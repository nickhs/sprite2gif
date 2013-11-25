#!/usr/bin/env python

import sys
import os
import struct
import subprocess


class UnknownImageFormat(Exception):
    pass


def get_image_size(file_path):
    size = os.path.getsize(file_path)

    with open(file_path) as input:
        height = -1
        width = -1
        data = input.read(25)

        if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
            # GIFs
            w, h = struct.unpack("<HH", data[6:10])
            width = int(w)
            height = int(h)
        elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
              and (data[12:16] == 'IHDR')):
            # PNGs
            w, h = struct.unpack(">LL", data[16:24])
            width = int(w)
            height = int(h)
        elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
            # older PNGs?
            w, h = struct.unpack(">LL", data[8:16])
            width = int(w)
            height = int(h)
        elif (size >= 2) and data.startswith('\377\330'):
            # JPEG
            msg = " raised while trying to decode as JPEG."
            input.seek(0)
            input.read(2)
            b = input.read(1)
            try:
                while (b and ord(b) != 0xDA):
                    while (ord(b) != 0xFF):
                        b = input.read(1)
                    while (ord(b) == 0xFF):
                        b = input.read(1)
                    if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                        input.read(3)
                        h, w = struct.unpack(">HH", input.read(4))
                        break
                    else:
                        input.read(int(struct.unpack(">H", input.read(2))[0]) - 2)
                    b = input.read(1)
                width = int(w)
                height = int(h)
            except struct.error:
                raise UnknownImageFormat("StructError" + msg)
            except ValueError:
                raise UnknownImageFormat("ValueError" + msg)
            except Exception as e:
                raise UnknownImageFormat(e.__class__.__name__ + msg)
        else:
            raise UnknownImageFormat(
                "Sorry, don't know how to get information from this file."
            )

    return width, height


def validateImageMagickInstall():
    try:
        return subprocess.check_output('which convert', shell=True)
    except subprocess.CalledProcessError:
        print "[x] It doesn't look like you have ImageMagick installed."
        print "[x] Maybe brew install imagemagick or sudo apt-get install imagemagick will help"


def printHelp():
    print "sprite2gif.py infile [outfile: out.gif] [optional layout: 2x2]"


def run():
    if len(sys.argv) < 2:
        printHelp()
        return

    infile = sys.argv[1]

    outfile = infile.split('.')[0] + '.gif'

    if len(sys.argv) > 2:
        outfile = sys.argv[2]

    layout = '2x2'

    if len(sys.argv) > 3:
        tmp = sys.argv[3]
        if 'x' not in tmp:
            print "[x] Error! Cannot parse dimension. Using default."
        else:
            layout = tmp

    width, height = get_image_size(infile)
    l_width = float(width) / int(layout.split('x')[0])
    l_height = float(height) / int(layout.split('x')[1])

    ret = validateImageMagickInstall()
    if ret is None:
        return

    command = "convert %s -crop %sx%s +repage -set dispose background -loop 0 -set delay 10 %s" % (infile, l_width, l_height, outfile)
    print "[.] Executing: %s" % command

    subprocess.call(command, shell=True)
    print '[.] Saved gif to %s' % outfile

if __name__ == "__main__":
    run()
