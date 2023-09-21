####################################################################################
#       Author: Nicolas Blanchard | nickyblanch@arizona.edu | (520) 834-3191
#         Date: 9/20/23
#      Purpose: 
# Dependencies: 
####################################################################################
# Libraries
####################################################################################


import tkinter as tk
from tkinter import ttk
from tkinter import *


####################################################################################
# Global variables
####################################################################################


drone_1_IP = "192.168.1.1"
drone_2_IP = "192.168.1.2"
drone_1_UDP = 1
drone_2_UDP = 1
window_width = 750
window_height = 450


####################################################################################
# Function definitions
####################################################################################


def setup():

    # DEBUG
    # print("Setup")

    # Use global window function
    global window
    global drone_1_IP_entry
    global drone_2_IP_entry
    global drone_1_UDP_entry
    global drone_2_UDP_entry

    # Create window
    window = Tk()

    # Set size of window
    window.geometry(str(window_width) + "x" +  str(window_height))

    # Create frames
    top_frame = Frame(window, bg='cyan', width=1920, height=window_height/5)
    left_frame = Frame(window, bg='red', width=window_width/2, height=window_height*3/5)
    right_frame = Frame(window, bg='yellow', width=window_width/2, height=window_height*3/5)
    bottom_frame = Frame(window, bg='blue', width=window_width/2, height=window_height/5)

    # Organize frames
    top_frame.grid(row=0, columnspan=2)
    left_frame.grid(row=1, column=0, sticky='nsew')
    right_frame.grid(row=1, column=1, sticky="nsew")
    bottom_frame.grid(row=2, columnspan=2, sticky="ew")

    # Formatting frames
    top_frame.grid_propagate(False)
    top_frame.pack_propagate(False)
    left_frame.grid_propagate(False)
    left_frame.pack_propagate(False)
    left_frame.columnconfigure(0, weight=2)
    left_frame.columnconfigure(1, weight=0)
    left_frame.columnconfigure(2, weight=1)
    right_frame.grid_propagate(False)
    right_frame.pack_propagate(False)
    right_frame.columnconfigure(0, weight=2)
    right_frame.columnconfigure(1, weight=0)
    right_frame.columnconfigure(2, weight=1)
    bottom_frame.grid_propagate(False)
    bottom_frame.pack_propagate(False)
    
    # Title
    title = Label(top_frame, text='CAVE DRONE GCS')
    title.pack()

    # Titles
    drone_1_title = Label(left_frame, text="Leader Drone")
    drone_1_title.grid(row=0, column=0, sticky='w')
    drone_2_title = Label(right_frame, text="Follower Drone")
    drone_2_title.grid(row=0, column=0, sticky='w')

    # IP Entry Widgets
    drone_1_IP_entry = Entry(left_frame, width=12, font=('Arial 16'))
    drone_1_IP_entry.grid(row=1, column=0, padx=5, pady=2, sticky='e')
    drone_2_IP_entry = Entry(right_frame, width=12, font=('Arial 16'))
    drone_2_IP_entry.grid(row=1, column=0, padx=5, pady=2, sticky='e')

    # UDP Entry Widgets
    drone_1_UDP_entry = Entry(left_frame, width=5, font=('Arial 16'))
    drone_1_UDP_entry.grid(row=1, column=1, pady=2, sticky='e')
    drone_2_UDP_entry = Entry(right_frame, width=5, font=('Arial 16'))
    drone_2_UDP_entry.grid(row=1, column=1, pady=2, sticky='e')

    # IP Buttons
    photo = PhotoImage(file = r"C:\Users\nicky\OneDrive\Pictures\wifi_small.png")

    drone_1_IP_button = Button(left_frame, image=photo, command=update_drone_1_IP)
    drone_1_IP_button.image = photo
    drone_1_IP_button.grid(row=1, column=2, padx=5, pady=2, sticky='w')
    drone_2_IP_button = Button(right_frame, image=photo, command=update_drone_2_IP)
    drone_2_IP_button.image = photo
    drone_2_IP_button.grid(row=1, column=2, padx=5, pady=2, sticky='w')

    # Other Buttons
    drone_1_arm_button = Button(left_frame, text="Arm Leader", width=20, command=lambda: arm_drone("1"))
    drone_1_arm_button.grid(row=2, column=0, padx=4, pady=2, sticky='e')
    drone_2_arm_button = Button(right_frame, text="Arm Follower", width=20, command=lambda: arm_drone("2"))
    drone_2_arm_button.grid(row=2, column=0, padx=4, pady=2, sticky='e')
    drone_1_takeoff_button = Button(left_frame, text="Takeoff Leader", width=20, command=lambda: arm_drone("1"))
    drone_1_takeoff_button.grid(row=3, column=0, padx=4, pady=2, sticky='e')
    drone_2_takeoff_button = Button(right_frame, text="Takeoff Follower", width=20, command=lambda: arm_drone("2"))
    drone_2_takeoff_button.grid(row=3, column=0, padx=4, pady=2, sticky='e')

    # TODO:
    # Add UDP port input
    # Add disarm button
    # Add land button
    # Add buttons for each mode (off, autnomous, demo, etc)
    # Add input for x,y,z target coordinates
    # Add current x,y,z coordinates in bottom frame

    # Configure grid
    window.rowconfigure(9)
    window.columnconfigure((0, 1), weight = 1, uniform="column")


def update_drone_1_IP():
   
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

    print(str(drone_1_IP) + ":" + str(drone_1_UDP))


def update_drone_2_IP():
   
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

    print(str(drone_2_IP) + ":" + str(drone_2_UDP))


def arm_drone(drone_number):
    print("DRONE " + drone_number + " ARMED")


def main():

    setup()

    window.mainloop()


####################################################################################
# Main
####################################################################################


main()