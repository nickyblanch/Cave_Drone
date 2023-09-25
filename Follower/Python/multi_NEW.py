###################################################################################################
#          Author: Nicolas Blanchard
#         Contact: nickyblanch@arizona.edu | (520) 834-3191
#         Purpose: Automatic control for follower drone in cave drone project.
#    Introduction: This code uses the pymavlink package (primarily the mavutil components) to
#                  create controls and a GUI for controlling drones running the PX4 flight
#                  stack. It is specifically tailored to test custom code, GPS-denied
#                  navigation, and 'train' (swarm) operation. Created as a part of my MS
#                  thesis in Electrical & Computer Engineering at the University of Arizona.
#    Dependencies: pymavlink, time, threading, os, tkinter
# Reproducibility: Tested to work on Windows 11 and Ubunutu 22.xx as of 9/25/2023. Please install
#                  the pymavlink and tkinter libraries before proceeding.

# Thank you to ardusub.com Intelligent Quads on YouTube for pymavlink references.

# ADDITIONAL COMMENTS

# Important: In order for this pymavlink script to execute on a ground station computer,
# run QGroundcontrol, and still communicate with the drone, MAVProxy is required to route
# the MAVLINK messages. The following command should be used to start MAVProxy:

# mavproxy --master=udp:192.168.1.125:14549 --out 127.0.0.1:14553
# mavproxy --master=udp:192.168.1.125:14550 --out 127.0.0.1:14551 --out 127.0.0.1:14552

# Then, a ground station (QGroundControl) can connect to UDP port 14551 and this
# pymavlink script can connect to UDP port 14552.

# The modalai voxl flight will send its MAVLINK traffic to UDP port 14550 and it
# will be visible on both QGroundControl and this executing pymavlink script.

# When calibrating sensors, the closest board orientation is: YAW 90 ROLL 90 PITCH 180

# NOTE: In QGroundcontrol, MAVLink forwarding must be enabled and the forwarding address
# must be port 14552.

###################################################################################################
# TODO

# 1.) Decrease proportional gain for velocity PID
# 2.) Change SYS_ID of Drone 2 -> Run two MAVProxy instances, each having one drone selected ->
#     each instance forwards to a different UDP port -> can connect two Pymavlink variables.

###################################################################################################

# DRONE 1: 192.168.1.124:
# DRONE 2: 192.168.1.126:14549

###################################################################################################


from pymavlink import mavutil
import time
import threading
import os
import tkinter as tk
from tkinter import ttk
from tkinter import *


###################################################################################################


FLIGHT_MODE = 4             # 0 = test mode: fly to (TEST_MODE_X, TEST_MODE_Y, TEST_MODE_Z)
                            # 1 = manual mode: fly to coordinates provided by user
                            # 2 = autonomous mode: fly to hard-coded coordinates
                            # 3 = demo: fly is a 2x2 meter square at an altitude of 1 meter.
                            # 4 = off.

TEST_MODE_X = 1             # target x coordinate in test mode
TEST_MODE_Y = 1             # target y coordinate in test mode
TEST_MODE_Z = -1            # targer z coordinate in test mode

SEND_TELEMETRY = 1          # 1 = send telemtry
                            # 0 = don't send telemtry

LAND = 0                    # 1 = landing
                            # 0 = normal operation

TARGET_X_1 = 0              # target x coordinate
TARGET_Y_1 = 0              # target y coordinate
TARGET_Z_1 = -1             # target z coordinate
TARGET_X_2 = 0              # target x coordinate
TARGET_Y_2 = 0              # target y coordinate
TARGET_Z_2 = -1             # target z coordinate


CURRENT_X_1 = 0             # current x coordinate
CURRENT_Y_1 = 0             # current y coordinate
CURRENT_Z_1 = 0             # current z coordinate
CURRENT_X_2 = 0             # current x coordinate
CURRENT_Y_2 = 0             # current y coordinate
CURRENT_Z_2 = 0             # current z coordinate

drone_1_IP = "192.168.1.1"  # IP address of Drone 1
drone_2_IP = "192.168.1.2"  # IP address of Drone 2
drone_1_UDP = 1             # UDP port of Drone 1
drone_2_UDP = 1             # UDP port of Drone 2
window_width = 750          # Width of GUI window
window_height = 450         # Length of GUI window

