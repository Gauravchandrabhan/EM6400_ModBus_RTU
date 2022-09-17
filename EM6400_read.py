import time
import pymodbus 
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder as decode
from pymodbus.payload import BinaryPayloadBuilder as builder
from pymodbus.compat import iteritems

try:
    client = ModbusClient(method ='rtu',port='COM2',stopbits=2, bytesize=8, parity='N', baudrate=9600)
    client.connect()
except:
    print("Unable to connect to the Com Port, Please try Again \n")
# w = client.write_register(40001, 10, unit=1)
while 1:
    #Average Current Values
    A=client.read_holding_registers(address=3913, count=2, unit =1)
    # print(A.registers)
    A_d = decode.fromRegisters(A.registers, byteorder=Endian.Big, wordorder=Endian.Big)
    A_d ={'Current':A_d.decode_32bit_float(),}

    #Line to line average Voltage Values
    VLL=client.read_holding_registers(address=3907, count=2, unit =1)
    # print(VLL.registers)
    VLL_d = decode.fromRegisters(VLL.registers, byteorder=Endian.Big, wordorder=Endian.Big)
    VLL_d ={'Voltage':VLL_d.decode_32bit_float(),}

    #Active power, total
    W=client.read_holding_registers(address=3903, count=2, unit =1)
    # print(W.registers)
    W_d = decode.fromRegisters(W.registers, byteorder=Endian.Big, wordorder=Endian.Big)
    W_d ={'Power':W_d.decode_32bit_float(),}

    #Forward active Energy Values
    E=client.read_holding_registers(address=3961, count=2, unit =1)
    # print(E.registers)
    E_d = decode.fromRegisters(E.registers, byteorder=Endian.Big, wordorder=Endian.Big)
    E_d ={'Energy':E_d.decode_32bit_float(),}

    print ("-------------")
    timestamp = time.strftime('%H:%M:%S %d-%m-%Y')
    print (timestamp)

    for name, value in iteritems(A_d):
        print ("%s\t" % name, value)
        A=value

    for name, value in iteritems(VLL_d):
        print ("%s\t" % name, value)
        VLL=value
    
    for name, value in iteritems(W_d):
        print ("%s\t" % name, round(value,2))
        W=value
    
    for name, value in iteritems(E_d):
        print ("%s\t" % name, round(value,1))
        E=value

    time.sleep(5)

client.close()