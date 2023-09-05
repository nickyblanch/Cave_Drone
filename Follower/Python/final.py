####################################################################################
# Author: Nicolas Blanchard, nickyblanch@arizona.edu, (520) 834-3191
# Created for Dr. Shkarayev at the University of Arizona
# Date: 1/10/23
# Purpose: Automatic control for follower drone in cave drone project.
# Dependencies: pymavlink, time, threading

# Thank you to ardusub.com Intelligent Quads on YouTube for pymavlink references.


# ADDITIONAL COMMENTS

# Important: In order for this pymavlink script to execute on a ground station computer
# and still communicate with the drone, MAVProxy is required to route the MAVLINK
# messages. The following command should be used to start MAVProxy:

# mavproxy --master=udp:192.168.8.60:14550 --out 127.0.0.1:14551 --out 127.0.0.1:14552
# mavproxy --master=udp:192.168.1.60:14550 --out 127.0.0.1:14551 --out 127.0.0.1:14552 (SEEKER 1)

# mavproxy --master=udp:192.168.1.134:14550 --out 127.0.0.1:14551 --out 127.0.0.1:14552 (MULTI DRONE, SEEKER 1)
# mavproxy --master=udp:192.168.1.124:14550 --out 127.0.0.1:14551 --out 127.0.0.1:14552 (MULTI DRONE, SEEKER 1)

# Then, a ground station (QGroundControl) can connect to UD port 14551 and this
# pymavlink script can connect to UDP port 14552.

# The modalai voxl flight will send its MAVLINK traffic to UDP port 14550 and it
# will be visible on both QGroundControl and this executing pymavlink script.

# Of course, it is also necessary for this ground station computer to be connected
# to the voxl's WiFi AP. For this project, the AP is named 'DRONE' and has a
# password of '123456789'.

# When calibarting sensors, the closest board orientation is: YAW 90 ROLL 90 PITCH 180

# NOTE: In QGroundcontrol, MAVLink forwarding must be enabled and the forwarding address
# must be port 14552.

####################################################################################
# TODO

# 1.) Decrease proportional gain for velocity PID
# 2.) Disable auto-disarm on landing
# 3.) Test course with landing at each corner
# 4.) Increase takeoff alt to 3.28 feet (1 meter)

####################################################################################


from pymavlink import mavutil
import time
import threading


####################################################################################


FLIGHT_MODE = 3         # 0 = test mode: fly to (TEST_MODE_X, TEST_MODE_Y, TEST_MODE_Z)
                        # 1 = manual mode: fly to coordinates provided by user
                        # 2 = autonomous mode: fly to hard-coded coordinates
                        # 3 = demo: fly is a 2x2 meter square at an altitude of 1 meter.

TEST_MODE_X = 1         # target x coordinate in test mode
TEST_MODE_Y = 1         # target y coordinate in test mode
TEST_MODE_Z = -1        # targer z coordinate in test mode

SEND_TELEMETRY = 1      # 1 = send telemtry
                        # 0 = don't send telemtry

LAND = 0                # 1 = landing
                        # 0 = normal operation

TARGET_X = 0            # target x coordinate
TARGET_Y = 0            # target y coordinate
TARGET_Z = -1           # target z coordinate

CURRENT_X = 0           # current x coordinate
CURRENT_Y = 0           # current y coordinate
CURRENT_Z = 0           # current z coordinate


####################################################################################