drone1 = 0                  # Drone 1 variable
drone2 = 0                  # Drone 2 variable


###################################################################################################


def main():
    ################################################
    # Main!
    ################################################

    # Setup GUI
    setup_GUI()

    # Setup
    setup()

    # Window mainloop
    # window.after(1000, flight_loop())
    window.after(100, update_current_coords)
    window.mainloop()
    

def flight_loop():
    ################################################
    # [no inputs or outputs]
    ################################################


    global TARGET_X
    global TARGET_Y
    global TARGET_Z
    global SEND_TELEMETRY


    # Note: In order for PX4 to remain in offboard mode, it needs to receive target commands
    # at a rate of at least 2 Hz.

    ############################################################
    # NAVIGATION                                               #
    ############################################################

    # TEST MODE
    if (FLIGHT_MODE == 0):
        # Test mode
        TARGET_X = TEST_MODE_X
        TARGET_Y = TEST_MODE_Y
        TARGET_Z = TEST_MODE_Z

    # MANUAL MODE
    elif (FLIGHT_MODE == 1):
        try:
            TARGET_X, TARGET_Y, TARGET_Z = input("Enter target x y z: ").split()
        except:
            print("Error reading input coordinates.")
        finally:
            print("Going to: " + str(TARGET_X) + ", " + str(TARGET_Y) + ", " + str(TARGET_Z))

    # AUTONOMOUS MODE
    elif (FLIGHT_MODE == 2):
        pass

    # DEMO MODE
    elif (FLIGHT_MODE == 3 and drone1 and drone2):

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

    # OFF
    elif(FLIGHT_MODE == 4):
        if drone1:
            disarm(drone1)
        if drone2:
            disarm(drone2)

    else:
        print("FLIGHT MODE NOT RECOGNIZED.")
        return
    
    window.after(1000, flight_loop())
    

###################################################################################################


