#! /usr/bin/python
# -*- coding: utf-8 -*-
##############################################
### Import definitions                    ####
##############################################
### Python Default modules ###################
import sys
import os

## For opening urls
import urllib
import time

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

##############################################
### Main                                  ####
##############################################
## Create dir
if (not os.path.isdir('html')):
    os.mkdir('html')

## Download comics
print "Downloading comicbooks from cmro.travis-starnes.com"    
for num in range (1,200):
    urllib.urlretrieve("http://cmro.travis-starnes.com/detail.php?idvalue=%d" % (num), "html/comic_book_%d.html" % (num))
    update_progress(num/200)
    time.sleep(2) 
