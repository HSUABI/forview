#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from .parser.cmd_line import CmdLine
from .parser import pkt_seed

def main():
    try:
        session_options = CmdLine(sys.argv).parse()
        print(session_options)

    except:
        print("error:")

    finally:
        print("done:")
