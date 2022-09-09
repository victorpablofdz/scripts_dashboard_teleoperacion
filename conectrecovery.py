#!/usr/bin/env python

import sys
sys.path.append('..')
import logging

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import socket
import pyads
import dash_class 
# CREATE A ROUTER COMUNICATION WITH TWINCAT
plc = pyads.Connection('127.0.0.1.1.1', 851)
plc.open()


#logging.basicConfig(level=logging.INFO)

ROBOT_HOST = '169.254.12.28'
ROBOT_PORT = 30004
config_filename = 'control_loop_configuration.xml'


dash_port=29999
dashboard=dash_class.DashBoard_Communication('169.254.12.28')
#s = socket.socket()


keep_running = True
prev=1
logging.getLogger().setLevel(logging.INFO)

conf = rtde_config.ConfigFile(config_filename)
state_names, state_types = conf.get_recipe('state')
setp_names, setp_types = conf.get_recipe('setp')
watchdog_names, watchdog_types = conf.get_recipe('watchdog')

con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)

try:

    con.connect()
    print("Conexión con la controladora recuperada")
    plc.write_by_name("Capture_states.connection_ok", True,pyads.PLCTYPE_BOOL)

except:
    print("No se pudo reestablecer la conexión con la controladora, revise la conexión e inténtelo de nuevo")
    plc.write_by_name("Capture_states.connection_ok", False,pyads.PLCTYPE_BOOL)
con.send_pause()

con.disconnect()
plc.close





















