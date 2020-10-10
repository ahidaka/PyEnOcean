# PyEnOcean
Basic EnOcean telegram decode tools by Python (Jaoanese ERP2 on ESP3 version)

This tool uses enocean module and modify it by https://github.com/kipe/enocean.

<br/>

## Samples
- enocean_example.py<br/>
    Basic test program for enocean package

- pymulti.py<br/>
    Sample program for Multi Sensor STM550J (Japanese version)

## Install

```sh
$ sudo apt install python3 #if your environment doesn't have Python3 
$ sudo pip3 install enocean
$ sudo chmod 666 /dev/ttyUSB0
```
<br/>

## Usage
```sh
$ ./pymulti.py -\?
PyMulti...
    usage:
    pymulti.py [options...] [TP HU IL...(point name)] [JSON EEP definition file (*.json)]

output example:

TP=28.5,HU=65.0,IL=515.6,...
TP=27.0,HU=67.0,IL=620.0,...
...

options:
    [-u]  add unit to displsy
    [-c]  output with CSV format (default)
    [-p]  output with prefix point name at CSV (default)
    [-l]  accept teach-In telegram by LEARN button

point name:
    TP - Temperature 10
    HU - Humidity
    IL - Illumination
    AS - Acceleration Status
    AX - Acceleration X
    AY - Acceleration Y
    AZ - Acceleration Z
    CO - Contact

Available json eep definition file:
    D2-14-41.json
    D2-14-40.json
    A5-02-05.json
    A5-04-01.json
    A5-04-03.json
    A5-06-02.json
    A5-06-03.json
    A5-14-05.json
    D5-00-01.json
```
<br/>

## Output sample

```sh
$ ./pymulti.py TP HU
PyMulti...
TP=21.60,HU=66.00,
TP=21.70,HU=67.00,
TP=21.70,HU=68.50,
TP=21.70,HU=70.00,
TP=21.70,HU=70.50,
```
