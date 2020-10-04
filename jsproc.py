#!/usr/bin/env python3

import sys
import json


#print('sys.argv         : ', sys.argv)
#print('type(sys.argv)   : ', type(sys.argv))
#print('len(sys.argv)    : ', len(sys.argv))

print("start")

#i = 0
#for arg in sys.argv:
#    print(i)
#    print(': ', arg)
#    print(': ', type(arg))
#    i += 1


json_open = open('sample.json', 'r')

json_load = json.load(json_open)

#print(json_load)


#print(json_load['section1']['key'])

#"EepDefinitions"
#"profile"

print(json_load['EepDefinitions']['profile'])

for v in json_load.values():
    print(v)
    
