import socket               # Import socket module
import time 
import pyads


plc = pyads.Connection('127.0.0.1.1.1', 851)
plc.open()

s = socket.socket()         # Create a socket object
host = '169.254.12.28' # Get local machine name
port = 29999                # Reserve a port for your service.

s.connect((host, port))
print (s.recv(1024))



data="unlock protective stop\n"
s.send(data.encode())
print (s.recv(1024))

plc.write_by_name("Recuperacion.safetyerror_flag", False,pyads.PLCTYPE_BOOL)
time.sleep(2)



plc.close
s.close()                     # Close the socket when done
