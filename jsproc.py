#!/usr/bin/env python3

import sys
import json


class Profile():
    '''
    EEP management
    '''
    def __init__(self, jsfile="D2-14-41.json"): # default file name
        self.json = open(jsfile, 'r')
        self.top = json.load(self.json)

        self.outputlist = {}

        self.SZ = 8
        self.SEVEN = 7

    def printall(self):
        print()
        print(self.top['EepDefinitions']['profile'])
        print(self.top['EepDefinitions']['title'])
        print()

        temp_prof = self.top['functions']['DataName']

        #for v in ["TP", ... ] #function
        #    print(v)

    def add_outiems(self, item_name, seq):
        self.outputlist[item_name] = seq

    def operation(self, data):
        '''
        Main process to handle data and output

        df['ValueType'],
        df['DataName'],
        df['ShortCut'],
        df['BitOffs'],
        df['BitSize'],
        df['RangeMin'],
        df['RangeMax'],
        df['ScaleMin'],
        df['ScaleMax'],
        df['Unit']
        '''

        for df in self.datafields:
            if 'slope' not in df:
                df['slope'] = self.calc_a(df['RangeMin'], df['ScaleMin'], df['RangeMax'], df['ScaleMax'])
            if 'offset' not in df:
                df['offset'] = self.calc_b(df['RangeMin'], df['ScaleMin'], df['RangeMax'], df['ScaleMax'])

            partialData = (int) self.get_bits(data, df['BitOffs'], df['BitSize'];

            if df['ValueType'] == vt_data:
                value = partialData * slope + offset
            else:
                value = partialData;

            if df['ShortCut'] in self.output_list:
                output(df['ShortCut'], value)


    def calc_a(self, r_min, s_min, r_max, s_max):
        return (y1 - y2) / (x1 - x2)

    def calc_b(self, r_min, s_min, r_max, s_max):
        return (x1 * y2 - x2 * y1) / (x1 - x2)

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
    JSProc main
    '''
    print("start")

    eep = Profile()
    eep.printall()
        
if __name__ == "__main__" :
    main()
