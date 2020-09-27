import os
import sys


def check():
    datafile = file('data/gandhi.txt')
    found = False
    for line in datafile:
        if  'marching' in line:
            found = True
            break

check()
if True:
    print "true"
else:
    print "false"