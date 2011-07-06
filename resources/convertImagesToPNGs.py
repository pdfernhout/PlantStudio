# meant to be run from the command line in the resource directory, as in:
# python ../convertImagesToPNGs.py 

import glob
import os

bmps = glob.glob("*.bmp")
xpms = glob.glob("*.xpm")
for bmp in bmps:
    os.system("convert %s %s" % (bmp, bmp[:-3] + "png"))
for xpm in xpms:
    os.system("convert %s %s" % (xpm, xpm[:-3] + "png"))
print "done"