def main():

    ################################################
    # [no inputs or outputs]
    ################################################

    print("working")

    global TARGET_X
    global TARGET_Y
    global TARGET_Z
    global CURRENT_X
    global CURRENT_Y
    global CURRENT_Z
    global SEND_TELEMETRY

    # Establish MAVLINK connection
    the_connection = setup()

    # Arm the system
    arm(the_connection)

    # Request local coordinates
    request_local_NED(the_connection)

    # Request target local coordinates
    request_target_pos_NED(the_connection)

    # Initialize X, Y, Z
    msg = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True).to_dict()
    x = msg["x"]
    y = msg["y"]
    z = msg["z"]

    # Begin our telemtry thread
    t1 = threading.Thread(target=telemetry_loop_thread, args=(the_connection,))
    t1.start()
    t2 = threading.Thread(target=telemetry_local_position_thread, args=(the_connection,))
    t2.start()

    # Take off
    takeoff_CUSTOM(the_connection, 1)

    # Loop
    print("Entering loop")
    while 1:

        # Note: In order for PX4 to remain in offboard mode, it needs to receive target commands
        # at a rate of at least 2 Hz.
        SEND_TELEMETRY = 1

        # Update current position
        try:
            msg = the_connection.messages['LOCAL_POSITION_NED']
            CURRENT_X = msg.x
            CURRENT_Y = msg.y
            CURRENT_Z = msg.z
            msg_success = True
        except:
            msg_success = False
            print("Problem receiving LOCAL_POSITION_NED Mav message.")

        # Update target position
        if (FLIGHT_MODE == 0):
            # Test mode
            TARGET_X = TEST_MODE_X
            TARGET_Y = TEST_MODE_Y
            TARGET_Z = TEST_MODE_Z
        elif (FLIGHT_MODE == 1):
            # Manual mode
            try:
                TARGET_X, TARGET_Y, TARGET_Z = input("Enter target x y z: ").split()
            except:
                print("Error reading input coordinates.")
            finally:
                print("Going to: " + str(TARGET_X) + ", " + str(TARGET_Y) + ", " + str(TARGET_Z))
        elif (FLIGHT_MODE == 2):
            # Autonomous mode
            pass
        elif (FLIGHT_MODE == 3):

            TARGET_X = 0
            TARGET_Y = 0
            TARGET_Z = -1
            time.sleep(2)
            offboard(the_connection)
            time.sleep(8)

            TARGET_X = 2
            TARGET_Y = 2
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = the_connection.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z
            land(the_connection)
            time.sleep(5)
            takeoff_CUSTOM_coordinates(the_connection, 2, 2, 1)
            time.sleep(5)

            TARGET_X = -2
            TARGET_Y = 2
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = the_connection.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z
            land(the_connection)
            time.sleep(5)
            takeoff_CUSTOM_coordinates(the_connection, -2, 2, 1)
            time.sleep(5)

            TARGET_X = -2
            TARGET_Y = -2
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = the_connection.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z
            land(the_connection)
            time.sleep(5)
            takeoff_CUSTOM_coordinates(the_connection, -2, -2, 1)
            time.sleep(5)

            TARGET_X = 2
            TARGET_Y = -2
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = the_connection.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z
            land(the_connection)
            time.sleep(5)
            takeoff_CUSTOM_coordinates(the_connection, 2, -2, 1)
            time.sleep(5)

            TARGET_X = 2
            TARGET_Y = 2
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = the_connection.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z

            TARGET_X = 0
            TARGET_Y = 0
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = the_connection.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z
            land(the_connection)
            time.sleep(20)

        else:
            print("FLIGHT MODE NOT RECOGNIZED.")
            return


####################################################################################


def setup():

    ################################################
    # the_connection: mavlink connection [output]
    ################################################

    # Start a connection listening on a UDP port
    the_connection = mavutil.mavlink_connection('udp:127.0.0.1:14552')

    # Wait for the first heartbeat 
    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

    return the_connection


def arm(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    ################################################

    # Arm the system
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

    # Wait until arming confirmed (can manually check with the_connection.motors_armed())
    print("Waiting for the vehicle to arm")
    the_connection.motors_armed_wait()
    print('Armed!')


def takeoff(the_connection, alt):

    ################################################
    # the_connection: mavlink connection [input]
    # alt: float, target altitude [input] UNUSED
    ################################################

    # Takeoff command
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, alt)

    # Wait for acknowledge
    # msg = the_connection.recv_match(type='COMMAND<ACK', blocking=True)
    # print(msg)


def takeoff_CUSTOM(the_connection, alt):

    ################################################
    # the_connection: mavlink connection [input]
    # alt: float, target altitude [input]
    ################################################

    global TARGET_X
    global TARGET_Y
    global TARGET_Z

    # Make sure we go up
    if alt > 0:
        alt = alt * -1

    # Initialize X, Y, Z
    msg = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True).to_dict()
    x = msg["x"]
    y = msg["y"]
    z = msg["z"]

    # Set initial target
    TARGET_X = x
    TARGET_Y = y
    TARGET_Z = alt

    offboard(the_connection)


