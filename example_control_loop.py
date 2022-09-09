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
con.connect()
dashboard.DashBoard_Connect()
# get controller version
con.get_controller_version()

# setup recipes
con.send_output_setup(state_names, state_types)
#setp = con.send_input_setup(setp_names, setp_types)
#watchdog = con.send_input_setup(watchdog_names, watchdog_types)




#setp.speed_slider_mask=1
#setp.speed_slider_fraction=0.2
#con.send(setp)
  
# The function "rtde_set_watchdog" in the "rtde_control_loop.urp" creates a 1 Hz watchdog
#watchdog.input_int_register_0 = 0


#start data synchronization
if not con.send_start():
    sys.exit()


##########################

#s.connect((ROBOT_HOST,dash_port))
#s.sendall('get_robot_model<lf>')
#        data = s.recv(1024)
#   print('Received', repr(data))

############################
try:
# control loop
    while keep_running:
    # receive the current state
        #try: 
        state = con.receive()
            # con.send(setp)
        plc.write_by_name("Capture_states.connection_ok", True,pyads.PLCTYPE_BOOL)
        #except:
        #    plc.write_by_name("Capture_states.connection_ok", False,pyads.PLCTYPE_BOOL)
  
        if state is None:
        #Se ha interrumpido la conexion
            print("Se ha interrumpido la conexión")
            break
   
        modo=state.robot_mode
        safety_mode=state.safety_mode
        safety_status_bits=state.safety_status_bits
        joint_mode=state.joint_mode
        safety_status=state.safety_status
        robot_status_bits=state.robot_status_bits

        print("Safety status bits is")
        print(safety_status_bits)
        print("Safety mode is")
        print(safety_mode)
        prev=safety_status_bits
        print("robot mode is")
        print(modo)
        #print("Joint mode is")
    #print(joint_mode)
    #print("Safety status is")
    #print(safety_status)
    #print("robot status bits")
    #print(robot_status_bits)
    
        plc.write_by_name("Capture_states.robot_mode", modo,pyads.PLCTYPE_INT)
        plc.write_by_name("Capture_states.safety_mode", safety_mode,pyads.PLCTYPE_INT)
        plc.write_by_name("Capture_states.safety_status", safety_status,pyads.PLCTYPE_INT)
    
    
        plc.write_by_name("Capture_states.robot_status_bits", robot_status_bits,pyads.PLCTYPE_UINT)
    
        plc.write_by_name("Capture_states.safety_status_bits", safety_status_bits,pyads.PLCTYPE_UINT)
    
    
   # plc.write_by_name("Capture_states.joint_modes", joint_mode,pyads.PLCTYPE_INT)
   
    
        if safety_status_bits!=prev :
            status=format(safety_status_bits,'b')
            print("Se ha producido un error")
            print(safety_status_bits)
            print("safety mode es")
            print(safety1)
        #= plc.read_by_name('MAIN.grabacion', pyads.PLCTYPE_BOOL)
        #plc.write_by_name("GVL.int_val", 1)
            for i in range(11):
            
                bit=status[i]
            
                if(status[i]=="1"):
                    print(i)
                    if(i==0):
                        print("Estado de seguridad normal")
                    elif(i==1):
                        print("Estado de seguridad reducido")
                    elif(i==2):
                        print("Parada de protección ")
                    elif(i==3):
                        print("Modo de recuperación")
                    elif(i==4):
                        print("Parada de seguridad del sistema ")
                    elif(i==5):
                        print("Parada de emergencia del robot")
                    elif(i==6):
                        print("Parada de emergencia ")
                    elif(i==7):
                        print("Violacion ")
                    elif(i==8):
                        print("Fallo")
                    elif(i==9):
                        print("Parado por seguridad")

       
        
except:
    print("Se perdió la conexión con el robot")     
    plc.write_by_name("Capture_states.connection_ok", False,pyads.PLCTYPE_BOOL)
        #keep_running=0
      #  s.close()  
       # break
    #print(safety1)
    #print (s.recv(1024).decode())
    


    # kick watchdog
   # con.send(watchdog)

con.send_pause()

con.disconnect()
plc.close