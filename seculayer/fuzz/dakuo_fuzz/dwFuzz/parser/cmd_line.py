#!/usr/bin/python
# -*- coding: utf-8 -*-

import getopt
#from dwFuzz.session import FuzzSession
from collections import defaultdict

short_opts = ""
long_opts = ""

class CmdLine:
    def __init__(self, argv):
        self.argv = argv

    def parse(self):

        try:
            opts, args = getopt.getopt(self.argv[1:], short_opts, long_opts)
            optsd = defaultdict(list)

        except getopt.GetoptError:
            return args

        #fuzzSess = FuzzSession()
        for opt, arg in opts:
            optsd[opt].append(arg)

        

        print(optsd)


           

