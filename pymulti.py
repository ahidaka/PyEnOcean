#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
import json

class Usage():
    def __init__(self):
        self.usage_line = [    
            "    usage:",
            "    pymulti.py [options...] [TP HU IL...(point name)] [JSON EEP definition file (*.json)]",
            "",
            "output example:",
            "",
            "28.5,65.0,515.6,...",
            "27.0,67.0,620.0,...",
            "...",
            "",
            "options:",
            "    [-u]  add unit to displsy",
            "    [-j]  output with json format",
            "    [-c]  output with CSV format (default)",
            "    [-t]  output with time stamp",
            "    [-l]  accept teach-In telegram by LEARN button",
            "    [-f]  apply telegram filter (after teach-In received)",
            "",
            "point name:",
            "    TP - Temperature 10",
            "    HU - Humidity",
            "    IL - Illumination",
            "    AS - Acceleration Status",
            "    AX - Acceleration X",
            "    AY - Acceleration Y",
            "    AZ - Acceleration Z",
            "    CO - Contact",
            "",
            "Available json eep definition file:",
            "    D2-14-41.json",
            "    D2-14-40.json",
            "    A5-02-05.json",
            "    A5-04-01.json",
            "    A5-04-03.json",
            "    A5-06-02.json",
            "    A5-06-03.json",
            "    A5-14-05.json",
            "    D5-00-01.json",
            ]

    def printall(self):
        for line in self.usage_line:
            print(line)


def main():
    '''
    PyMulti main
    '''

    usage = Usage()
    usage.printall()
    print()

if __name__ == "__main__" :
    main()
