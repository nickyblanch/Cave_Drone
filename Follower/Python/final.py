####################################################################################
# Author: Nicolas Blanchard, nickyblanch@arizona.edu, (520) 834-3191
# Created for Dr. Shkarayev at the University of Arizona
# Date: 1/10/23
# Purpose: Automatic control for follower drone in cave drone project.
# Dependencies: pymavlink, time

# Thank you to ardusub.com Intelligent Quads on YouTube for pymavlink references.


# ADDITIONAL COMMENTS

# Important: In order for this pymavlink script to execute on a ground station computer
# and still communicate with the drone, MAVProxy is required to route the MAVLINK
# messages. The following command should be used to start MAVProxy:

# mavproxy --master=udp:192.168.8.60:14550 --out 127.0.0.1:14551 --out 127.0.0.1:14552

# Then, a ground station (QGroundControl) can connect to UD port 14551 and this
# pymavlink script can connect to UDP port 14552.

# The modalai voxl flight will send its MAVLINK traffic to UDP port 14550 and it
# will be visible on both QGroundControl and this executing pymavlink script.

# Of course, it is also necessary for this ground station computer to be connected
# to the voxl's WiFi AP. For this project, the AP is named 'DRONE' and has a
# password of '123456789'.

####################################################################################

from pymavlink import mavutil
import time

####################################################################################

def main():

    ################################################
    # [no inputs or outputs]
    ################################################

    # Establish MAVLINK connection
    the_connection = setup()

    # Arm the system
    arm(the_connection)

    # Take off
    takeoff(the_connection, 0.1)
    request_local_NED(the_connection)

    # Enter offboard mode
    # TODO - the command to enter offboard mode does not currently work.
    # More information on PX4 operating mode numbers are required.
    # For now, offboard mode must be invoked manually from QGroundControl.
    
    # offboard(the_connection)

    # Loop
    while 1:

        # Note: In order for PX4 to remain in offboard mode, it needs to receive target commands
        # at a rate of at least 2 Hz.

        # Update current position
        request_local_NED(the_connection)


        try:
            # print(the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True).to_dict())
            msg = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=False).to_dict()
            x = msg["x"]
            y = msg["y"]
            z = msg["x"]
            msg_success = True
        except:
            msg_success = False
            print("Problem!")

        # Update target position
        if msg_success:
            x_target = x
            y_target = y
            z_target = z
            update_target_ned(the_connection, x_target, y_target, z_target)
        
        time.sleep(0.1)

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
    # alt: float, target altitude [input]
    ################################################

    # Takeoff command
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, alt)

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

    # Set our target
    boot_time = 10
    # the_connection.mav.set_position_target_local_ned_send(boot_time, the_connection.target_system, the_connection.target_component, 1,
    # type_mask=(
    #             # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_X_IGNORE |
    #             # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_Y_IGNORE |
    #             # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_Z_IGNORE |
    #             mavutil.mavlink.POSITION_TARGET_TYPEMASK_VX_IGNORE |
    #             mavutil.mavlink.POSITION_TARGET_TYPEMASK_VY_IGNORE |
    #             mavutil.mavlink.POSITION_TARGET_TYPEMASK_VZ_IGNORE |
    #             mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE |
    #             mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE |
    #             mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE |
    #             # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_FORCE_SET |
    #             mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_IGNORE |
    #             mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_RATE_IGNORE), x=1, y=1, z=0.5, vx=0, vy=0, vz=0, afx=0, afy=0, afz=0, yaw=0, yaw_rate=0)

    # type_mask=3576
    # the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(3576), float(x_val), float(y_val), float(z_val), 0, 0, 0, 0, 0, 0, 0, 0))
    the_connection.mav.set_position_target_local_ned_send(0, the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, type_mask=(
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_X_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_Y_IGNORE |
                # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_Z_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_VX_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_VY_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_VZ_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE |
                # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_FORCE_SET |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_IGNORE |
                mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_RATE_IGNORE), x=float(x_val), y=float(y_val), z=float(z_val), vx=0, vy=0, vz=0, afx=0, afy=0, afz=0, yaw=0, yaw_rate=0)

    # Verify that target is set
    request_target_pos_NED(the_connection)

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


####################################################################################
# TODO
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


def offboard(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    # mode: int, id of the desired px4 mode [input]
    ################################################

    
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, 1, 0, 0, 0, 0, 0, 0)

    while True:
        # Wait for ACK command
        # Would be good to add mechanism to avoid endlessly blocking
        # if the autopilot sends a NACK or never receives the message
        ack_msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
        ack_msg = ack_msg.to_dict()

        # Continue waiting if the acknowledged command is not `set_mode`
        if ack_msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
            continue

        # Print the ACK result !
        print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
        break


def land(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    # mode: int, id of the desired px4 mode [input]
    ################################################

    
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, 1, 0, 0, 0, 0, 0, 0)

    while True:
        # Wait for ACK command
        # Would be good to add mechanism to avoid endlessly blocking
        # if the autopilot sends a NACK or never receives the message
        ack_msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
        ack_msg = ack_msg.to_dict()

        # Continue waiting if the acknowledged command is not `set_mode`
        if ack_msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
            continue

        # Print the ACK result !
        print(mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description)
        break


####################################################################################
# Main function call
####################################################################################

main()