def takeoff_CUSTOM_coordinates(the_connection, x, y, alt):

    ################################################
    # the_connection: mavlink connection [input]
    # alt: float, target altitude [input]
    ################################################

    global TARGET_X
    global TARGET_Y
    global TARGET_Z

    # Make sure we go up
    if alt > 0:
        alt = alt * -1

    # Set initial target
    TARGET_X = x
    TARGET_Y = y
    TARGET_Z = alt

    offboard(the_connection)


def land(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    ################################################

    # Takeoff command
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0, 0)

    # Wait for acknowledge
    # msg = the_connection.recv_match(type='COMMAND<ACK', blocking=True)
    # print(msg)


def update_target_ned(the_connection, x_val, y_val, z_val):

    ################################################
    # the_connection: mavlink connection [input]
    # x_val: float, desired x target [input]
    # y_val: float, desired y target [input]
    # z_val: float, desired z target [input]
    ################################################

    if z_val > 0:
        z_val = z_val * -1

    the_connection.mav.set_position_target_local_ned_send(0, the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, type_mask=(
                # mavutil.mavlink.POSITION_TARGET_TYPEMASK_X_IGNORE |
                # mavutil.mavlink.POSITION_TARGET_TYPEMASK_Y_IGNORE |
                # mavutil.mavlink.POSITION_TARGET_TYPEMASK_Z_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_VX_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_VY_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_VZ_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE |
                # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_FORCE_SET |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_RATE_IGNORE), x=float(x_val), y=float(y_val), z=float(z_val), vx=0, vy=0, vz=0, afx=0, afy=0, afz=0, yaw=0, yaw_rate=0)

    if (FLIGHT_MODE != 1):
        print("TARGET: [" + str(x_val) + ", " + str(y_val) + ", " + str(z_val) + "]")


def request_local_NED(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    ################################################

    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED, 1e6/20, 0, 0, 0, 0, 0)


def request_target_pos_NED(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    ################################################

    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, mavutil.mavlink.MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED, 1e6/20, 0, 0, 0, 0, 0)


def telemetry_loop_thread(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    ################################################

    global TARGET_X
    global TARGET_Y
    global TARGET_Z

    while SEND_TELEMETRY:
        update_target_ned(the_connection, TARGET_X, TARGET_Y, TARGET_Z)

    return 0


def telemetry_local_position_thread(the_connection):

     ################################################
    # the_connection: mavlink connection [input]
    ################################################

    global CURRENT_X
    global CURRENT_Y
    global CURRENT_Z

    while 1:
        try:
            msg = the_connection.messages['LOCAL_POSITION_NED']
            CURRENT_X = msg.x
            CURRENT_Y = msg.y
            CURRENT_Z = msg.z
        except:
            print("Problem receiving LOCAL_POSITION_NED Mav message.")
    

def offboard(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    # mode: int, id of the desired px4 mode [input]
    ################################################

    # master.mav.command_long_send( master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, 0, mode_id, 0, 0, 0, 0, 0)

    
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, 209, 6, 0, 0, 0, 0, 0)

    # while True:
    #     # Wait for ACK command
    #     # Would be good to add mechanism to avoid endlessly blocking
    #     # if the autopilot sends a NACK or never receives the message
    #     ack_msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
    #     ack_msg = ack_msg.to_dict()

    #     # Continue waiting if the acknowledged command is not `set_mode`
    #     if ack_msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
    #         continue

    #     # Print the ACK result !
    #     print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
    #     break


####################################################################################

def debug_test_offboard():
    # Establish MAVLINK connection
    the_connection = setup()

    status = input("Okay for enter offboard?")

    if status != "n" and status != "N":
        while 1:
            offboard(the_connection)
            time.sleep(1)


def debug_test_land():
   ################################################
    # [no inputs or outputs]
    ################################################

    global TARGET_X
    global TARGET_Y
    global TARGET_Z
    global SEND_TELEMETRY
    global LAND
    
    SEND_TELEMETRY = 1
    LAND = 0

    # Establish MAVLINK connection
    the_connection = setup()

    # Arm the system
    arm(the_connection)

    # Take off
    takeoff(the_connection, 0.75)

    # Request local coordinates
    request_local_NED(the_connection)

    # Request target local coordinates
    request_target_pos_NED(the_connection)

    # Enter offboard mode
    # TODO - the command to enter offboard mode does not currently work.
    # More information on PX4 operating mode numbers are required.
    # For now, offboard mode must be invoked manually from QGroundControl.
    
    # offboard(the_connection)

    # Initialize X, Y, Z
    msg = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True).to_dict()
    x = msg["x"]
    y = msg["y"]
    z = msg["z"]

    # Begin our telemtry thread
    t1 = threading.Thread(target=telemetry_loop_thread, args=(the_connection,))
    t1.start()

    # Set initial target
    TARGET_X = 0
    TARGET_Y = 0
    TARGET_Z = -0.5

    # Pause for 7 seconds
    time.sleep(12)

    while 1:
        # Land
        LAND = 1
        time.sleep(1)
        the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0, 0)
       

def debug_test_takeoff():
   ################################################
    # [no inputs or outputs]
    ################################################

    global TARGET_X
    global TARGET_Y
    global TARGET_Z
    global SEND_TELEMETRY
    global LAND
    
    SEND_TELEMETRY = 1
    LAND = 0

    # Establish MAVLINK connection
    the_connection = setup()

    # Arm the system
    arm(the_connection)

    # Request local coordinates
    request_local_NED(the_connection)

    # Request target local coordinates
    request_target_pos_NED(the_connection)

    # Initialize X, Y, Z
    msg = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True).to_dict()
    x = msg["x"]
    y = msg["y"]
    z = msg["z"]

    # Begin our telemtry thread
    t1 = threading.Thread(target=telemetry_loop_thread, args=(the_connection,))
    t1.start()

    # Set initial target
    TARGET_X = x
    TARGET_Y = y
    TARGET_Z = -0.5

    # Pause for 5 seconds
    time.sleep(5)

    while 1:
        # Takeoff
        # Enter offboard mode
        offboard(the_connection)
        time.sleep(100)
       
  

