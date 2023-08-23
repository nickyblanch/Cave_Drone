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

# mavproxy --master=udp:192.168.1.125:14549 --out 127.0.0.1:14553
# mavproxy --master=udp:192.168.1.125:14550 --out 127.0.0.1:14551 --out 127.0.0.1:14552

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
# 2.) Change SYS_ID of Drone 2 -> Run two MAVProxy instances, each having one drone selected ->
#     each instance forwards to a different UDP port -> can connect two Pymavlink variables.

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

TARGET_X_1 = 0            # target x coordinate
TARGET_Y_1 = 0            # target y coordinate
TARGET_Z_1 = -1           # target z coordinate
TARGET_X_2 = 0            # target x coordinate
TARGET_Y_2 = 0            # target y coordinate
TARGET_Z_2 = -1           # target z coordinate


CURRENT_X_1 = 0           # current x coordinate
CURRENT_Y_1 = 0           # current y coordinate
CURRENT_Z_1 = 0           # current z coordinate
CURRENT_X_2 = 0           # current x coordinate
CURRENT_Y_2 = 0           # current y coordinate
CURRENT_Z_2 = 0           # current z coordinate


####################################################################################


def main():

    ################################################
    # [no inputs or outputs]
    ################################################

    global TARGET_X
    global TARGET_Y
    global TARGET_Z
    global CURRENT_X
    global CURRENT_Y
    global CURRENT_Z
    global SEND_TELEMETRY

    # Establish MAVLINK connection
    drone1, drone2 = setup()

    # Arm the system
    arm(drone1)
    arm(drone2)

    # Request local coordinates
    request_local_NED(drone1)
    request_local_NED(drone2)

    # Request target local coordinates
    request_target_pos_NED(drone1)
    request_target_pos_NED(drone2)

    # Initialize X, Y, Z
    msg = drone1.recv_match(type='LOCAL_POSITION_NED', blocking=True).to_dict()
    x = msg["x"]
    y = msg["y"]
    z = msg["z"]

    # Begin our telemtry thread
    t1 = threading.Thread(target=telemetry_loop_thread, args=(drone1,))
    t1.start()
    t2 = threading.Thread(target=telemetry_local_position_thread, args=(drone1,))
    t2.start()

    # Take off
    takeoff_CUSTOM(drone1, 1)
    takeoff_CUSTOM(drone2, 1)

    # Loop
    print("Entering loop")
    while 1:

        # Note: In order for PX4 to remain in offboard mode, it needs to receive target commands
        # at a rate of at least 2 Hz.
        SEND_TELEMETRY = 1

        # Update current position
        try:
            msg = drone1.messages['LOCAL_POSITION_NED']
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
            time.sleep(15)

            TARGET_X = 1
            TARGET_Y = 1
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = drone1.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z
            land(drone1)
            time.sleep(5)
            takeoff_CUSTOM(drone1, 1)
            time.sleep(5)

            TARGET_X = -1
            TARGET_Y = 1
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = drone1.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z
            land(drone1)
            time.sleep(5)
            takeoff_CUSTOM(drone1, 1)
            time.sleep(5)

            TARGET_X = -1
            TARGET_Y = -1
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = drone1.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z
            land(drone1)
            time.sleep(5)
            takeoff_CUSTOM(drone1, 1)
            time.sleep(5)

            TARGET_X = 1
            TARGET_Y = -1
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = drone1.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z
            land(drone1)
            time.sleep(5)
            takeoff_CUSTOM(drone1, 1)
            time.sleep(5)

            TARGET_X = 0
            TARGET_Y = 0
            TARGET_Z = -1
            time.sleep(8)
            # while( (x - TARGET_X) > .1 and (y - TARGET_Y) > 0.1 ):
                # msg = drone1.messages['LOCAL_POSITION_NED']
                # x = msg.x
                # y = msg.y
                # z = msg.z
            land(drone1)

        else:
            print("FLIGHT MODE NOT RECOGNIZED.")
            return


####################################################################################


def setup():

    ################################################
    # drone1: mavlink connection [output]
    # drone1: mavlink connection [output]
    ################################################

    # Start a connection listening on a UDP port
    # drone1 = mavutil.mavlink_connection('udp:127.0.0.1:14552')
    drone1 = mavutil.mavlink_connection('udp:127.0.0.1:14552')

    # Wait for the first heartbeat 
    drone1.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (drone1.target_system, drone1.target_component))

    # Start a connection listening on a UDP port
    drone2 = mavutil.mavlink_connection('udp:127.0.0.1:14553')

    # Wait for the first heartbeat 
    drone2.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (drone2.target_system, drone2.target_component))

    return drone1, drone2


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


