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

import cpmapi as c_api
import pcp
from pcp import pmapi
from pcp import pmi

NAME = "test"

class _Options(object):
    def __init__(self):
        self.opts = self.setup()
        self.path = os.path.join(pmapi.pmContext.pmGetConfig('PCP_SYSCONF_DIR'),
                            NAME, NAME + ".conf")

    def setup(self):
        """Setup default command line argument option handling."""
        opts = pmapi.pmOptions()

def main():
    global opts
    opts = _Options()
    print opts.path
    print pcp.__doc__
    help(help)
    #help(pmi)
    #help(pcp)
    #help(c_api)
    #help(pmapi)


if __name__ == '__main__':
    main()
