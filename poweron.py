

import dash_class
import socket               # Import socket module
import time 
import pyads


plc = pyads.Connection('127.0.0.1.1.1', 851)
plc.open()



try:
    plc.write_by_name("power_on.poweronerror",False,pyads.PLCTYPE_BOOL)
    s = socket.socket()         # Create a socket object
    host = '169.254.12.28' # Get local machine name
    port = 29999                # Reserve a port for your service.

    s.connect((host, port))
    print (s.recv(1024))

    data="power on\n"
    s.send(data.encode())
    print (s.recv(1024))

    data="load /programs/tfm/test1.urp\n"
    s.send(data.encode())
    print (s.recv(1024))

    time.sleep(10)
    data="power on\n"
    s.send(data.encode())
    print (s.recv(1024))
    time.sleep(10)
    data="brake release\n"
    s.send(data.encode())
    print (s.recv(1024))

    time.sleep(30)
    data="play\n"
    s.send(data.encode())
    print (s.recv(1024))


    plc.write_by_name("Capture_states.robot_init",True,pyads.PLCTYPE_BOOL)
    plc.write_by_name("power_on.poweronerror",False,pyads.PLCTYPE_BOOL)
    print("Encendido finalizado con éxito")

except: 
    print("No ha sido posible completar el proceso, revise todas las conexiones y vuelva a intentarlo")
    plc.write_by_name("power_on.poweronerror",True,pyads.PLCTYPE_BOOL)

plc.close
s.close()                     # Close the socket when done