def telemetry_loop_thread(the_connection_1, the_connection_2):

    ################################################
    # the_connection: mavlink connection [input]
    ################################################

    global TARGET_X_1
    global TARGET_Y_1
    global TARGET_Z_1
    global TARGET_X_2
    global TARGET_Y_2
    global TARGET_Z_2

    while SEND_TELEMETRY:
        update_target_ned(the_connection_1, TARGET_X_1, TARGET_Y_1, TARGET_Z_1)
        update_target_ned(the_connection_2, TARGET_X_2, TARGET_Y_2, TARGET_Z_2)

    return 0


def telemetry_local_position_thread(the_connection_1, the_connection_2):

    ############################################################
    # SUMMARY: telemetry_local_position_thread continually     #
    #          updates the local position coordinates of up    #
    #          to two drones.                                  #
    #                                                          #
    # the_connection_1: mavlink connection for drone 1 [input] #
    ############################################################

    global CURRENT_X_1
    global CURRENT_Y_1
    global CURRENT_Z_1
    global CURRENT_X_2
    global CURRENT_Y_2
    global CURRENT_Z_2

    while 1:
        try:
            msg = the_connection_1.messages['LOCAL_POSITION_NED']
            CURRENT_X_1 = msg.x
            CURRENT_Y_1 = msg.y
            CURRENT_Z_1 = msg.z
        except:
            print("Problem receiving LOCAL_POSITION_NED Mav message: 1.")
        try:
            msg = the_connection_2.messages['LOCAL_POSITION_NED']
            CURRENT_X_2 = msg.x
            CURRENT_Y_2 = msg.y
            CURRENT_Z_2 = msg.z
        except:
            print("Problem receiving LOCAL_POSITION_NED Mav message: 2.")
    

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


def debug_test_arm():

    ################################################
    # [no inputs or outputs]
    ################################################

    global TARGET_X
    global TARGET_Y
    global TARGET_Z
    global CURRENT_X
    global CURRENT_Y
    global CURRENT_Z
    global SEND_TELEMETRY

    # Establish MAVLINK connection
    drone1, drone2 = setup()

    # Arm the system
    arm(drone1)
    arm(drone2)

    # Request local coordinates
    request_local_NED(drone1)
    request_local_NED(drone2)

    # Request target local coordinates
    request_target_pos_NED(drone1)
    request_target_pos_NED(drone2)

    # Wait
    time.sleep(30)


def debug_test_demo():

    ################################################
    # [no inputs or outputs]
    ################################################

    global TARGET_X_1
    global TARGET_Y_1
    global TARGET_Z_1
    global TARGET_X_2
    global TARGET_Y_2
    global TARGET_Z_2

    global CURRENT_X_1
    global CURRENT_Y_1
    global CURRENT_Z_1
    global CURRENT_X_2
    global CURRENT_Y_2
    global CURRENT_Z_2

    global SEND_TELEMETRY

    # Initialize target coordinates
    TARGET_X_1 = 0
    TARGET_Y_1 = 0
    TARGET_Z_1 = -1

    TARGET_X_2 = 0
    TARGET_Y_2 = 0
    TARGET_Z_2 = -1

    # Establish MAVLINK connection
    drone1, drone2 = setup()

    # Arm the system
    arm(drone1)
    arm(drone2)

    # Request local coordinates
    request_local_NED(drone1)
    request_local_NED(drone2)

    # Request target local coordinates
    request_target_pos_NED(drone1)
    request_target_pos_NED(drone2)

    # Start telemetry threads
    t1 = threading.Thread(target=telemetry_loop_thread, args=(drone1,drone2,))
    t1.start()
    t2 = threading.Thread(target=telemetry_local_position_thread, args=(drone1,drone2,))
    t2.start()

    # Wait
    time.sleep(5)

    # Takeoff
    takeoff_CUSTOM(drone1, -1)
    takeoff_CUSTOM(drone2, -1)

    # Wait
    time.sleep(5)

    # Land
    land(drone1)
    land(drone2)

    # Wait
    time.sleep(30)

    # Return
    return

       

####################################################################################


if __name__ == "__main__":
    # main()
    # debug_test_takeoff()
    debug_test_demo()
