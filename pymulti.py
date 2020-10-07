#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
import json

class Usage():
    '''
    Usage print
    '''
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


class SystemControl():
    '''
    Analyse start up paarameters and set up at start up
    '''
    def __init__(self):
        self.parameters = {
            #'u' : 0, # output with unit
            #'j' : 0, # json output
            'c' : 1, # CSV output, default
            #'t' : 0, # Timestamp
            #'l' : 0, # Learn for TeachIn
            #'f' : 0, # Filter
            }
        self.point_lists = {}
        self.seq = 0


    def setup(self):
        i = 0
        for arg in sys.argv:
            print(i)
            print(': ', arg)
            print(': ', type(arg))
            c = ''
            option = ''

            if arg[0] == '-' or arg[0] == '+':
                print("opt<" + arg[0] + "> found") ####
                oprion = arg[0]
                c = arg[1]
                self.set_flag(c, option)

            elif type(arg) is str and arg.endswith(('.json', '.JSON')):
            #elif arg.endswith('.JSON'):
                self.json_file = arg
                print("json<" + arg + "> found") ####

            else:
                print("other<" + arg + "> found")
                self.set_point(arg)

            i += 1    

    def set_flag(self, key, option = 1):
        number = 0
        if (type(option) is int):
            number = option
        elif (option == '+'):
            number = 1
        elif (option == '-'):
            number = -1
        if number != 0:
            if key in self.parameters:
                self.parameters[key] += number
            else:
                self.parameters[key] = number

    def get_flag(self, key):
        val = self.parameters.get(key, "")
        return val

    def set_point(self, point):
        self.point_lists[point] = self.seq
        self.seq += 1

    def get_seq(self, point):
        val = self.point_lists.get(point, -1)
        return val

    def print_flagall(self):
        for k, v in self.parameters.items():
            print(k, v)

    def print_pointall(self):
        for k, v in self.point_lists.items():
            print(k, v)


def main():
    '''
    PyMulti main
    '''
    print('PyMulti...')

    sc = SystemControl()
    sc.setup()
    #usage = Usage()
    #usage.printall()
    print()

    print('flags')
    sc.print_flagall()
    print()

    print('points')
    sc.print_pointall()
    print()

    print('json_file')
    print(sc.json_file)
    print()

if __name__ == "__main__" :
    main()
