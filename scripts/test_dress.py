#!/usr/bin/env python

import os
import sys
import re
import json
import ast
import subprocess
import bisect
import time
import datetime
import glob

def encloseCharacter(itxt,target,ornament):
    otxt=''
    for ii in range( len(itxt) ):
        if itxt[ii]==target:
            atxt=ornament+itxt[ii]+ornament
        else:
            atxt=itxt[ii]
        otxt+=atxt
    return otxt

if __name__ == "__main__":
    aa="Cheyenne Rack 1"
    bb=encloseCharacter(aa,' ','"')
    print bb,"\n"