def setup_GUI():
    ################################################
    # [no inputs or outputs]
    ################################################

    # Use global window function
    global window
    global drone_1_IP_entry
    global drone_2_IP_entry
    global drone_1_UDP_entry
    global drone_2_UDP_entry
    global drone_1_x_entry
    global drone_1_y_entry
    global drone_1_z_entry
    global drone_2_x_entry
    global drone_2_y_entry
    global drone_2_z_entry
    global drone_1_x_coord
    global drone_1_y_coord
    global drone_1_z_coord
    global drone_2_x_coord
    global drone_2_y_coord
    global drone_2_z_coord

    # Create window
    window = Tk()

    # Set size of window
    window.geometry(str(window_width) + "x" +  str(window_height))

    # Create frames
    top_frame = Frame(window, width=1920, height=window_height/5)
    left_frame = Frame(window, width=window_width/2, height=window_height*2/5)
    left_frame_bottom = Frame(window, width=window_width/2, height=window_height*1/10)
    left_frame_bottom_coords = Frame(window, width=window_width/2, height=window_height*1/10)
    right_frame = Frame(window, width=window_width/2, height=window_height*2/5)
    right_frame_bottom = Frame(window, width=window_width/2, height=window_height*1/10)
    right_frame_bottom_coords = Frame(window, width=window_width/2, height=window_height*1/10)
    bottom_frame = Frame(window, width=window_width/2, height=window_height/5)
    
    # Organize frames
    top_frame.grid(row=0, columnspan=2)
    left_frame.grid(row=1, column=0, sticky='nsew')
    left_frame_bottom.grid(row=2, column=0, sticky='nsew')
    left_frame_bottom_coords.grid(row=3, column=0, sticky='nsew')
    right_frame.grid(row=1, column=1, sticky="nsew")
    right_frame_bottom.grid(row=2, column=1, sticky='nsew')
    right_frame_bottom_coords.grid(row=3, column=1, sticky='nsew')
    bottom_frame.grid(row=4, columnspan=2, sticky="ew")

    # Formatting frames
    top_frame.grid_propagate(False)
    top_frame.pack_propagate(False)
    left_frame.grid_propagate(False)
    left_frame.pack_propagate(False)
    left_frame.columnconfigure(0, weight=2)
    left_frame.columnconfigure(1, weight=0)
    left_frame.columnconfigure(2, weight=1)
    left_frame_bottom.grid_propagate(False)
    left_frame_bottom.pack_propagate(False)
    left_frame_bottom.columnconfigure(0, weight=1)
    left_frame_bottom.columnconfigure(1, weight=0)
    left_frame_bottom.columnconfigure(2, weight=0)
    left_frame_bottom.columnconfigure(3, weight=0)
    left_frame_bottom.columnconfigure(4, weight=1)
    left_frame_bottom_coords.grid_propagate(False)
    left_frame_bottom_coords.pack_propagate(False)
    left_frame_bottom_coords.columnconfigure(0, weight=1)
    left_frame_bottom_coords.columnconfigure(3, weight=1)
    right_frame.grid_propagate(False)
    right_frame.pack_propagate(False)
    right_frame.columnconfigure(0, weight=2)
    right_frame.columnconfigure(1, weight=0)
    right_frame.columnconfigure(2, weight=1)
    right_frame_bottom.grid_propagate(False)
    right_frame_bottom.pack_propagate(False)
    right_frame_bottom.columnconfigure(0, weight=1)
    right_frame_bottom.columnconfigure(1, weight=0)
    right_frame_bottom.columnconfigure(2, weight=0)
    right_frame_bottom.columnconfigure(3, weight=0)
    right_frame_bottom.columnconfigure(4, weight=1)
    right_frame_bottom_coords.grid_propagate(False)
    right_frame_bottom_coords.pack_propagate(False)
    right_frame_bottom_coords.columnconfigure(0, weight=1)
    right_frame_bottom_coords.columnconfigure(3, weight=1)
    bottom_frame.grid_propagate(False)
    bottom_frame.pack_propagate(False)
    bottom_frame.columnconfigure(0, weight=1)
    bottom_frame.columnconfigure(1, weight=1)
    bottom_frame.columnconfigure(2, weight=1)
    bottom_frame.columnconfigure(3, weight=1)
    bottom_frame.columnconfigure(4, weight=1)
    bottom_frame.columnconfigure(5, weight=1)
    bottom_frame.rowconfigure(0, weight=1)

    # TODO: Set backgrounds
    cwd = os.getcwd()
    mars_top = PhotoImage(file = cwd+"\Follower\Python\GUI_Images\mars_top.png", master=window)
    background_label_top = Label(top_frame, image=mars_top)
    background_label_top.img = mars_top
    background_label_top.place(x=0, y=0, relwidth=1, relheight=1)
    mars_left = PhotoImage(file = cwd+"\Follower\Python\GUI_Images\mars_left.png", master=window)
    background_label_left = Label(left_frame, image=mars_left)
    background_label_left.img = mars_left
    background_label_left.place(x=0, y=0, relwidth=1, relheight=1)
    mars_left_bottom = PhotoImage(file = cwd+"\Follower\Python\GUI_Images\mars_left_bottom.png", master=window)
    background_label_left_bottom = Label(left_frame_bottom, image=mars_left_bottom)
    background_label_left_bottom.img = mars_left_bottom
    background_label_left_bottom.place(x=0, y=0, relwidth=1, relheight=1)
    mars_left_bottom_coords = PhotoImage(file = cwd+"\Follower\Python\GUI_Images\mars_left_bottom_coords.png", master=window)
    background_label_left_bottom_coords = Label(left_frame_bottom_coords, image=mars_left_bottom_coords)
    background_label_left_bottom_coords.img = mars_left_bottom_coords
    background_label_left_bottom_coords.place(x=0, y=0, relwidth=1, relheight=1)
    mars_right = PhotoImage(file = cwd+"\Follower\Python\GUI_Images\mars_right.png", master=window)
    background_label_right = Label(right_frame, image=mars_right)
    background_label_right.img = mars_right
    background_label_right.place(x=0, y=0, relwidth=1, relheight=1)
    mars_right_bottom = PhotoImage(file =cwd+"\Follower\Python\GUI_Images\mars_right_bottom.png", master=window)
    background_label_right_bottom = Label(right_frame_bottom, image=mars_right_bottom)
    background_label_right_bottom.img = mars_right_bottom
    background_label_right_bottom.place(x=0, y=0, relwidth=1, relheight=1)
    mars_right_bottom_coords = PhotoImage(file = cwd+"\Follower\Python\GUI_Images\mars_right_bottom_coords.png", master=window)
    background_label_right_bottom_coords = Label(right_frame_bottom_coords, image=mars_right_bottom_coords)
    background_label_right_bottom_coords.img = mars_right_bottom_coords
    background_label_right_bottom_coords.place(x=0, y=0, relwidth=1, relheight=1)
    mars_bottom = PhotoImage(file = cwd+"\Follower\Python\GUI_Images\mars_bottom.png", master=window)
    background_label_bottom = Label(bottom_frame, image=mars_bottom)
    background_label_bottom.img = mars_bottom
    background_label_bottom.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Title
    title = Label(top_frame, text='CAVE DRONE GCS', font=('Arial 26'))
    title.pack()

    # Titles
    drone_1_title = Label(left_frame, text="Leader Drone", font=('Arial 20'))
    drone_1_title.grid(row=0, column=0, sticky='w')
    drone_2_title = Label(right_frame, text="Follower Drone", font=('Arial 20'))
    drone_2_title.grid(row=0, column=0, sticky='w')

    # IP Entry Widgets
    drone_1_IP_entry = Entry(left_frame, width=12, font=('Arial 16'))
    drone_1_IP_entry.grid(row=1, column=0, padx=5, pady=10, sticky='e')
    drone_2_IP_entry = Entry(right_frame, width=12, font=('Arial 16'))
    drone_2_IP_entry.grid(row=1, column=0, padx=5, pady=10, sticky='e')

    # UDP Entry Widgets
    drone_1_UDP_entry = Entry(left_frame, width=5, font=('Arial 16'))
    drone_1_UDP_entry.grid(row=1, column=1, pady=10, sticky='w')
    drone_2_UDP_entry = Entry(right_frame, width=5, font=('Arial 16'))
    drone_2_UDP_entry.grid(row=1, column=1, pady=10, sticky='w')

    # IP Buttons
    photo = PhotoImage(file = r"C:\Users\nicky\OneDrive\Pictures\wifi_small.png")

    drone_1_IP_button = Button(left_frame, image=photo, command=update_drone_1_IP)
    drone_1_IP_button.image = photo
    drone_1_IP_button.grid(row=1, column=2, padx=5, pady=10, sticky='w')
    drone_2_IP_button = Button(right_frame, image=photo, command=update_drone_2_IP)
    drone_2_IP_button.image = photo
    drone_2_IP_button.grid(row=1, column=2, padx=5, pady=10, sticky='w')

    # Arm buttons
    drone_1_arm_button = Button(left_frame, text="Arm Leader", width=20, command=lambda: arm(drone1))
    drone_1_arm_button.grid(row=2, column=0, padx=4, pady=2, sticky='e')
    drone_2_arm_button = Button(right_frame, text="Arm Follower", width=20, command=lambda: arm(drone2))
    drone_2_arm_button.grid(row=2, column=0, padx=4, pady=2, sticky='e')

    # Disarm buttons
    drone_1_disarm_button = Button(left_frame, text="Disarm Leader", width=20, command=lambda: disarm(drone1))
    drone_1_disarm_button.grid(row=2, column=1, columnspan=2, padx=4, pady=2, sticky='w')
    drone_2_disarm_button = Button(right_frame, text="Disarm Follower", width=20, command=lambda: disarm(drone2))
    drone_2_disarm_button.grid(row=2, column=1, columnspan=2, padx=4, pady=2, sticky='w')

    # Takeoff buttons
    drone_1_takeoff_button = Button(left_frame, text="Takeoff Leader", width=20, command=lambda: takeoff_CUSTOM(drone1, -.75))
    drone_1_takeoff_button.grid(row=3, column=0, padx=4, pady=2, sticky='e')
    drone_2_takeoff_button = Button(right_frame, text="Takeoff Follower", width=20, command=lambda: takeoff_CUSTOM(drone2, -.75))
    drone_2_takeoff_button.grid(row=3, column=0, padx=4, pady=2, sticky='e')

    # Land buttons
    drone_1_land_button = Button(left_frame, text="Land Leader", width=20, command=lambda: land(drone1))
    drone_1_land_button.grid(row=3, column=1, columnspan=2, padx=4, pady=2, sticky='w')
    drone_2_land_button = Button(right_frame, text="Land Follower", width=20, command=lambda: land(drone2))
    drone_2_land_button.grid(row=3, column=1, columnspan=2, padx=4, pady=2, sticky='w')

    # Mode buttons
    drone_1_off_button = Button(left_frame_bottom, text="OFF", width=7, command=lambda: update_flight_mode(1, 4))
    drone_1_off_button.grid(row=1, column=0, padx=4, pady=2, sticky='e')
    drone_1_test_button = Button(left_frame_bottom, text="TEST", width=7, command=lambda: update_flight_mode(1, 0))
    drone_1_test_button.grid(row=1, column=1, padx=4, pady=2, sticky='w')
    drone_1_manual_button = Button(left_frame_bottom, text="MANUAL", width=7, command=lambda: update_flight_mode(1, 1))
    drone_1_manual_button.grid(row=1, column=2, padx=4, pady=2, sticky='w')
    drone_1_demo_button = Button(left_frame_bottom, text="DEMO", width=7, command=lambda: update_flight_mode(1, 3))
    drone_1_demo_button.grid(row=1, column=3, padx=4, pady=2, sticky='w')
    drone_1_autonomous_button = Button(left_frame_bottom, text="AUTO", width=7, command=lambda: update_flight_mode(1, 2))
    drone_1_autonomous_button.grid(row=1, column=4, padx=4, pady=2, sticky='w')
    drone_2_off_button = Button(right_frame_bottom, text="OFF", width=7, command=lambda: update_flight_mode(2, 4))
    drone_2_off_button.grid(row=1, column=0, padx=4, pady=2, sticky='e')
    drone_2_test_button = Button(right_frame_bottom, text="TEST", width=7, command=lambda: update_flight_mode(2, 0))
    drone_2_test_button.grid(row=1, column=1, padx=4, pady=2, sticky='w')
    drone_2_manual_button = Button(right_frame_bottom, text="MANUAL", width=7, command=lambda: update_flight_mode(2, 1))
    drone_2_manual_button.grid(row=1, column=2, padx=4, pady=2, sticky='w')
    drone_2_demo_button = Button(right_frame_bottom, text="DEMO", width=7, command=lambda: update_flight_mode(2, 3))
    drone_2_demo_button.grid(row=1, column=3, padx=4, pady=2, sticky='w')
    drone_2_autonomous_button = Button(right_frame_bottom, text="AUTO", width=7, command=lambda: update_flight_mode(2, 2))
    drone_2_autonomous_button.grid(row=1, column=4,padx=4, pady=2, sticky='w')

    # Manual coordinate entries
    drone_1_x_entry = Entry(left_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_1_x_entry.grid(row=1, column=0, pady=10, sticky='e')
    drone_1_y_entry = Entry(left_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_1_y_entry.grid(row=1, column=1, pady=10)
    drone_1_z_entry = Entry(left_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_1_z_entry.grid(row=1, column=2, pady=10)
    drone_2_x_entry = Entry(right_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_2_x_entry.grid(row=1, column=0, pady=10, sticky='e')
    drone_2_y_entry = Entry(right_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_2_y_entry.grid(row=1, column=1, pady=10)
    drone_2_z_entry = Entry(right_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_2_z_entry.grid(row=1, column=2, pady=10)

    # Manual coordinate entry button
    drone_1_coords_button = Button(left_frame_bottom_coords, text='✓', width=5, command=update_coords_drone_1)
    drone_1_coords_button.grid(row=1, column=3, columnspan=2, padx=4, pady=2, sticky='w')
    drone_2_coords_button = Button(right_frame_bottom_coords, text='✓', width=5, command=update_coords_drone_2)
    drone_2_coords_button.grid(row=1, column=3, columnspan=2, padx=4, pady=2, sticky='w')

    # Current coordinate feedback
    drone_1_x_coord = Label(bottom_frame, text='1.01', font=('Arial 16'))
    drone_1_x_coord.grid(row = 0, column = 0)
    drone_1_y_coord = Label(bottom_frame, text='0.75', font=('Arial 16'))
    drone_1_y_coord.grid(row = 0, column = 1)
    drone_1_z_coord = Label(bottom_frame, text='-0.88', font=('Arial 16'))
    drone_1_z_coord.grid(row = 0, column = 2)
    drone_2_x_coord = Label(bottom_frame, text='1.01', font=('Arial 16'))
    drone_2_x_coord.grid(row = 0, column = 3)
    drone_2_y_coord = Label(bottom_frame, text='0.75', font=('Arial 16'))
    drone_2_y_coord.grid(row = 0, column = 4)
    drone_2_z_coord = Label(bottom_frame, text='-0.88', font=('Arial 16'))
    drone_2_z_coord.grid(row = 0, column = 5)
    drone_1_x_lab = Label(bottom_frame, text='X', font=('Arial 16'))
    drone_1_x_lab.grid(row = 1, column = 0)
    drone_1_y_lab = Label(bottom_frame, text='Y', font=('Arial 16'))
    drone_1_y_lab.grid(row = 1, column = 1)
    drone_1_z_lab = Label(bottom_frame, text='Z', font=('Arial 16'))
    drone_1_z_lab.grid(row = 1, column = 2)
    drone_2_x_lab = Label(bottom_frame, text='X', font=('Arial 16'))
    drone_2_x_lab.grid(row = 1, column = 3)
    drone_2_y_lab = Label(bottom_frame, text='Y', font=('Arial 16'))
    drone_2_y_lab.grid(row = 1, column = 4)
    drone_2_z_lab = Label(bottom_frame, text='Z', font=('Arial 16'))
    drone_2_z_lab.grid(row = 1, column = 5)

    # TODO:
    # Add current x,y,z coordinates in bottom frame

    # Configure grid
    window.resizable(False, False)
    window.title("MAV Lab")
    window.rowconfigure(9)
    window.columnconfigure((0, 1), weight = 1, uniform="column")


def update_current_coords():
    ################################################
    # [no inputs or outputs]
    ################################################
    drone_1_x_coord.config(text=str(CURRENT_X_1))
    drone_1_y_coord.config(text=str(CURRENT_Y_1))
    drone_1_z_coord.config(text=str(CURRENT_Z_1))

    drone_2_x_coord.config(text=str(CURRENT_X_2))
    drone_2_y_coord.config(text=str(CURRENT_Y_2))
    drone_2_z_coord.config(text=str(CURRENT_Z_2))

    # window.after(0, update_current_coords)


def update_drone_1_IP():
    ################################################
    # [no inputs or outputs]
    ################################################
   
    global drone_1_IP
    global drone_1_IP_entry
    global drone_1_UDP
    global drone_1_UDP_entry

    temp = drone_1_IP_entry.get()

    if temp != "":
        drone_1_IP = temp

    temp = drone_1_UDP_entry.get()

    if temp != "":
        drone_1_UDP = temp

    establish_connection(1, drone_1_IP, drone_1_UDP)
    print(str(drone_1_IP) + ":" + str(drone_1_UDP))


def update_drone_2_IP():
    ################################################
    # [no inputs or outputs]
    ################################################
   
    global drone_2_IP
    global drone_2_IP_entry
    global drone_2_UDP
    global drone_2_UDP_entry

    temp = drone_2_IP_entry.get()

    if temp != "":
        drone_2_IP = temp

    temp = drone_2_UDP_entry.get()

    if temp != "":
        drone_2_UDP = temp
        
    establish_connection(2, drone_2_IP, drone_2_UDP)
    print(str(drone_2_IP) + ":" + str(drone_2_UDP))


def update_flight_mode(number, mode):
    ################################################
    # number: 1 or 2, drone [input]
    # mode: 0-4, flight mode [input]
    ################################################

    global FLIGHT_MODE

    if number == 1:
        FLIGHT_MODE = mode
    if number == 2:
        pass


def update_coords_drone_1():
    ################################################
    # [no inputs or outputs]
    ################################################

    global TARGET_X_1
    global TARGET_Y_1
    global TARGET_Z_1
    TARGET_X_1=drone_1_x_entry.get()
    TARGET_Y_1=drone_1_y_entry.get()
    TARGET_Z_1=drone_1_z_entry.get()


def update_coords_drone_2():
    ################################################
    # [no inputs or outputs]
    ################################################

    global TARGET_X_2
    global TARGET_Y_2
    global TARGET_Z_2
    TARGET_X_2=drone_2_x_entry.get()
    TARGET_Y_2=drone_2_y_entry.get()
    TARGET_Z_2=drone_2_z_entry.get()


###################################################################################################


def setup():
    ################################################
    # [no inputs or outputs]
    ################################################

    # Begin our telemtry thread
    t1 = threading.Thread(target=telemetry_loop_thread, args=(drone1,drone2))
    t1.start()
    t2 = threading.Thread(target=telemetry_local_position_thread, args=(drone1,drone2))
    t2.start()


def establish_connection(number, IP, UDP):

    ################################################
    # drone1: mavlink connection [output] (via global)
    # drone1: mavlink connection [output] (via global)
    ################################################

    global drone1
    global drone2

    global CURRENT_X_1
    global CURRENT_Y_1
    global CURRENT_Z_1
    global CURRENT_X_2
    global CURRENT_Y_2
    global CURRENT_Z_2

    if number == 1:
        # Start a connection listening on a UDP port
        drone1 = mavutil.mavlink_connection('udp:' + str(IP) + ':' + str(UDP))

        # Wait for the first heartbeat 
        drone1.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (drone1.target_system, drone1.target_component))

        # Request target and local positions
        request_local_NED(drone1)
        request_target_pos_NED(drone1)

        # Initialize current position
        msg = drone1.recv_match(type='LOCAL_POSITION_NED', blocking=True).to_dict()
        CURRENT_X_1 = msg["x"]
        CURRENT_Y_1 = msg["y"]
        CURRENT_Z_1= msg["z"]


    elif number == 2:
        # Start a connection listening on a UDP port
        drone2 = mavutil.mavlink_connection('udp:' + str(IP) + ':' + str(UDP))

        # Wait for the first heartbeat 
        drone2.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (drone2.target_system, drone2.target_component))
    
        # Request target and local position
        request_local_NED(drone2)
        request_target_pos_NED(drone2)

        # Initialize current position
        msg = drone2.recv_match(type='LOCAL_POSITION_NED', blocking=True).to_dict()
        CURRENT_X_2 = msg["x"]
        CURRENT_Y_2 = msg["y"]
        CURRENT_Z_2= msg["z"]

    # Re-do telemetry thread
    setup()


def arm(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    ################################################

    # Arm the system
    if the_connection:
        the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

        # Wait until arming confirmed (can manually check with the_connection.motors_armed())
        print("Waiting for the vehicle to arm")
        the_connection.motors_armed_wait()
        print('Armed!')


def disarm(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    ################################################

    # Arm the system
    if the_connection:
        the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)

        # Wait until arming confirmed (can manually check with the_connection.motors_armed())
        print("Waiting for the vehicle to disarm")
        the_connection.motors_disarmed_wait()
        print('Disarmed!')


def takeoff(the_connection, alt):

    ################################################
    # the_connection: mavlink connection [input]
    # alt: float, target altitude [input] UNUSED
    ################################################

    # Takeoff command
    if the_connection:
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
    if the_connection:
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
    if the_connection:
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

    if the_connection:
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

    if the_connection:
        the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, mavutil.mavlink.MAVLINK_MSG_ID_LOCAL_POSITION_NED, 1e6/20, 0, 0, 0, 0, 0)


def request_target_pos_NED(the_connection):

    ################################################
    # the_connection: mavlink connection [input]
    ################################################

    if the_connection:
        the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, mavutil.mavlink.MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED, 1e6/20, 0, 0, 0, 0, 0)


def telemetry_loop_thread(the_connection_1, the_connection_2):

    ################################################
    # SUMMARY: telemtry_loop_thread continually sends
    #          target coordinates for the drones
    #          to navigate towards in offboard mode.
    #
    # the_connection: mavlink connection [input]
    ################################################

    global TARGET_X_1
    global TARGET_Y_1
    global TARGET_Z_1
    global TARGET_X_2
    global TARGET_Y_2
    global TARGET_Z_2

    while SEND_TELEMETRY:
        # print("TARGET: " + str(TARGET_X_1)) #DEBUG

        if the_connection_1:
            update_target_ned(the_connection_1, TARGET_X_1, TARGET_Y_1, TARGET_Z_1)
        if the_connection_2:
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
        if the_connection_1:
            try:
                msg = the_connection_1.messages['LOCAL_POSITION_NED']
                CURRENT_X_1 = msg.x
                CURRENT_Y_1 = msg.y
                CURRENT_Z_1 = msg.z
            except:
                print("Problem receiving LOCAL_POSITION_NED Mav message: 1.")
        if the_connection_2:
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


###################################################################################################


if __name__ == "__main__":
    main()
    pass