####################################################################################


if __name__ == "__main__":
    main()
    # debug_test_takeoff()

    
####################################################################################
# UNUSED
####################################################################################


# UNUSED
# def update_mode(the_connection, mode):

#     ################################################
#     # the_connection: mavlink connection [input]
#     # mode: string, name of the desired px4 mode [input]
#     ################################################

#     # Check if mode is available
#     if mode not in the_connection.mode_mapping():
#         print('Unknown mode : {}'.format(mode))
#         print('Try:', list(the_connection.mode_mapping().keys()))
#         return

#     # Get mode ID
#     mode_id = the_connection.mode_mapping()[mode]
#     # Set new mode
#     the_connection.mav.command_long_send(
#        the_connection.target_system, the_connection.target_component,
#        mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
#        0, mode_id, 0, 0, 0, 0, 0)
#     # the_connection.set_mode(mode_id) or:
#     # the_connection.mav.set_mode_send(
#     #     the_connection.target_system,
#     #     mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
#     #     mode_id)

#     while True:
#         # Wait for ACK command
#         # Would be good to add mechanism to avoid endlessly blocking
#         # if the autopilot sends a NACK or never receives the message
#         ack_msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
#         ack_msg = ack_msg.to_dict()

#         # Continue waiting if the acknowledged command is not `set_mode`
#         if ack_msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
#             continue

#         # Print the ACK result !
#         print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
#         break

# # UNUSED
# def update_mode_px4(the_connection, mode):

#     ################################################
#     # the_connection: mavlink connection [input]
#     # mode: int, id of the desired px4 mode [input]
#     ################################################

    
#     the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, 1, 0, 0, 0, 0, 0, 0)

#     while True:
#         # Wait for ACK command
#         # Would be good to add mechanism to avoid endlessly blocking
#         # if the autopilot sends a NACK or never receives the message
#         ack_msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
#         ack_msg = ack_msg.to_dict()

#         # Continue waiting if the acknowledged command is not `set_mode`
#         if ack_msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
#             continue

#         # Print the ACK result !
#         print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
#         break