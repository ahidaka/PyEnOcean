#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket
from enocean.protocol.constants import PACKET, RORG
import sys
import traceback
import json
import logging

class Usage():
    '''
    Usage print
    '''
    usage_line = [    
        "    usage:",
        "    pymulti.py [options...] [TP HU IL...(point name)] [JSON EEP definition file (*.json)]",
        "",
        "output example:",
        "",
        "TP=28.5,HU=65.0,IL=515.6,...",
        "TP=27.0,HU=67.0,IL=620.0,...",
        "...",
        "",
        "options:",
        "    [-u]  add unit to displsy",
        "    [-j]  output with json format",
        "    [-c]  output with CSV format (default)",
        "    [-p]  output with prefix point name at CSV (default)",
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

    @staticmethod
    def printall():
        for line in usage_line:
            print(line)


class SystemControl():
    '''
    Analyse start up parameters
    '''
    logger = logging.getLogger('enocean.PyMulti.SystemControl')
    json_file = "D2-14-41.json"

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
            #print(i)
            #print(': ', arg)
            #print(': ', type(arg))
            c = ''
            option = ''

            if arg[0] == '-' or arg[0] == '+':
                #print("opt<" + arg[0] + "> found") ####
                oprion = arg[0]
                c = arg[1]
                self.set_flag(c, option)

            elif type(arg) is str and arg.endswith(('.json', '.JSON')):
                self.json_file = arg
                #print("json<" + arg + "> found") ####

            elif arg == 'help' or arg.endswith('?'):
                Usage.printall()

            elif i != 0:
                #print("other<" + arg + "> found") ####
                self.logger.debug('point:' + arg)
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


class Profile():
    '''
    EEP management
    '''
    logger = logging.getLogger('enocean.PyMulti.Profile')

    def __init__(self, jsfile="D2-14-41.json"): # default file name
        self.json = open(jsfile, 'r')
        self.top = json.load(self.json)
        self.output_list = {}
        self.data_fields = {}
        self.logger.debug('jsfile(%s) load completed.' % jsfile)
        self.SZ = 8
        self.SEVEN = 7

    def print_test(self):
        print()
        print(self.top['EepDefinitions']['profile']) ##sample
        print(self.top['EepDefinitions']['title']) ##sample
        print(self.top['EepDefinitions']['functions']) ##sample
        print()

    def convert(self):
        self.data_fields = self.top['EepDefinitions']['functions']
        for df in self.data_fields:
            #print()
            #print('SC:' + df['ShortCut'])
            #print('RI:' + df['RangeMin'])
            #print('RA:' + df['RangeMax'])
            #print('SI:' + df['ScaleMin'])
            #print('SA:' + df['ScaleMax'])
            #print()
            df['slope'] = self.calc_a(df['RangeMin'], df['ScaleMin'], df['RangeMax'], df['ScaleMax'])
            df['offset'] = self.calc_b(df['RangeMin'], df['ScaleMin'], df['RangeMax'], df['ScaleMax'])
            #print('SL:{}'.format(df['slope']))
            #print('OF:{}'.format(df['offset']))
            #print()
        self.logger.debug('convert:done')

    def print_datafields(self):
        i = 0
        for df in self.data_fields:
            print('%d: %s=%s' % (i, df['ShortCut'], df['DataName']))
            i += 1

    def add_outitems(self, item_name, seq):
        self.output_list[item_name] = seq

    def print_outitems(self):
        for k, v in self.output_list.items():
            self.logger.debug('print_outitems:%s=%d' % (k, v))

    def operation(self, data):
        '''
        Main process to handle data and output

        df['ValueType'],
        df['DataName'],
        df['ShortCut'],
        df['Bitoffs'],
        df['Bitsize'],
        df['RangeMin'],
        df['RangeMax'],
        df['ScaleMin'],
        df['ScaleMax'],
        df['Unit']
        '''

        self.logger.debug('operation:')

        for df in self.data_fields:

            ####print('SC=' + df['ShortCut']) ####

            partialData = self.get_bits(data, int(df['Bitoffs']), int(df['Bitsize']))
            if df['ValueType'] == "Data":
                value = partialData * df['slope'] + df['offset']
            else:
                value = partialData

            #######################################
            print("%s: %f = %d * %f + %f" % (df['ShortCut'], value, partialData, df['slope'], df['offset']))
            #######################################

            if df['ShortCut'] in self.output_list:
                self.logger.debug('operation:point=' + df['ShortCut'])
                print('%s=%d' % (df['ShortCut'], value))

    def calc_a(self, x1, y1, x2, y2):
        return (float(y1) - float(y2)) / (float(x1) - float(x2))

    def calc_b(self, x1, y1, x2, y2):
        return (float(x1) * float(y2) - float(x2) * float(y1)) / (float(x1) - float(x2))

    def get_bits(self, inArray, start, leng):
        """
        getbits: How to get some bits from a byte array.
        """
        ul = 0
        startBit = start % self.SZ
        startByte = start / self.SZ
        posInArray = int(startByte)
        dataInArray = 0
        i = 0

        pos = startBit
        #for (i = 0; i < leng; i+=1):
        for i in range(leng):
            ul <<= 1
            dataInArray = inArray[posInArray]
            ul |= (dataInArray >> (self.SEVEN - pos)) & 1
            pos += 1
            if pos >= self.SZ:
                pos = 0
                posInArray += 1
        return ul


def main():
    '''
    PyMulti main
    '''
    print('PyMulti...')
    logger = logging.getLogger('enocean.PyMulti.main')

    try:
        import queue
    except ImportError:
        import Queue as queue

    #init_logging(level=logging.NOTSET)
    init_logging(level=logging.DEBUG)
    #init_logging(level=logging.INFO)
    #init_logging(level=logging.WARNING)

    sc = SystemControl()
    sc.setup()
    #usage = Usage()
    #usage.printall()

    logger.debug('jsfile:<%s>' % sc.json_file)

    eep = Profile(sc.json_file)
    eep.convert()

    for k, v in sc.point_lists.items():
        eep.add_outitems(k, 1)

    eep.print_outitems()
    eep.print_datafields()

    #print()

    #print('flags')
    #sc.print_flagall()
    #print()

    #print('points')
    #sc.print_pointall()
    #print()

    #print('json_file')
    #print(sc.json_file)
    #print()

    communicator = SerialCommunicator(port='/dev/ttyUSB0')
    communicator.start()

    # endless loop receiving radio packets
    while communicator.is_alive():
        try:
            # Loop to empty the queue...
            packet = communicator.receive.get(block=True, timeout=1)

            if packet.packet_type == PACKET.RADIO_ERP2:
                print('Packet ERP2: %02X' % packet.rorg)

            #print('*** packet ***')
            #print(packet)
            #print('***        ***')

            if packet.packet_type == PACKET.RADIO_ERP2:
                if packet.rorg == RORG.VLD:
                    print('ERP2 VLD found')

                    if len(packet.data) == 15:
                        # shuld be a multi sensor
                        #print('@%s' % ([hex(o) for o in packet.data]))
                        eep.operation(packet.data[5:])

                elif packet.rorg == RORG.BS4:
                    print('ERP2 4BS found')
                    # parse packet with given FUNC and TYPE
                    for k in packet.parse_eep(0x02, 0x05):
                        print('%s: %s' % (k, packet.parsed[k]))

                elif  packet.rorg == RORG.BS1:
                    # alternatively you can select FUNC and TYPE explicitely
                    print('ERP2 1BS found')
                    packet.select_eep(0x00, 0x01)
                    # parse it
                    packet.parse_eep()
                    for k in packet.parsed:
                        print('%s: %s' % (k, packet.parsed[k]))

                elif packet.rorg == RORG.RPS:
                    print('ERP2 RPS found')
                    #for k in packet.parse_eep(0x02, 0x02):
                    for k in packet.parse_eep(0x02, 0x04): #Japan, 928MHz (F6-02-04)
                        print('%s: %s' % (k, packet.parsed[k]))

                elif packet.rorg == RORG.UTE:
                    print('ERP2 UTE found')
                    #for k in packet.parse_eep(0x02, 0x02):
                    #for k in packet.parse_eep(0x02, 0x04): #Japan, 928MHz (F6-02-04)
                    #    print('%s: %s' % (k, packet.parsed[k]))

                else:
                    print('ERP2 unkown packet')

        except queue.Empty:
            continue
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc(file=sys.stdout)
            break

    if communicator.is_alive():
        communicator.stop()


if __name__ == "__main__" :
    main()
