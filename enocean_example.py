#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket
from enocean.protocol.constants import PACKET, RORG
import sys
import traceback
import logging

try:
    import queue
except ImportError:
    import Queue as queue


#def assemble_radio_packet(transmitter_id):
#    return RadioPacket.create(rorg=RORG.BS4, rorg_func=0x20, rorg_type=0x01,
#                              sender=transmitter_id,
#                              CV=50,
#                              TMP=21.5,
#                              ES='true')


init_logging()
communicator = SerialCommunicator()
communicator.start()
#print('The Base ID of your module is %s.' % enocean.utils.to_hex_string(communicator.base_id))

#if communicator.base_id is not None:
#    print('Sending example package.')
#    communicator.send(assemble_radio_packet(communicator.base_id))

# endless loop receiving radio packets
while communicator.is_alive():
    try:
        # Loop to empty the queue...
        packet = communicator.receive.get(block=True, timeout=1)

        if packet.packet_type == PACKET.RADIO_ERP2:
            print('Packet ERP2: %02X' % packet.rorg)

        print('*** packet ***')
        print(packet)
        print('***        ***')

        if packet.packet_type == PACKET.RADIO_ERP1:
            if packet.rorg == RORG.VLD:
                packet.select_eep(0x05, 0x00)
                packet.parse_eep()
                for k in packet.parsed:
                    print('%s: %s' % (k, packet.parsed[k]))
            elif packet.rorg == RORG.BS4:
                # parse packet with given FUNC and TYPE
                for k in packet.parse_eep(0x02, 0x05):
                    print('%s: %s' % (k, packet.parsed[k]))
            elif  packet.rorg == RORG.BS1:
                # alternatively you can select FUNC and TYPE explicitely
                packet.select_eep(0x00, 0x01)
                # parse it
                packet.parse_eep()
                for k in packet.parsed:
                    print('%s: %s' % (k, packet.parsed[k]))
            elif packet.rorg == RORG.RPS:
                for k in packet.parse_eep(0x02, 0x02):
                    print('%s: %s' % (k, packet.parsed[k]))

        elif packet.packet_type == PACKET.RADIO_ERP2:
            if packet.rorg == RORG.VLD:
                #packet.select_eep(0x05, 0x00)
                #packet.parse_eep()
                #for k in packet.parsed:
                #    print('%s: %s' % (k, packet.parsed[k]))
                print('ERP2 VLD found')

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
