from pymavlink import mavutil
import time

# Test
print("Program Starting!")

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udp:127.0.0.1:14552')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

# Once connected, use 'the_connection' to get and send messages
# index = 0
# while 1:
#     # msg = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)
#     msg = the_connection.recv_match(blocking=True)
#     index = index + 1

#     # if index % 10000 == 1:
#     print(msg)

# Arm the system
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

# Wait until arming confirmed (can manually check with the_connection.motors_armed())
print("Waiting for the vehicle to arm")
the_connection.motors_armed_wait()
print('Armed!')


# Set our target
boot_time = 0
the_connection.mav.set_position_target_local_ned_send(0, the_connection.target_system, the_connection.target_component, 1,
type_mask=(
            # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_X_IGNORE |
            # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_Y_IGNORE |
            # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_Z_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_VX_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_VY_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_VZ_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE |
            # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_FORCE_SET |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_RATE_IGNORE
            ), x=0.5, y=0.5, z=0.5, vx=0, vy=0, vz=0, afx=0, afy=0, afz=0, yaw=0, yaw_rate=0)

# Verift that target is set
# the_connection.mav.position_target_local_ned(0, 1, 0, )

# the_connection.mav.request_data_stream_send(the_connection.target_system, the_connection.target_component,
#                                         mavutil.mavlink.POSITION_TARGET_LOCAL_NED, 1, 1)

the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, mavutil.mavlink.MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED, 1e6/50, 0, 0, 0, 0, 2)
# the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, 0, mavutil.mavlink.MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED, 0, 0, 0, 0, 0, 2)


while 1:
    try: 
        print(the_connection.recv_match().to_dict())
    except:
        print('No GPS_RAW_INT message received')

    the_connection.mav.set_position_target_local_ned_send(0, the_connection.target_system, the_connection.target_component, 1,
    type_mask=(
            # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_X_IGNORE |
            # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_Y_IGNORE |
            # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_Z_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_VX_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_VY_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_VZ_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE |
            # DON'T mavutil.mavlink.POSITION_TARGET_TYPEMASK_FORCE_SET |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_IGNORE |
            mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_RATE_IGNORE
            ), x=0.5, y=0.5, z=0.5, vx=0, vy=0, vz=0, afx=0, afy=0, afz=0, yaw=0, yaw_rate=0)

    # the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, mavutil.mavlink.MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED, 1e6/50, 0, 0, 0, 0, 0)
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, mavutil.mavlink.MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED, 1e6/50, 0, 0, 0, 0, 0)


    # try:
    #     print(the_connection.recv_match().to_dict())
    # except:
    #     pass
    time.sleep(0.1)


